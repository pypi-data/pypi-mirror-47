import logging
import django_rq

from algoliasearch import algoliasearch
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.test.client import RequestFactory

from .utils import underscore_to_camelcase, recursive_key_map

algolia_settings = settings.ALGOLIA
APP_ID = algolia_settings['APPLICATION_ID']
API_KEY = algolia_settings['API_KEY']

logger = logging.getLogger('indexer')


class BaseIndexer(object):
    serializer_class = None
    index_name = None

    def __init__(self):
        if not self.serializer_class:
            raise NotImplementedError
        if not self.index_name:
            raise NotImplementedError
        if not self.model:
            raise NotImplementedError

        '''Initializes the index'''
        client = algoliasearch.Client(APP_ID, API_KEY)
        self.__client = client
        self.__set_index(client)

    def __set_index(self, client):
        '''Get an instance of Algolia Index'''
        self.__index = client.init_index(self.index_name)
        self.__tmp_index = client.init_index(self.index_name + '_tmp')

    def get_objectID(self, instance):
        key = self.get_property_for_objectID()
        return getattr(instance, key)

    def get_property_for_objectID(self):
        return 'id'

    def get_index_setting_dict(self):
        return {
            "attributesToIndex": [],
            "attributesForFaceting": [],
            "attributesToRetrieve": [],
            "customRanking": [],
            "attributesToHighlight": []
        }

    def get_synonyms_list(self):
        """
        Override this method if we are using update_synonyms.
        @example
        [{ objectID: "optional-but-better-to-use-it", type: "synonym", synonyms: ["abc", "cba"] }] == abc <=> cba
        Must return list of synonym
        @see https://www.algolia.com/doc/api-reference/api-methods/save-synonym/#method-param-synonym-object
        @return list of dict
        """
        return None

    def index_wait_task(self, index, taskID):
        return index.wait_task(taskID)

    def get_index_all_queryset(self):
        return self.model.objects.all()

    def get_index_partial_queryset(self, list_of_objectID):
        kwargs = {'{0}__{1}'.format(
            self.get_property_for_objectID(), 'in'): list_of_objectID}
        return self.model.objects.filter(**kwargs)

    def get_stale_tracker_model(self):
        # Untuk ngetrack yang mana aja yang butuh direindex
        # Bakal dipanggil : Model.objects.update_or_create(objectID)
        return None

    def build_object(self, instance):
        user = AnonymousUser()

        # Create fake context
        SERVER_NAME = "localhost:8000"
        context = dict(request=RequestFactory().get(
            '/', SERVER_NAME=SERVER_NAME))
        context['request'].user = user
        request = context['request']

        # Build object
        # - object to dictionary
        ser = self.serializer_class(instance, context=context)
        obj = ser.data
        # - convert to camelcase
        res = recursive_key_map(underscore_to_camelcase, obj)
        # - attach objectID
        res['objectID'] = self.get_objectID(instance)
        return res

    """
        Reindexing Interfaces
    """

    def reindex_one(self, objectID, wait_task=False):
        self.reindex_partial([objectID], wait_task=wait_task)
        logger.info('UPDATED %s OBJECT %s', objectID, self.index_name)

    def wait_task(self, result):
        if type(result) is list and len(result) > 0:
            max_task_id = result[0]['taskID']
            for item in result:
                if max_task_id < item['taskID']:
                    max_task_id = item['taskID']
            self.__index.wait_task(max_task_id)
        elif type(result) is dict:
            self.__index.wait_task(result['taskID'])

    def reindex_partial(self, list_of_objectID, batch_size=150, wait_task=False):
        qs = self.get_index_partial_queryset(list_of_objectID)

        counts = 0
        result = None
        batch = []

        for idx, instance in enumerate(qs):
            builded_object = self.build_object(instance)
            print("Building object ( %d / %d ) %s" %
                  ((idx + 1), len(qs), builded_object.get('objectID')))

            batch.append(builded_object)
            if len(batch) >= batch_size:
                result = self.__index.save_objects(batch)
                if wait_task:
                    self.wait_task(result)

                logger.info('SAVE %d OBJECTS TO %s', len(batch),
                            self.index_name)
                self.post_update(batch, result)
                batch = []
            counts += 1
        if len(batch) > 0:  # handle when batch is not all cleared
            result = self.__index.save_objects(batch)
            if wait_task:
                self.wait_task(result)

            logger.info('SAVE %d OBJECTS TO %s', len(batch),
                        self.index_name)
            self.post_update(batch, result)
            counts += 1

        # Assume all items are reindexed
        return counts

    def reindex_all(self, batch_size=150, async=False):
        qs = self.get_index_all_queryset()

        '''Spawn workers '''
        counts = 0
        batch_counts = 0
        result = None
        objectIDs = []

        for idx, instance in enumerate(qs):
            objectIDs.append(self.get_objectID(instance))
            if len(objectIDs) >= batch_size:
                if async:
                    django_rq.enqueue(self.reindex_partial, objectIDs)
                else:
                    self.reindex_partial(objectIDs)
                batch_counts += 1
                objectIDs = []
            counts += 1
        if len(objectIDs) > 0:  # handle when batch is not all cleared
            if async:
                django_rq.enqueue(self.reindex_partial, objectIDs)
            else:
                self.reindex_partial(objectIDs)
            batch_counts += 1
        print("Spawning %d tasks" % batch_counts)

        print("Done")

    def reindex_update_one(self, objectID):
        self.reindex_update_partial([objectID], wait_task=wait_task)
        logger.info('UPDATED %s OBJECT %s', objectID, self.index_name)

    def reindex_update_partial(self, list_of_objectID, batch_size=150, wait_task=False):
        qs = self.get_index_partial_queryset(list_of_objectID)

        counts = 0
        result = None
        batch = []

        for idx, instance in enumerate(qs):
            builded_object = self.build_object(instance)
            print("Building object ( %d / %d ) %s" %
                  ((idx + 1), len(qs), builded_object.get('objectID')))

            batch.append(builded_object)
            if len(batch) >= batch_size:
                result = self.__index.partial_update_objects(batch)
                if wait_task:
                    self.wait_task(result)

                logger.info('SAVE %d OBJECTS TO %s', len(batch),
                            self.index_name)
                self.post_update(batch, result)
                batch = []
            counts += 1
        if len(batch) > 0:  # handle when batch is not all cleared
            result = self.__index.partial_update_objects(batch)
            if wait_task:
                self.wait_task(result)

            logger.info('SAVE %d OBJECTS TO %s', len(batch),
                        self.index_name)
            self.post_update(batch, result)
            counts += 1

        # Assume all items are reindexed
        return counts

    def reindex_update_all(self, batch_size=150, async=False):
        qs = self.get_index_all_queryset()

        '''Spawn workers '''
        counts = 0
        batch_counts = 0
        result = None
        objectIDs = []

        for idx, instance in enumerate(qs):
            objectIDs.append(self.get_objectID(instance))
            if len(objectIDs) >= batch_size:
                if async:
                    django_rq.enqueue(self.reindex_update_partial, objectIDs)
                else:
                    self.reindex_update_partial(objectIDs)
                batch_counts += 1
                objectIDs = []
            counts += 1
        if len(objectIDs) > 0:  # handle when batch is not all cleared
            if async:
                django_rq.enqueue(self.reindex_update_partial, objectIDs)
            else:
                self.reindex_update_partial(objectIDs)
            batch_counts += 1
        print("Spawning %d tasks" % batch_counts)

        print("Done")

    def reindex_delete_one(self, objectID):
        self.reindex_delete_partial([objectID])
        logger.info('DELETED %s OBJECT %s', objectID, self.index_name)

    def reindex_delete_partial(self, list_of_objectID, batch_size=150):
        counts = 0
        result = None
        batch = []

        for idx, objectId in enumerate(list_of_objectID):
            batch.append(objectId)
            if len(batch) >= batch_size:
                result = self.__index.delete_objects(batch)
                logger.info('DELETE %d OBJECTS ON %s', len(batch),
                            self.index_name)
                batch = []
            counts += 1
        if len(batch) > 0:  # handle when batch is not all cleared
            result = self.__index.delete_objects(batch)
            logger.info('DELETE %d OBJECTS ON %s', len(batch),
                        self.index_name)
            counts += 1
        return counts

    def rebuild_all(self, batch_size=150):
        qs = self.get_index_all_queryset()

        '''Reindex all records.'''
        self.__tmp_index.clear_index()
        logger.debug('CLEAR INDEX %s_tmp', self.index_name)

        counts = 0
        result = None
        batch = []

        for idx, instance in enumerate(qs):
            builded_object = self.build_object(instance)
            print("Building object ( %d / %d ) %s" %
                  ((idx + 1), len(qs), builded_object.get('url')))

            batch.append(builded_object)
            if len(batch) >= batch_size:
                result = self.__tmp_index.save_objects(batch)
                logger.info('SAVE %d OBJECTS TO %s_tmp', len(batch),
                            self.index_name)
                batch = []
            counts += 1
        if len(batch) > 0:  # handle when batch is not all cleared
            result = self.__tmp_index.save_objects(batch)
            logger.info('SAVE %d OBJECTS TO %s_tmp', len(batch),
                        self.index_name)

        self.__tmp_index.set_settings(self.get_index_setting_dict())

        if result:
            self.__client.move_index(self.index_name + '_tmp', self.index_name)
            # self.__client.
            logger.info('MOVE INDEX %s_tmp TO %s', self.index_name,
                        self.index_name)
        return counts

    def update_settings(self):
        self.__index.set_settings(self.get_index_setting_dict())
        print("Settings updated")

    def update_synonyms(self, forward_to_replicas=False, replace_existing_synonyms=False):
        """
        Create or update many synonyms to indexer.

        This function will replace synonym automatically with same objectID. If we don't
        declare objectID algolia doesn't recognize them individually and unknown synonym will be created.

        It is recommended to use unique objectID on every synonym or use replace_existing_synonyms True
        everytime we call update_synonyms.

        @see https://www.algolia.com/doc/api-reference/api-methods/batch-synonyms/
        """
        synonyms = self.get_synonyms_list()

        if synonyms is None:
            raise Exception("get_synonyms_list is not implemented")

        result = self.__index.batch_synonyms(
            synonyms,
            forward_to_replicas=forward_to_replicas,
            replace_existing_synonyms=replace_existing_synonyms)
        self.wait_task(result)
        print("Synonyms updated")

    def post_update(self, batch, result):
        Tracker = self.get_stale_tracker_model()

        if Tracker is not None:
            self.index_wait_task(self.__index, result['taskID'])

            for entity in batch:
                Tracker.objects.update_or_create(entity['objectID'])
