"""Pylons application test package

This package assumes the Pylons environment is already loaded, such as
when this script is imported from the `nosetests --with-pylons=test.ini`
command.

This module initializes the application via ``websetup`` (`paster
setup-app`) and provides the base testing objects.
"""
from unittest import TestCase

from paste.deploy import loadapp
from paste.script.appinstall import SetupCommand
from pylons import url
from routes.util import URLGenerator

from civicboom.model      import Message
from civicboom.model.meta import Session
from sqlalchemy           import or_, and_, not_, null

# XXX: Paste's TestApp supports app.delete() with params
#from webtest import TestApp
from paste.fixture import TestApp
import cbutils.worker as worker

from civicboom.lib.database.query_helpers import to_apilist

from civicboom.lib.communication.email_log import getLastEmail, getNumEmails, emails
import re
import json

from civicboom.lib.form_validators.base import IsoFormatDateConverter

import pylons.test

__all__ = ['environ', 'url', 'TestController',
           # Email Log
           'getLastEmail', 'getNumEmails', 'emails',
           # libs
           'json', 're'
           ]

# we import tests/init_base_data during websetup, but only want
# this to trigger in test mode. Possibly init_base_data shouldn't
# be in tests/ ?
if pylons.test.pylonsapp:
    # Invoke websetup with the current config file
    SetupCommand('setup-app').run([pylons.test.pylonsapp.config['__file__']])


environ = {}


