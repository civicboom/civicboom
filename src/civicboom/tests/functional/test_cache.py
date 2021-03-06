from civicboom.tests import *

from pylons import config

from civicboom.lib.cache import cache_separator, key_var_separator, list_item_separator

from nose.plugins.skip import SkipTest

ver_threshold = 2 # AllanC - when updating items the updates events fire multiple times in some cases so the version number could jump 2 or 3 at a time. If we are incrementing version numbers greater than this threshold then error

# -- Utils ---------------------------------------------------------------------

def get_etag_dict(response):
    """
    A response object will contain an eTag if it is set.
    This extracts the eTag from the response and attempts to break it into it's component parts
    Under normal circunstances the eTag is not ment to be deconstructed in this way. It is only ment to reflect a simple "change in state".
    For testing it is a neat way to assess the state of the cache
    """
    etag_dict = {}
    etag = response.header('etag')
    etag = etag[1:-1] # Remove first and last char as these are double quotes
    #print etag
    for etag_key_value in etag.split(cache_separator):
        try:
            key, value = etag_key_value.split(key_var_separator)
            # AllanC - not proud of this. An eTag can be generated with two fields the same e.g. list_name is response_to and a kwarg param response_to .. the later always overwrites the first
            #          The order of the etag is not important. It's only these automated tests that actually inspoect the etag for deeper testing.
            #          I've made the decition for the automated tests to only use the FIRST instance of a key name so that the tests function correctly. I dont see the need to rename the entire lists for this
            if key not in etag_dict: 
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
        """
        func_get_list - a function to perform a get/post and return a response
        func_create   - a function that will modify the list aquired by funct_get_list
        func_remove   - a string to indicate 'content' or 'member' to remove OR a function to do custom removal of the created object
        """
        
        def check_list_version(key, ver):
            self.assertIsBetween(int(get_etag_dict(response)[key]), ver+1, ver+ver_threshold) # Check list_version has incremented by 1 - it should not increment more than 1 because only one medification has been performed
        
        # Get content list
        response         = func_get_list()
        response_json    = json.loads(response.body)
        
        # Record list vars
        list_etag  = response.header('etag')
        list_count = response_json['data']['list']['count']
        if list_version_key_to_check:
            list_version = int(get_etag_dict(response)[list_version_key_to_check])
            #print "%s:%s" %(list_version_key_to_check, list_version)
        
        # Create content
        id = func_create() # a record the id of the item created
        
        # Get new list
        response         = func_get_list()
        response_json    = json.loads(response.body)
        # Check Assertions
        self.assertNotEqual(response.header('etag')               , list_etag      ) # Check list etag has changed
        self.assertEqual   (response_json['data']['list']['count'], list_count + 1 ) # Check list count has incremented by 1
        self.assertIn      (str(id)                               , response.body  ) # Loose presence check
        if list_version_key_to_check:
            check_list_version(list_version_key_to_check, list_version)
        
        # Abort if no remove method spcifyed (we have tested all we can)
        if not func_remove:
            return
        
        # Remove the created item
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
        
        # Check list updated on remove
        response         = func_get_list()
        response_json    = json.loads(response.body)
        # Check list assertions
        self.assertNotEqual(response.header('etag')               , list_etag ) # Check list etag has changed
        self.assertEqual   (response_json['data']['list']['count'], list_count) # Check list count is the same as it was to begin with
        if list_version_key_to_check:
            check_list_version(list_version_key_to_check, list_version)

    
    # -- Content List --------------------------------------------------------
    
    def test_content_list(self):
        """
        Attempt to get lists - modify them - and check version number has incremented
        """
        self.log_in_as('unittest')
        self._test_list(lambda: self.app.get(url('member_action' , id='me'     , action='content'  , format='json')), lambda: self.create_content(title='cache test'                                ), list_version_key_to_check='content'    )
        self._test_list(lambda: self.app.get(url('contents'      , creator='me', list='drafts'     , format='json')), lambda: self.create_content(title='cache test', type='draft'                  ), list_version_key_to_check='drafts'     )
        self._test_list(lambda: self.app.get(url('contents'      , creator='me', list='articles'   , format='json')), lambda: self.create_content(title='cache test', type='article'                ), list_version_key_to_check='articles'   )
        self._test_list(lambda: self.app.get(url('contents'      , creator='me', list='assignments', format='json')), lambda: self.create_content(title='cache test', type='assignment'             ), list_version_key_to_check='assignments')
        self._test_list(lambda: self.app.get(url('contents'      , creator='me', list='responses'  , format='json')), lambda: self.create_content(title='cache test', type='article'   , parent_id=1), list_version_key_to_check='responses'  )
        self._test_list(lambda: self.app.get(url('content_action', id=1        , action='responses', format='json')), lambda: self.create_content(title='cache test', type='article'   , parent_id=1), list_version_key_to_check='response_to')
        self._test_list(lambda: self.app.get(url('content_action', id=1        , action='comments' , format='json')), lambda: self.comment(1,'cache_test')                                           , list_version_key_to_check='comments_to') #, func_remove=None
        
        #'boomed_by'   : {'boomed_by': None},



    def test_delete_from_admin_pannel(self):
        """
        Delete an item using the admin pannel and check that the list version numbers are updated
        This should work as the the admin pannel uses the SQLAlchemy model and invlidation events are tied to the model
        """
        raise SkipTest("Not implemented")


    def test_content_morph(self):
        """
        morph a draft from one type to another
        """
        # Profile
        self.log_in_as('unittest')
        response      = self.app.get(url(controller='profile', action='index', format='json'))
        #response_json = json.loads(response.body)
        self.assertIn("Mr U. Test", response.body)
        
        # Create draft - check on profile
        content_id = self.create_content(title='cache morph test', content='cache morph test', type='draft', target_type='assignment')
        response      = self.app.get(url(controller='profile', action='index', format='json'))
        response_json = json.loads(response.body)
        self.assertEquals("cache morph test", response_json['data']['drafts']['items'][0]['title'])
        self.assertEquals(content_id        , response_json['data']['drafts']['items'][0]['id']   )
        draft_count = response_json['data']['drafts']['count']
        
        # Publish draft - it should become an assignment
        self.publish_content(content_id)
        
        # Check lists have updated
        response      = self.app.get(url(controller='profile', action='index', format='json'))
        response_json = json.loads(response.body)
        self.assertEquals(response_json['data']['drafts']['count'], draft_count - 1)
        self.assertIn("cache morph test", response.body)
        self.assertEquals(content_id        , response_json['data']['assignments_active']['items'][0]['id'])
        
        # Cleanup
        self.delete_content(content_id)