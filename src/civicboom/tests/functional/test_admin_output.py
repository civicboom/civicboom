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
