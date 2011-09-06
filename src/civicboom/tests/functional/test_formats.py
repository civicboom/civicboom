from civicboom.tests import *


class TestFormats(TestController):

    def test_formats(self):
        """
        Frag and HTML Templates often customise there look depending if a logged_in_persona is present - sometimes these can error as anon use is not tested
        Run the other formats though their paces
        """
        
        def test_all_formats():
            for format in ['json', 'xml', 'frag', 'html', 'rss']:
                response = self.app.get(url('content', id=1         , format=format), status=200)
                self.assertIn('API Documentation', response)
                response = self.app.get(url('member' , id='unittest', format=format), status=200)
                self.assertIn('unittest'         , response)
        
        test_all_formats() # Logged in user
        self.log_out()
        test_all_formats() # Anon user

    def test_sub_domains(self):
        def test_all_sub_domains():
            for sub_domain in ['mobile', 'widget']:
                response = self.app.get(url('content', id=1         ), extra_environ={'HTTP_HOST': '%s.civicboom_test.com' % sub_domain}, status=200)
                self.assertIn('API Documentation', response)
                response = self.app.get(url('member' , id='unittest'), extra_environ={'HTTP_HOST': '%s.civicboom_test.com' % sub_domain}, status=200)
                self.assertIn('unittest'         , response)
        
        test_all_sub_domains() # Logged in user
        self.log_out()
        test_all_sub_domains() # Anon user
