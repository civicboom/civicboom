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
        
        response       = self.app.get(url('member_action', id='unittest', action='content', format='json'))
        response_json  = json.loads(response.body)
        response_etags = get_etag_dict(response)
        
        