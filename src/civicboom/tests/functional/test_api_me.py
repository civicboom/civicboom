from civicboom.tests import *


class TestAccountController(TestController):

    def test_api_me(self):
        # Create content
        content_id = self.create_content(title="Me in API", content="Me in API", type="article") # Create an item of content to ensure unittest has some content
        
        # Compare username with 'me'
        response          = self.app.get(url('member', id='unittest', format='json'))        
        response_unittest = response.body
        response          = self.app.get(url('member', id='me'      , format='json'))
        response_me       = response.body
        self.assertEqual(response_unittest, response_me)
        
        response          = self.app.get(url('member_action', id='unittest', action='content', format='json'))
        response_unittest = response.body
        response          = self.app.get(url('member_action', id='me'      , action='content', format='json'))
        response_me       = response.body
        self.assertEqual(response_unittest, response_me)
        
        response          = self.app.get(url('contents', creator='unittest', format='json'))
        response_unittest = response.body
        response          = self.app.get(url('contents', creator='me'      , format='json'))
        response_me       = response.body
        self.assertEqual(response_unittest, response_me)

        #response_json = json.loads(response.body)
        #content_count = response_json['data']['list']['count']
        
        self.delete_content(content_id)
