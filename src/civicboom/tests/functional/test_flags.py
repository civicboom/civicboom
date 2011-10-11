from civicboom.tests import *

from pylons import config

from civicboom.model.meta import Session
from civicboom.model import FlaggedEntity

class TestFlagContentController(TestController):

    #---------------------------------------------------------------------------
    # Flag then Deflag Content
    #---------------------------------------------------------------------------
    def test_flag_deflag_content(self):
        """
        create content
        unitfriend login
        flag
        admin login
        check email generated
        deflag content
        """
        # Create content as unittest
        content_id = self.create_content(title='Flag Test', content='This is naughty stuff that somebody should flag')
        
        num_emails = getNumEmails()
        
        # Flag content as unitfirned
        self.log_in_as('unitfriend')
        response = self.app.post(
            url('content_action', action='flag', id=content_id, format='json') ,
            params = {
                '_authentication_token': self.auth_token,
                'type'    : 'offensive'   ,
                'comment' : 'ban this despicable filth',
            } ,
        )
        
        # Check correct email was sent to moderator
        self.assertEqual(getNumEmails(), num_emails + 1)
        email_response = getLastEmail()
        self.assertEquals(email_response.email_to, config['email.moderator'])
        self.assertIn('ban this despicable filth', email_response.content_text)
        
        #TODO - deflag content - the moderator says it's fine
        
        self.log_in_as('unittest')
        self.delete_content(content_id)

    #---------------------------------------------------------------------------
    # Flag then take offline Content
    #---------------------------------------------------------------------------
    def test_flag_disable_content(self):
        """
        create content
        new user log in
        flag
        admin login
        check email generated
        take content offline
        """
        pass


    #---------------------------------------------------------------------------
    # Test Profanity Filter
    #---------------------------------------------------------------------------
    def test_flag_content_profanity(self):
        """
        create content with 'naughty words'
        check alert sent
        on admin pannel
        admin take offline
        """
        
        ## We must be online to use cydyn profanity filter
        ## Check system is online - return success if not connected
        #try:
        #    import urllib2
        #    w = urllib2.urlopen('http://www.python.org/', timeout=10).read()
        #    if not w:
        #        return
        #except:
        #    return
        ## reguargless of online flag - we need to enable set the following settings for the profanity folter to trigger - these will be reverted later
        #config_online           = config['online']
        #self.config_var('online'                  , True)
        config_profanity_filter = config['feature.profanity_filter']
        self.config_var('feature.profanity_filter', True)
        
        
        # Check email is sent to moderator in config
        content_id = self.create_content(title='Profanity Test', content='this content is testing the profanity checker, so, without further ado, cock shit bollox slut monkey badger moose slag wanker nigle rob shytalk')
        
        response      = self.app.get(url('content', id=content_id, format="json"))
        response_json = json.loads(response.body)
        content = response_json['data']['content']['content']
        self.assertNotIn('cock'  , content)
        self.assertNotIn('bollox', content)
        self.assertNotIn('slag'  , content)
        self.assertIn('[Explicit]', content)
        self.assertIn('monkey', content)
        self.assertIn('nigle' , content)
        
        email_response = getLastEmail(to=config['email.moderator'])
        self.assertIn('profanity_filter', email_response.content_text)
        self.assertIn('cock'            , email_response.content_text)
        self.assertIn('bollox'          , email_response.content_text)
        self.assertIn('slag'            , email_response.content_text)
        
        # my god this content is dispcable, take it offline
        # set to content invisible
        # TODO
        
        
        self.log_in_as('unittest')
        self.delete_content(content_id)
        
        # Set config vars back to origninal settings
        #config_var('online'                  , config_online          )
        self.config_var('feature.profanity_filter', config_profanity_filter)


    #---------------------------------------------------------------------------
    # Test Member Flaging
    #---------------------------------------------------------------------------
    def test_flag_member(self):
        self.sign_up_as('spam_man')
        
        self.log_in_as('unittest')
        
        num_emails = getNumEmails()
        
        response = self.app.post(
            url('member_action', action='flag', id='spam_man', format='json') ,
            params = {
                '_authentication_token': self.auth_token,
                'type'    : 'spam'                      ,
                'comment' : 'This member says they are bulgarian royaly and wants my account details. I think not.' ,
            } ,
        )
        
        self.assertEqual(getNumEmails(), num_emails + 1)
        email_response = getLastEmail()
        self.assertEquals(email_response.email_to, config['email.moderator'])
        self.assertIn('wants my account details', email_response.content_text)
        
        self.assertEquals(Session.query(FlaggedEntity).filter(FlaggedEntity.raising_member_id=='unittest').filter(FlaggedEntity.offending_member_id=='spam_man').count(), 1)
        
        # AllanC - TODO - follow the whole flow though?
        
        self.delete_member('spam_man')
        # Double check delete cascade
        self.assertEquals(Session.query(FlaggedEntity).filter(FlaggedEntity.raising_member_id=='unittest').filter(FlaggedEntity.offending_member_id=='spam_man').count(), 0)
        
    #---------------------------------------------------------------------------
    # Test Message Flaging
    #---------------------------------------------------------------------------
    def test_flag_message(self):
        
        
        
        self.send_member_message('unitfriend', subject='You smell', content='I hate you')
        
        self.log_in_as('unitfriend')
        
        message = self.get_messages()['list']['items'][0]
        self.assertIn('hate you', message['content'])
        
        num_emails = getNumEmails()
        response = self.app.post(
            url('message_action', action='flag', id=message['id'], format='json') ,
            params = {
                '_authentication_token': self.auth_token,
                'type'    : 'offensive',
                'comment' : 'They said they hated me, and I smell ... sniff' ,
            } ,
        )
        
        self.assertEqual(getNumEmails(), num_emails + 1)
        email_response = getLastEmail()
        self.assertEquals(email_response.email_to, config['email.moderator'])
        self.assertIn('They said', email_response.content_text)
        
        # Get raised flag from DB, will error on fail, then delete/cleanup
        flag = Session.query(FlaggedEntity).filter(FlaggedEntity.raising_member_id=='unitfriend').filter(FlaggedEntity.offending_message_id==message['id']).one()
        Session.delete(flag)
        
        self.delete_message(message['id'])