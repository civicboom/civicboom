from civicboom.tests import *


class TestBoom(TestController):
    
    def test_boom(self):
        self.log_in_as('unittest')
        
        # Create public content as unittest
        content_id = self.create_content(title=u'Content to BOOM!', contents=u'This tests is going to Boom be boomed by unitfriend', type=u'article')
        
        self.log_in_as('unitfriend')
        
        # Count content (to be used for assertion later)
        response      = self.app.get(url('member_action', action='content'       , id='unitfriend', format='json'), status=200)
        response_json = json.loads(response.body)
        count_content = response_json['data']['list']['count']
        # Count boomed (to be used for assertion later)
        response      = self.app.get(url('member_action', action='boomed', id='unitfriend', format='json'), status=200)
        response_json = json.loads(response.body)
        count_boomed  = response_json['data']['list']['count']
        
        
        # View the unittests profile as unitfriend
        response      = self.app.get(url('member', id='unittest', format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertIn('unittest'        , response)
        self.assertIn('Content to BOOM!', response)
        
        # Does unitfriend have the 'boom' action
        response      = self.app.get(url('content', id=content_id, format='json'), status=200)
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
        response      = self.app.get(url('member_action', action='boomed', id='unitfriend', format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertIn('Content to BOOM!', response)
        
        # Check that the content appears in unitfriends profile
        response      = self.app.get(url('member', id='unitfriend', format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertIn('Content to BOOM!', response)
        
        # Check the boom count has been incremented
        response      = self.app.get(url('content', id=content_id, format='json'), status=200)
        response_json = json.loads(response.body)
        # assert 'boomed by unitfriend'
        self.assertIn('unboom', response_json['data']['actions'])
        self.assertEqual( int(response_json['data']['content']['boom_count']), boom_count + 1)
        
        # Check the 'content and boomed' union stream
        response      = self.app.get(url('member_action', action='content_and_boomed', id='unitfriend', format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertIn('Content to BOOM!', response)
        self.assertEqual( int(response_json['data']['list']['count']), count_content + count_boomed + 1)
        
        
        #-----------------------------------------------------------------------
        
        # Ensure boomed content for other is unaffected after boom - login and get boom count
        # Logged as issue #231
        self.log_in_as('kitten')
        
        response      = self.app.get(url('member', id='kitten', format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertEqual(len(response_json['data']['boomed']['items']), 0)
        
        self.boom_content(content_id)
        
        response      = self.app.get(url('member', id='kitten', format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertEqual(len(response_json['data']['boomed']['items']), 1)


        #-----------------------------------------------------------------------
        
        # TODO: try to boom private content - "should get error"
        
        #-----------------------------------------------------------------------
        
        # Delete content that has been boomed to test Delete cascade behaviour
        
        self.log_in_as('unittest')

        self.delete_content(content_id)

        # Check that the content DOSE NOT appear in unitfriends profile
        response = self.app.get(url('member', id='unitfriend', format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertNotIn('Content to BOOM!', response)


    def test_unboom(self):
        self.log_in_as('unittest')
        content_id = self.create_content(title=u'Content to BOOM!', contents=u'This tests is going to Boom be boomed by unitfriend', type=u'article')
        
        self.log_in_as('unitfriend')
        self.boom_content(content_id)
        self.unboom_content(content_id)
        
        self.assertNotIn(content_id, [item['id'] for item in self.get_member('unitfriend')['boomed']['items']])

        self.log_in_as('unittest')
        self.delete_content(content_id)