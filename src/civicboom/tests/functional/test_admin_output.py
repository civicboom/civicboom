from civicboom.tests import *

class TestAdminEmails(TestController):
    
    def test_summary_emails(self):
        num_emails = getNumEmails()
        
        response = self.app.get(url(controller='task', action='email_new_user_summary'))
        
        self.assertEqual(getNumEmails(), num_emails + 1)
        email_response = getLastEmail()
        self.assertTrue(email_response.content_text)
        self.assertIn  ('unittest'  , email_response.content_text)
        self.assertIn  ('unitfriend', email_response.content_text)


    def test_user_emails_csv(self):
        response = self.app.get(url(controller='test', action='user_emails_csv'))
        
        found_unittest = False
        for line in response.body.split('\n'):
            for item in line.split(','):
                item = item.strip()
                if item=='unittest':
                    found_unittest = True
        
        assert found_unittest