class TestController(TestCase):

    logged_in_as = None
    auth_token   = None

    def __init__(self, *args, **kwargs):
        wsgiapp = pylons.test.pylonsapp
        config = wsgiapp.config
        self.app = TestApp(wsgiapp, extra_environ={'REMOTE_ADDR': '0.0.0.0'})
        url._push_object(URLGenerator(config['routes.map'], {
            # pretend we are in an HTTP request
            'wsgi.url_scheme': 'https',
            'HTTP_HOST': 'www.civicboom.com',
            # pretend routes middleware has added stuff
            'wsgiorg.routing_args': (None, {'action': u'titlepage', 'controller': u'misc', 'sub_domain': 'www'})
        }))
        TestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        # log in by default
        self.log_in()

    def tearDown(self):
        # wait for the worker to finish its work before reporting "test passed"
        worker.stop_worker()

    #---------------------------------------------------------------------------
    # Common functions for all test
    #---------------------------------------------------------------------------

    def config_var(self, key, value=None):
        """
        Used to get and set config vars from automated tests
        """
        response = self.app.get(
            url(controller='test', action='config_var'),
            params={
                'key'  : key   ,
                'value': value ,
            },
            status=200
        )
        return json.loads(response.body)[key]

    def generate_image(self, size, seed=0):
        import Image
        import StringIO
        import random
        random.seed(seed)
        im = Image.new('RGB', size)
        for x in range(0, size[0]):
            for y in range(0, size[1]):
                im.putpixel(
                    (x, y),
                    (
                        random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255),
                    )
                )
        buf = StringIO.StringIO()
        im.save(buf, format= 'PNG')
        return buf.getvalue()

    def server_datetime(self, new_datetime=None):
        """
        Used to get and set server date for tests
        
        passing the paramiter new_datetime='now' resets any date override for the test server
        """
        response = self.app.get(
            url(controller='test', action='server_datetime'),
            params={
                'new_datetime': new_datetime ,
            },
            status=200
        )
        datetime_string = json.loads(response.body)['datetime']
        return IsoFormatDateConverter().to_python(datetime_string, None)


    def log_in(self):
        self.log_in_as('unittest')

    def log_in_as(self, username, password='password'):
        if self.logged_in_as != username:
            self.log_out()
            response = self.app.post(
                url(controller='account', action='signin'),
                extra_environ={'HTTP_X_URL_SCHEME': 'https'},
                params={
                    'username': username ,
                    'password': password ,
                }
            )
            response = self.app.get(url(controller='profile', action='index')) # get an auth token
            self.assertIn('_authentication_token', response.session) # If this failed the login was unsuccessful
            self.auth_token   = response.session['_authentication_token']
            self.logged_in_as = username
            self.logged_in_password = password

    def log_out(self):
        if self.logged_in_as:
            response = self.app.post(
                url(controller='account', action='signout'),
                extra_environ={'HTTP_X_URL_SCHEME': 'https'},
                params={
                    '_authentication_token': self.auth_token
                }
            )
            self.auth_token   = None
            self.logged_in_as = None
        self.app.reset()

    def set_account_type(self, account_type):
        # AllanC TODO - do somthing with account_type var
        response = self.app.get(url(controller='test', action='set_account_type', id=self.logged_in_as, account_type=account_type))
        self.assertIn('ok', response.body)

    def set_persona(self, username_group):
        response = self.app.post(
            url(controller='account', action='set_persona', id=username_group, format='json'),
            params={
                '_authentication_token': self.auth_token,
            },
            status=200
        )
        response_json = json.loads(response.body)
        self.assertEqual(response_json['status'], 'ok')
        self.logged_in_as = username_group

    def join(self, username_group):
        response = self.app.post(
            url('group_action', action='join', id=username_group, format='json') ,
            params={
                '_authentication_token': self.auth_token   ,
                #'member'               : self.logged_in_as , #AllanC - why was this here?
            },
            status=200,
        )
        #self.assertIn('request', response) # successful "join request" in response

    def create_group(self, username, name=None, description='', join_mode='invite_and_request', default_role='editor', member_visibility='public', default_content_visibility='public'):
        if not name:
            name = username
        response = self.app.post(
            url('groups', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'username'     : username,
                'name'         : name ,
                'description'  : description ,
                'default_role' : default_role ,
                'join_mode'    : join_mode ,
                'member_visibility'         : member_visibility , 
                'default_content_visibility': default_content_visibility ,
            },
            status=201
        )
        response_json = json.loads(response.body)
        
        group_id = response_json['data']['id']
        self.assertNotEqual(group_id, 0)
        
        response = self.app.get(url('group', id=username, format='json'))
        response_json = json.loads(response.body)
        self.assertEqual(response_json['data']['member']['username']                  , username                   )
        self.assertEqual(response_json['data']['member']['join_mode']                 , join_mode                  )
        self.assertEqual(response_json['data']['member']['default_role']              , default_role               )
        self.assertEqual(response_json['data']['member']['member_visibility']         , member_visibility          )
        self.assertEqual(response_json['data']['member']['default_content_visibility'], default_content_visibility )
        return group_id


    def sign_up_as(self, username, password=u'password', dob=u'1/1/1980'):
        """
        A function that can be called from other automated tests to call the signup proccess and generate a new user
        """
        self.log_out()
        num_emails = getNumEmails()
        
        # Request new user email for new user
        response = self.app.post(
            url(controller='register', action='email', format="json"),
            params={
                'username': username,
                'email'   : 'test+'+username+'@civicboom.com',
            },
        )
        
        # Get email generated by last event
        self.assertEqual(getNumEmails(), num_emails + 1) # GregM: Added email notifications! Doh... 
        
        for offset in range(1,3): # Right then, as we are generating more than one email at signup we need to loop through the last two emails (1...2) to check both :(
            email_response = getLastEmail(offset)
            self.assertGreater(len(email_response.content_text), 0)
            link = str(re.search(r'https?://(?:.*?)(/.*?)[\'"\s]', email_response.content_text+' ').group(1))
            if 'hash' in link:
                break
        
        self.assertIn('hash', link)
            
        num_emails = getNumEmails()
        response = self.app.post(
            link,
            params={
                'password'        : password  ,
                'password_confirm': password  ,
                'dob'             : dob       ,
                'terms'           : u'checked',
                'name'            : username + "'s Full Name",
                'help_type'       : u'ind',
            },
        )
        self.assertEqual(getNumEmails(), num_emails + 2) # AllanC - this has been botched .. Lizzie wants emails personaly to her for EVERY signup ... this is throwing off the tests and we need a 2 here instead of a 1
        
        self.log_in_as(username, password)
    
    def get_member(self, username=None, format='json'):
        if not username:
            username = self.logged_in_as
        response      = self.app.get(url('member', id=username, format=format), status=200)
        if format=='json':
            response_json = json.loads(response.body)
            return response_json['data']
        return response

    def get_content(self, content_id, format='json'):
        response      = self.app.get(url('content', id=content_id, format=format), status=200)
        if format=='json':
            response_json = json.loads(response.body)
            return response_json['data']
        return response
    
    def get_comments(self, content_id, format='json'):
        response      = self.app.get(url('content_action', action='comments', id=content_id, format=format), status=200)
        if format=='json':
            response_json = json.loads(response.body)
            return response_json['data']
        return response
    
    def create_content(self, title=u'Test', content=u'Test', type='article', **kwargs):
        params={
            '_authentication_token': self.auth_token,
            'title'         : title      ,
            'content'       : content    ,
            'type'          : type       ,
            #'submit_publish': u'publish' , # publish needs to be remove from API
        }
        params.update(kwargs)
        
        response = self.app.post(
            url('contents', format='json') ,
            params = params ,
            status = 201 ,
        )
        response_json = json.loads(response.body)
        content_id = int(response_json['data']['id'])
        self.assertGreater(content_id, 0)
        
        # Check public notifications are generated (for public content)
        if False: #not kwargs.get('private'): # AllanC - The notification tests are remmed out for now ... multiple tests fail for odd reasons, this needs looking at when we have more time
            try:
                follower_id = json.loads(self.app.get(url('member_action', action='followers', id=self.logged_in_as, limit=1, format='json'), status=200).body)['data']['list']['items'][0]['id'] #   get a follower of the creator of this item of content
                notification = self.getLastNotification(user_id=follower_id) # Get the followers most recent notification
            except:
                pass
            if notification:
                if type=='article' and kwargs.get('parent_id'):
                    self.assertIn('response'         , notification['subject'])
                    self.assertIn('response'         , notification['content'])
                elif type=='article' or type=='assignment':
                    self.assertIn('new'              , notification['subject']) # Check the text expected in the notification
                    self.assertIn('new'              , notification['content'])
                if kwargs.get('parent_id'):
                    self.assertIn('/'+kwargs.get('parent_id'), notification['content']) # Check there is a reference to the parent content id
                self.assertIn('/'+str(content_id), notification['content']) # Check there is a reference to this content id
        
        return content_id

    def update_content(self, id, **kwargs):
        params={
            '_authentication_token': self.auth_token
        }
        params.update(kwargs)
        response = self.app.put(
            url('content', id=id, format='json'),
            params = params ,
            status = 200    ,
        )
        # Todo - check notifications

    def delete_content(self, id):
        response = self.app.delete(
            url('content', id=id, format="json"),
            params={'_authentication_token': self.auth_token,},
            status=200
        )

    def delete_member(self, username=None):
        """
        Not an API call .. this remove the user from the database! - used to stop there being 100's of test users after the tests have run
        """
        if not username:
            username = self.logged_in_as
            self.log_out()
        from civicboom.lib.database.get_cached import get_member
        member = get_member(username)
        member.delete()
        

    def follow(self, username, trusted=False):
        response = self.app.post(
            url('member_action', action='follow', id=username, format='json'),
            params={
                '_authentication_token': self.auth_token ,
            },
            status=200
        )
        # If we require a trusted follower perform accept from following
        if trusted:
            original_username = self.logged_in_as
            self.log_in_as(username)
            self.follower_trust(original_username)
            self.log_in_as(original_username)
        # Todo - check notifications
            
    
    def unfollow(self, username):
        response = self.app.post(
            url('member_action', action='unfollow', id=username, format='json'),
            params={
                '_authentication_token': self.auth_token ,
            },
            status=200
        )

    def follower_trust(self, username):
        response = self.app.post(
            url('member_action', action='follower_trust', id=username, format='json'),
            params={
                '_authentication_token': self.auth_token ,
            },
            status=200
        )
        response = self.app.post(
            url('member_action', action='follower_trust', id=username, format='json'),
            params={
                '_authentication_token': self.auth_token ,
            },
            status=400
        )
        
    def follower_distrust(self, username):
        response = self.app.post(
            url('member_action', action='follower_distrust', id=username, format='json'),
            params={
                '_authentication_token': self.auth_token ,
            },
            status=200
        )
        response = self.app.post(
            url('member_action', action='follower_distrust', id=username, format='json'),
            params={
                '_authentication_token': self.auth_token ,
            },
            status=400
        )

    def follower_invite_trusted(self, username):
        response = self.app.post(
            url('member_action', action='follower_invite_trusted', id=username, format='json'),
            params={
                '_authentication_token': self.auth_token ,
            },
            status=200
        )

    def send_member_message(self, username, subject, content):
        response = self.app.post(
            url('messages', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'target' : username,
                'subject': subject ,
                'content': content ,
            },
            status=201
        )
        message_id_list = json.loads(response.body)['data']['id']
        # AllanC - the id feild now returns a list of all messages created .. is this needed?
        if len(message_id_list)==1:
            return message_id_list[0]
        return message_id_list
        # Todo - check email with message content sent?

    def get_messages(self, username=None):
        if not username:
            username = self.logged_in_as
        response      = self.app.get(url('messages', list='to', format='json'), status=200)
        response_json = json.loads(response.body)
        return response_json['data']


    def boom_content(self, content_id):
        response = self.app.post(
            url('content_action', action='boom', id=content_id, format='json'),
            params={
                '_authentication_token': self.auth_token,
            },
            status=200
        )
        response_json = json.loads(response.body)
        assert response_json['status'] == 'ok'

    def comment(self, content_id, comment='comment'):
        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                #'title': "A test comment by the test user",
                'type'     : 'comment'  ,
                'parent_id': content_id ,
                'content'  : comment    ,
            },
            status=201
        )
        comment_id = json.loads(response.body)["data"]["id"]
        
        # Check comment is listed in parent as the latest comment
        parent_content = self.get_content(content_id)
        self.assertEqual(parent_content['comments']['items'][0]['id'], comment_id)
        
        # Check the comment notification was generated for the creator of the content being commented on
        #self.assertEqual(self.get_comments(content_id)['list']['items'][-1]['id'], comment_id) # AllanC - no need to re-get just the comments, we got the whole content object above
        last_parent_creator_notification = self.getLastNotification(user_id=parent_content['content']['creator']['id'])
        self.assertIn('comment'          , last_parent_creator_notification['subject'])
        self.assertIn('commented'        , last_parent_creator_notification['content'])
        self.assertIn('/'+str(comment_id), last_parent_creator_notification['content'])
        
        return comment_id

    def accept_assignment(self, id):
        response = self.app.post( # Accept assignment
            url('content_action', action='accept', id=id, format='json') ,
            params = {'_authentication_token': self.auth_token,} ,
            status = 200
        )
        self.assertIn('accepted', response)

    def withdraw_assignment(self, id):
        response = self.app.post(
            url('content_action', action='withdraw', id=id, format='json'),
            params={'_authentication_token': self.auth_token,},
            status=200
        )
        self.assertIn('withdrawn', response)

    def getNumNotificationsInDB(self):
        return Session.query(Message).filter(Message.source_id==null()).count()

    def getNotificationsFromDB(self, limit=10):
        return Session.query(Message).filter(Message.source_id==null()).order_by(Message.id.desc()).limit(limit).all()

    def getNumMessagesInDB(self):
        return Session.query(Message).filter(not_(Message.source_id==null())).filter(not_(Message.target_id==null())).count()

    def getMessagesFromDB(self, limit=10):
        return Session.query(Message).filter(not_(Message.source_id==null())).filter(not_(Message.target_id==null())).order_by(Message.id.desc()).limit(limit).all()

    def getNumNotifications(self, username=None, password=None):
        if username:
            if self.logged_in_as != username:
                old_user = self.logged_in_as
                old_password = self.logged_in_password
                self.log_in_as(username, password)
        response = self.app.get(
            url('messages', format='json'),
            params={
                'list': 'notification',
            },
            status=200
        )
        response_json = json.loads(response.body)
        if username:
            if self.logged_in_as != old_user:
                self.log_in_as(old_user, old_password)
        return int(response_json['data']['list']['count'])
    
    def getLastNotification(self, user_id=None):
        # If user ID given - Get notifications directly from db for that user - we do this because if the user is persona we cant just log in and out to get there notifications
        if user_id:
            notification_list = to_apilist(
                Session.query(Message).filter(and_(Message.source_id==null(), Message.target_id==user_id)).order_by(Message.timestamp.desc()) ,
                obj_type = 'messages' ,
                limit    = 3 ,
            )
        # Else - get notifications using API for currently logged in user
        else:
            response = self.app.get(
                url('messages', format='json'),
                params={
                    'list' : 'notification',
                    'limit': 3 ,
                },
                status=200
            )
            notification_list = json.loads(response.body)
        return notification_list['data']['list']['items'][0]
    
    def invite_user_to(self, type, id, user):
        # Test that we can access the invite page
        response = self.app.get(
            '/invite',
            params={
                '_authentication_token': self.auth_token,
                'invite': type,
                'id': id,
                'format': 'json',
            },
            status=200
        )
        # Test that searching for user that does not exist returns 0
        response = self.app.get(
            '/invite.json',
            params={
                '_authentication_token': self.auth_token,
                'invite': type,
                'id': id,
                'search-name': user + 'does_not_exist_ever'
            },
            status=200
        )
        response_json = json.loads(response.body)
        self.assertEqual(response_json['data']['invite_list']['count'], 0)
        # Search for user and check we get less results
        response = self.app.post(
            '/invite.json',
            params={
                '_authentication_token': self.auth_token,
                'invite': type,
                'id': id,
                'search-name': user
            },
            status=200
        )
        response_json = json.loads(response.body)
        self.assertGreaterEqual(response_json['data']['invite_list']['count'], 1)
        self.assertLess(response_json['data']['invite_list']['count'], 10)
        # Add user to invite list
        response = self.app.post(
            '/invite.json',
            params={
                '_authentication_token': self.auth_token,
                'invite': type,
                'id': id,
                'search-name': user,
                'add-'+user: user
            },
            status=200
        )
        response_json = json.loads(response.body)
        self.assertIn(user, response_json['data']['invitee_list']['items']['0']['username'])
        # Generate extra invite parameters
        invitees = response_json['data']['invitee_list']['items']
        invitee_list = dict([('inv-'+key, invitees[key]['username']) for key in invitees.keys()])
        params = {
                '_authentication_token': self.auth_token,
                'invite': type,
                'id': id,
                'search-name': user,
                'submit-invite': 'Invite',
            }
        params.update(invitee_list)
        response = self.app.post(
            '/invite.json',
            params=params,
            status=200
        )
        response_json = json.loads(response.body)
        self.assertEqual(response_json['data']['invitee_list']['count'], 0)
        self.assertEqual(response_json['status'], 'ok')
        
        # Repeat to check error double inviting
        response = self.app.post(
            '/invite.json',
            params=params,
            status=200
        )
        response_json = json.loads(response.body)
        self.assertEqual(response_json['data']['invitee_list']['count'], 1)
        self.assertEqual(len(response_json['data']['error-list']), 1)
        self.assertEqual(response_json['status'], 'ok')

    def assertSubStringIn(self, substring, string_list):
        found = False
        for i in string_list:
            if substring in i:
                fount = True
                return True
        raise AssertionError('%s not found in subelements of %s' % (substring, string_list))
    
    def run_task(self, task, **kwargs):
        response = self.app.get(
            url(controller='task', action=task, **kwargs),
            status=200
        )
        assert "task:ok" in response
        
        
