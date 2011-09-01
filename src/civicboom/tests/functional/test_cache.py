from civicboom.tests import *

from pylons import config

from civicboom.lib.cache import cache_separator, key_var_separator, list_item_separator

from nose.plugins.skip import SkipTest

# -- Utils ---------------------------------------------------------------------

def get_etag_dict(response):
    etag_dict = {}
    etag = response.header('etag')
    etag = etag[1:-1] # Remove first and last char as these are double quotes
    for etag_key_value in etag.split(cache_separator):
        try:
            key, value = etag_key_value.split(key_var_separator)
            etag_dict[key] = value
        except:
            etag_dict[etag_key_value] = ''
    return etag_dict

    

# -- Tests ---------------------------------------------------------------------

class TestCache(TestController):
    
    def setUp(self):
        if not (config['beaker.cache.enabled'] and config['cache.etags.enabled']):
            #log.warn('Cache not enabled - skipping cache tests')
            raise SkipTest('Cache not enabled in config - cache test skipped')
    
    def _test_list(self, func_get_list, func_create, func_remove='content', list_version_key_to_check=None):
        # Get content list
        response         = func_get_list()
        response_json    = json.loads(response.body)
        
        # Record list vars
        list_etag  = response.header('etag')
        list_count = response_json['data']['list']['count']
        if list_version_key_to_check:
            list_version = int(get_etag_dict(response)[list_version_key_to_check])
        
        # Create content
        id = func_create()
        
        # Get new list
        response         = func_get_list()
        response_json    = json.loads(response.body)
        # Check Assertions
        self.assertNotEqual(response.header('etag')               , list_etag      ) # Check list etag has changed
        self.assertEqual   (response_json['data']['list']['count'], list_count + 1 ) # Check list count has incremented by 1
        self.assertIn      (str(id)                               , response.body  ) # Loose presence check
        if list_version_key_to_check:
            self.assertEqual(int(get_etag_dict(response)[list_version_key_to_check]), list_version + 1) # Optinaly check list_version has incremented by 1 - it should not increment more than 1 because only one medification has been performed
        
        # Some items like comments cant be removed - this is optinal cleanup and test
        if func_remove:
            list_etag  = response.header('etag') # Record the start of the list
            if list_version_key_to_check:
                list_version = int(get_etag_dict(response)[list_version_key_to_check])
            
            # Cleanup
            if callable(func_remove):
                func_remove(id)
            elif func_remove=='content':
                self.delete_content(id)
            elif func_remove=='member':
                self.delete_member(id)
            
            # Get new list
            response         = func_get_list()
            response_json    = json.loads(response.body)
            # Check Assertions
            self.assertNotEqual(response.header('etag')               , list_etag ) # Check list etag has changed
            self.assertEqual   (response_json['data']['list']['count'], list_count) # Check list count is the same as it was to begin with
            if list_version_key_to_check:
                self.assertEqual(int(get_etag_dict(response)[list_version_key_to_check]), list_version + 1) # Optinaly check list_version has incremented by 1 - it should not increment more than 1

    
    # -- Content List --------------------------------------------------------
    
    def test_content_list(self):
        """
        Attempt to get lists - modify them - and check version number has incremented
        """
        self.log_in_as('unittest')
        self._test_list(lambda: self.app.get(url('member_action' , id='me'     , action='content'  , format='json')), lambda: self.create_content(title='cache test'                                ), list_version_key_to_check='content'    )
        self._test_list(lambda: self.app.get(url('contents'      , creator='me', list='drafts'     , format='json')), lambda: self.create_content(title='cache test', type='draft'                  ), list_version_key_to_check='drafts'     )
        self._test_list(lambda: self.app.get(url('contents'      , creator='me', list='articles'   , format='json')), lambda: self.create_content(title='cache test', type='article'                ), list_version_key_to_check='articles'   )
        self._test_list(lambda: self.app.get(url('contents'      , creator='me', list='assignments', format='json')), lambda: self.create_content(title='cache test', type='assignment'             ), list_version_key_to_check='assignment' )
        self._test_list(lambda: self.app.get(url('contents'      , creator='me', list='responses'  , format='json')), lambda: self.create_content(title='cache test', type='article'   , parent_id=1), list_version_key_to_check='responses'  )
        self._test_list(lambda: self.app.get(url('content_action', id=1        , action='responses', format='json')), lambda: self.create_content(title='cache test', type='article'   , parent_id=1), list_version_key_to_check='response_to')
        #self._test_list(lambda: self.app.get(url('content_action', id=1        , action='comments' , format='json')), lambda: self.comment(1,'cache_test')                                           , None)
        
        #'boomed_by'   : {'boomed_by': None},        



    def test_delete_from_admin_pannel(self):
        """
        Delete an item using the admin pannel and check that the list version numbers are updated
        This should work as the the admin pannel uses the SQLAlchemy model and invlidation events are tied to the model
        """
        # TODO
        pass
        