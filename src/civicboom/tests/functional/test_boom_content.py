from civicboom.tests import *
import json

class TestBoomController(TestController):
    
    def test_all(self):
        
        #-----------------------------------------------------------------------
        
        self.log_in_as('unittest')
        
        # Create publis content as unittest
        response = self.app.post(
            url('contents', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'title'        : u'Content to BOOM!',
                'contents'     : u'This tests is going to Boom be boomed by unitfriend' ,
                'type'         : u'article' ,
                'submit_publish': u'publish' ,
            },
            status=201
        )
        response_json = json.loads(response.body)
        content_id = int(response_json['data']['id'])
        assert content_id > 0
        
        self.log_in_as('unitfriend')
        
        # View the unittests profile as unitfriend
        response = self.app.get(url('member', id='unittest', format='json'), status=200)
        response_json = json.loads(response.body)
        assert 'unittest'         in response
        assert 'Content to BOOM!' in response
        
        # Does unitfriend have the 'boom' action
        response = self.app.get(url('content', id=content_id, format='json'), status=200)
        response_json = json.loads(response.body)
        assert 'boomed by unitfriend'
        assert 'boom' in response_json['data']['actions']
        boom_count = int(response_json['data']['content']['boom_count'])
        
        # Boom unittest's content as unitfriend
        response = self.app.post(
            url('content_action', action='boom', id=content_id, format='json'),
            params={
                '_authentication_token': self.auth_token,
            },
            status=200
        )
        response_json = json.loads(response.body)
        
        response = self.app.get(url('member_action', action='boomed_content', id='unitfriend', format='json'), status=200)
        response_json = json.loads(response.body)
        assert 'Content to BOOM!' in response
        
        # Check that the content appears in unitfriends profile
        response = self.app.get(url('member', id='unitfriend', format='json'), status=200)
        response_json = json.loads(response.body)
        assert 'Content to BOOM!' in response
        
        # Check the boom count has been incremented
        response = self.app.get(url('content', id=content_id, format='json'), status=200)
        response_json = json.loads(response.body)
        assert 'boomed by unitfriend'
        assert 'boom' in response_json['data']['actions']
        assert  int(response_json['data']['content']['boom_count']) == boom_count + 1
        
        #-----------------------------------------------------------------------
        
        # Ensure boomed content for other is unaffected after boom - login and get boom count
        # Logged as issue 231
        self.log_in_as('kitten')
        
        response      = self.app.get(url('member', id='kitten', format='json'), status=200)
        response_json = json.loads(response.body)
        assert len(response_json['data']['boomed_content']) == 0
        
        response = self.app.post(
            url('content_action', action='boom', id=content_id, format='json'),
            params={
                '_authentication_token': self.auth_token,
            },
            status=200
        )
        response_json = json.loads(response.body)
        
        response      = self.app.get(url('member', id='kitten', format='json'), status=200)
        response_json = json.loads(response.body)
        assert len(response_json['data']['boomed_content']) == 1
