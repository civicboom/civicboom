from civicboom.tests import *

class TestRSSController(TestController):

    def test_rss_member(self):
        
        def create_content(title):
            response = self.app.post(
                url('contents', format='json'),
                params={
                    '_authentication_token': self.auth_token,
                    'title'         : title      ,
                    'contents'      : title      ,
                    'type'          : u'article' ,
                    'submit_publish': u'publish' ,
                },
                status=201
            )
            response_json = json.loads(response.body)
            id = int(response_json['data']['id'])
            assert id > 0
            return id
        
        
        
        #response      = self.app.get(url('member', id='unittest', format='json'), status=200)
        #response_json = json.loads(response.body)
        
        rss_content_id = create_content('rss content test')
        
        # AllanC - member.rss now uses all the separte lists and therefor does not have a single date sorted contents list to go out over RSS
        #          in prefernce users are expected to use contents/index
        #response      = self.app.get(url('member', id='unittest', format='rss'), status=200)
        response      = self.app.get(url('contents', creator='unittest', format='rss'), status=200)
        assert 'rss content test' in response
        
        response      = self.app.get(url('content', id=rss_content_id, format='rss'), status=200)
        assert 'rss content test' in response
        
        response      = self.app.get(url('members' , format='rss'), status=200)
        response      = self.app.get(url('contents', format='rss'), status=200)
        response      = self.app.get(url('messages', format='rss'), status=200)