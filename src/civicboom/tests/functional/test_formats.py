from civicboom.tests import *


class TestFormats(TestController):

    def test_formats(self):
        """
        Frag and HTML Templates often customise there look depending if a logged_in_persona is present - sometimes these can error as anon use is not tested
        Run the other formats though their paces
        """
        
        def test_all_formats():
            
            for format in ['json', 'xml', 'frag', 'html', 'rss']:
                # Content Lists
                response = self.app.get(url('contents', creator='unittest', format=format), status=200)
                self.assertIn('API Documentation', response)
                # Member Lists
                response = self.app.get(url('members' , term='unittest', format=format), status=200)
                self.assertIn("Mr U. Test", response)
                # Message Lists
                if self.logged_in_as:
                    response = self.app.get(url('messages', list='notification', sort='timestamp', format=format), status=200)
                    self.assertIn('Base Notification', response)
                
                # Content
                response = self.app.get(url('content', id=1         , format=format), status=200)
                self.assertIn('API Documentation', response)
                # Member
                response = self.app.get(url('member' , id='unittest', format=format), status=200)
                self.assertIn('unittest'         , response)
                # Message
                if self.logged_in_as and format not in ['rss']:
                    response = self.app.get(url('message', id=1, format=format), status=200)
                    self.assertIn('Base Message', response)
        
        test_all_formats() # Logged in user
        self.log_out()
        test_all_formats() # Anon user

    def test_sub_domains(self):
        
        def test_all_sub_domains():
            def get_(url_, sub_domain):
                return self.app.get(url_, extra_environ={'HTTP_HOST': '%s.civicboom_test.com' % sub_domain}, status=200)
                
            for sub_domain in ['mobile', 'widget']:
                # Content Lists
                response = get_(url('contents', creator='unittest'), sub_domain)
                self.assertIn('API Documentation', response)
                # Member Lists
                response = get_(url('members' , term='unittest'   ), sub_domain)
                self.assertIn("Mr U. Test", response)
                
                # Content
                response = get_(url('content', id=1         ), sub_domain)
                self.assertIn('API Documentation', response)
                # Member
                response = get_(url('member' , id='unittest'), sub_domain)
                self.assertIn('unittest'         , response)
                # Message
                if self.logged_in_as and sub_domain not in ['widget']:
                    # Check messages template
                    response = get_(url('messages', sort='timestamp'), sub_domain)
                    self.assertIn('Base Notification', response)
                    response = get_(url('message', id=1), sub_domain)
                    self.assertIn('Base Message', response)
        
        test_all_sub_domains() # Logged in user
        self.log_out()
        test_all_sub_domains() # Anon user
