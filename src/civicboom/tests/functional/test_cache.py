from civicboom.tests import *

from pylons import config

from civicboom.lib.cache import cache_separator, key_var_separator, list_item_separator

class TestCache(TestController):
    
    def test_cache(self):
        if not (config['beaker.cache.enabled'] and config['cache.etags.enabled']):
            log.warn('Cache not enabled - skipping cache tests')
            return
        
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
        
        # -- Content List ------------------------------------------------------
        
        # Get content list
        response         = self.app.get(url('member_action', id='unittest', action='content', format='json'))
        response_json    = json.loads(response.body)
        
        # Record list vars
        list_content_ver = get_etag_dict(response)['content']
        list_count       = response_json['data']['list']['count']
        
        # Create content
        content_id = self.create_content(title='cache test')
        
        # Get new list
        response         = self.app.get(url('member_action', id='unittest', action='content', format='json'))
        response_json    = json.loads(response.body)
        
        # Check Assertions
        self.assertNotEqual(get_etag_dict(response)['content']     , list_content_ver) # Check list version has changed
        self.assertEqual   ( response_json['data']['list']['count'], list_count + 1  ) # Check list count has incremented by 1
        
        # Cleanup
        self.delete_content(content_id)
