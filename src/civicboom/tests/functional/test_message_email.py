from civicboom.tests import *


class TestMessageEmail(TestController):
    
    def test_send_message(self):
        
        self.log_in_as('unitfriend')
        message_list = self.get_messages()['list']
        num_messages = message_list['count']
        
        num_emails = getNumEmails()
        
        self.log_in_as('unittest')
        self.send_member_message('unitfriend', subject='message_email_test', content='xyz')
        
        self.log_in_as('unitfriend')
        
        # Check message
        message_list = self.get_messages()['list']
        message      = message_list['items'][0]
        self.assertEquals(message_list['count'], num_messages + 1             )
        self.assertIn    ('message_email_test' , message['subject']           )
        self.assertIn    ('xyz'                , message['content']           )
        self.assertEquals('unittest'           , message['source']['username'])
        
        # Check email
        self.assertEquals(getNumEmails(), num_emails + 1)
        email = getLastEmail()
        self.assertIn('message_email_test', email.subject     )
        self.assertIn('xyz'               , email.content_text)
        self.assertIn('xyz'               , email.content_html)
        self.assertIn('unittest'          , email.content_html)
    
    
    def test_send_message_multiple_recipients(self):
        num_messages = self.getNumMessagesInDB()
        num_emails   = getNumEmails()
        
        self.send_member_message('unitfriend,kitten, puppy,    bunny,  ', subject='message_email_test', content='zyx')
        
        self.assertEquals(self.getNumMessagesInDB(), num_messages + 4)
        self.assertEquals(getNumEmails()           , num_emails   + 4)
        
        for message in self.getMessagesFromDB(limit=4):
            self.assertEquals(message.content, u'zyx')
