from civicboom.tests import *
#import json


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
                #'submit_publish': u'publish' ,
            },
            status=201
        )
        response_json = json.loads(response.body)
        content_id = int(response_json['data']['id'])
        self.assertNotEqual(content_id, 0)
        
        self.log_in_as('unitfriend')
        
        # View the unittests profile as unitfriend
        response = self.app.get(url('member', id='unittest', format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertIn('unittest'        , response)
        self.assertIn('Content to BOOM!', response)
        
        # Does unitfriend have the 'boom' action
        response = self.app.get(url('content', id=content_id, format='json'), status=200)
        response_json = json.loads(response.body)
        # assert 'boomed by unitfriend'
        self.assertIn('boom', response_json['data']['actions'])
        boom_count = int(response_json['data']['content']['boom_count'])
        
        # Boom unittest's content as unitfriend
        self.boom_content(content_id)
        
        # Try to Boom it again - expected error because you can only boom it once
        response = self.app.post(
            url('content_action', action='boom', id=content_id, format='json'),
            params={
                '_authentication_token': self.auth_token,
            },
            status=400
        )
        response_json = json.loads(response.body)
        
        # Check that it appears in unitfriend's boomed list
        response = self.app.get(url('member_action', action='boomed_content', id='unitfriend', format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertIn('Content to BOOM!', response)
        
        # Check that the content appears in unitfriends profile
        response = self.app.get(url('member', id='unitfriend', format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertIn('Content to BOOM!', response)
        
        # Check the boom count has been incremented
        response = self.app.get(url('content', id=content_id, format='json'), status=200)
        response_json = json.loads(response.body)
        # assert 'boomed by unitfriend'
        self.assertIn('boom', response_json['data']['actions'])
        self.assertEqual( int(response_json['data']['content']['boom_count']), boom_count + 1)
        
        #-----------------------------------------------------------------------
        
        # Ensure boomed content for other is unaffected after boom - login and get boom count
        # Logged as issue #231
        self.log_in_as('kitten')
        
        response      = self.app.get(url('member', id='kitten', format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertEqual(len(response_json['data']['boomed_content']['items']), 0)
        
        self.boom_content(content_id)
        
        response      = self.app.get(url('member', id='kitten', format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertEqual(len(response_json['data']['boomed_content']['items']), 1)


        #-----------------------------------------------------------------------
        
        # TODO: try to boom private content - "should get error"
        
        #-----------------------------------------------------------------------
        
        # Delete content that has been boomed to test Delete cascade behaviour
        
        self.log_in_as('unittest')
        
        response = self.app.delete(
            url('content', id=content_id, format="json"),
            params={'_authentication_token': self.auth_token,},
            status=200
        )

        # Check that the content DOSE NOT appear in unitfriends profile
        response = self.app.get(url('member', id='unitfriend', format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertNotIn('Content to BOOM!', response)
