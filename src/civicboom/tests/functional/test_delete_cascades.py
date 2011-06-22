from civicboom.tests import *

from civicboom.lib.database.get_cached import get_member, get_group, get_content, get_membership

from civicboom.model         import Boom, Content, Media, Member, Follow, GroupMembership, Message, Tag, MemberAssignment, PaymentAccount
from civicboom.model.meta    import Session

import logging
log = logging.getLogger(__name__)


class TestDeleteCascadesController(TestController):
    
    def get_list_count(self, url_index):
        response      = self.app.get(url_index, status=200)
        response_json = json.loads(response.body)
        return response_json['data']['list']['count']

    def num_members_public(self, term=None):
        url_index = url('members', format='json')
        if term:
            url_index = url('members', format='json', term=term)
        return self.get_list_count(url_index)
    
    def num_content_public(self, term=None):
        url_index = url('contents', format='json')
        if term:
            url_index = url('contents', format='json', term=term)
        return self.get_list_count(url_index)

    # AllanC - TODO! this should put in default params to use __init__.create_content but cant get it working right now
    #          see remmed out ideas below
    def create_content(self, parent_id=None, title=u'Testing delete_cascade', content=u'delete_cascade delete_cascade', type='article', tags=u'delete_cascade'):
        #def create_content(self, **kwargs):
        #    if 'title' not in kwargs:
        #        kwargs['title'] = u'Testing delete_cascade'
        #    if 'content' not in kwargs:
        #        kwargs['content'] = u'delete_cascade delete_cascade'
        #    super(TestDeleteCascadesController,self).create_content(**kwargs)
        
        params={
            '_authentication_token': self.auth_token,
            'title'         : title ,
            'contents'      : content ,
            'type'          : type ,
            'tags_string'   : tags ,
            #'submit_publish': u'publish' ,
        }
        if parent_id:
            params.update({'parent_id':parent_id})
        
        response = self.app.post(
            url('contents', format='json') ,
            params = params ,
            status = 201 ,
        )
        response_json = json.loads(response.body)
        content_id = int(response_json['data']['id'])
        self.assertNotEqual(content_id, 0)
        return content_id


    #---------------------------------------------------------------------------
    # Delete User
    #---------------------------------------------------------------------------
    def test_delete_user(self):
        
        self.assertEqual(self.num_members_public('delete_cascade'), 0)
        self.assertEqual(self.num_content_public('delete_cascade'), 0)
        
        num_members_start = self.num_members_public()
        num_content_start = self.num_content_public()
        
        #-----------------------------------------------------------------------
        # Step 1: Create a set of interlinked objects over a range of tables to test delete cascades
        #-----------------------------------------------------------------------
        
        # Create user
        self.sign_up_as('delete_cascade')
        
        response      = self.app.get(url('member', id='delete_cascade', format='json'), status=200)
        response_json = json.loads(response.body)
        self.delete_cascade_member_id = response_json['data']['member']['id']
        self.assertNotEqual(self.delete_cascade_member_id, 0)
        
        self.assertEqual(self.num_members_public(), num_members_start + 1)
        
        # Setup known objects for delete cascade - Create a record in every related table to 'delete_cascade' member
        # when searching through the database after the deletion has occoured there should be NO trace of the string 'delete_cascade' anywhere!
        #  - follow
        #  - messages
        #  - content
        #  - group membership
        
        # Create content with media
        self.png1x1 = self.generate_image((1, 1))
        response = self.app.post(
            url('contents', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'title'         : u'Testing delete_cascade' ,
                'contents'      : u'delete_cascade delete_cascade' ,
                'type'          : u'assignment' ,
                'tags_string'   : u'delete_cascade' ,
                #'submit_publish': u'publish' ,
            },
            upload_files = [("media_file", "1x1.png", self.png1x1)],
            status=201
        )
        response_json = json.loads(response.body)
        self.content_id = int(response_json['data']['id'])
        self.assertNotEqual(self.content_id, 0)
        response      = self.app.get(url('content', id=self.content_id, format='json'), status=200)
        response_json = json.loads(response.body)
        self.media_id = response_json['data']['content']['attachments'][0]['id']
        self.assertNotEqual(self.media_id  , 0)



        
        # record current number of
        response      = self.app.get(url('member', id='unittest', format='json'), status=200)
        response_json = json.loads(response.body)
        num_following      = response_json['data']['following']['count']
        num_followers      = response_json['data']['followers']['count']
        num_boomed_content = response_json['data']['boomed'   ]['count']
        #num_sent_messages =
        
        # Following, message recive, boom, comment
        self.log_in_as('unittest')
        self.follow('delete_cascade')
        self.send_member_message('delete_cascade', 'testing delete_cascade', 'this message should never be seen as it part of the delete_cascade test')
        self.boom_content(self.content_id)
        self.comment(self.content_id, 'delete_cascade comment')
        unittest_assingment_id = self.create_content(type='assignment', title='assignment', content='assignment')
        
        # Follow, message send, comment
        self.log_in_as('delete_cascade')
        self.follow('unittest')
        self.send_member_message('unittest', 'testing delete_cascade', 'this message should never be seen as it part of the delete_cascade test')
        self.comment(self.content_id, 'delete_cascade comment')
        # TODO: accept assignment by unittest
        self.accept_assignment(unittest_assingment_id)
        self.withdraw_assignment(unittest_assingment_id)
        
        response      = self.app.get(url('member', id='unittest', format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertEqual(num_following      + 1, response_json['data']['following']['count'])
        self.assertEqual(num_followers      + 1, response_json['data']['followers']['count'])
        self.assertEqual(num_boomed_content + 1, response_json['data']['boomed'   ]['count'])
        
        
        # Create group - and therefor become a member
        response = self.app.post(
            url('groups', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'username'     : 'delete_cascade_group',
                'name'         : 'Test group for delete_cascade' ,
                'description'  : 'This group should not be visible once the tests have completed because it will be removed' ,
                'default_role'              : 'admin'  ,
                'join_mode'                 : 'public' ,
                'member_visibility'         : 'public' ,
                'default_content_visibility': 'public' ,
            },
            status=201
        )
        response_json = json.loads(response.body)
        self.group_id = int(response_json['data']['id'])
        self.assertNotEqual(self.group_id, 0)
        
        self.set_account_type('plus') # Create an account record associated with this user
        self.delete_cascade_payment_account_id = Session.query(Member).filter_by(id = self.delete_cascade_member_id).one().payment_account_id # Get payment account id
        
        
        #-----------------------------------------------------------------------
        # Step 2: check data is in database
        #-----------------------------------------------------------------------
        # check tables deeply for all instances of the member id for removal
        
        self.assertEqual(self.num_members_public('delete_cascade'), 2) # 'delete_cascade' and 'delete_cascade_group'
        self.assertEqual(self.num_content_public('delete_cascade'), 1) # 'delete_cascade' in public content # unittest assignment has delete cascade in title and content
        
        self.assertEqual(Session.query(Media           ).filter_by(         id = self.media_id                ).count(), 1)
        self.assertEqual(Session.query(Content         ).filter_by(         id = self.content_id              ).count(), 1)
        self.assertEqual(Session.query(Content         ).filter_by(  parent_id = self.content_id              ).count(), 2)
        self.assertEqual(Session.query(Boom            ).filter_by( content_id = self.content_id              ).count(), 1)
        
        self.assertEqual(Session.query(Member          ).filter_by(         id = self.delete_cascade_member_id).count(), 1)
        #self.assertEqual(Session.query(Boom            ).filter_by(  member_id = self.delete_cascade_member_id).count(), 1) # The boom didnt come from the member 'delete_cascade'
        self.assertEqual(Session.query(GroupMembership ).filter_by(  member_id = self.delete_cascade_member_id).count(), 1)
        self.assertEqual(Session.query(Follow          ).filter_by(  member_id = self.delete_cascade_member_id).count(), 1)
        self.assertEqual(Session.query(Follow          ).filter_by(follower_id = self.delete_cascade_member_id).count(), 1)
        self.assertEqual(Session.query(MemberAssignment).filter_by(  member_id = self.delete_cascade_member_id).count(), 1)
        
        #self.assertEqual(Session.query(Message         ).filter_by(  target_id = self.delete_cascade_member_id).count() == 1) # cant, 1 as notifications are generated and it is more than 1
        self.assertEqual(Session.query(Message         ).filter_by(  source_id = self.delete_cascade_member_id).count(), 1)
        
        self.assertEqual(Session.query(Tag             ).filter_by(       name = u'delete_cascade'            ).count(), 1)
        
        self.assertEqual(Session.query(Member          ).filter_by(payment_account_id = self.delete_cascade_payment_account_id).count(), 1)
        
        
        #-----------------------------------------------------------------------
        # Step 3: Delete objects
        #-----------------------------------------------------------------------
        
        member_delete_cascade = get_member('delete_cascade')
        member_delete_cascade.delete()
        
        group_delete_cascade = get_group('delete_cascade_group')
        self.assertEqual(group_delete_cascade.num_members, 0)
        group_delete_cascade.delete()
        
        #-----------------------------------------------------------------------
        # Step 4: Check for successful removal
        #-----------------------------------------------------------------------
        
        self.assertEqual(self.num_members_public('delete_cascade'), 0)
        self.assertEqual(self.num_content_public('delete_cascade'), 0)
        self.assertEqual(num_members_start, self.num_members_public())
        self.assertEqual(num_content_start, self.num_content_public() - 1) # -1 because unittest set an assignment
        
        # check current number of
        response      = self.app.get(url('member', id='unittest', format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertEqual(num_following     , response_json['data']['following']['count'])
        self.assertEqual(num_followers     , response_json['data']['followers']['count'])
        self.assertEqual(num_boomed_content, response_json['data']['boomed'   ]['count'])
        
        # check tables deeply for all instances of the member id for removal
        self.assertEqual(Session.query(Media           ).filter_by(         id = self.media_id                ).count(), 0)
        self.assertEqual(Session.query(Content         ).filter_by(         id = self.content_id              ).count(), 0)
        self.assertEqual(Session.query(Content         ).filter_by(  parent_id = self.content_id              ).count(), 0)
        self.assertEqual(Session.query(Boom            ).filter_by( content_id = self.content_id              ).count(), 0)
        
        self.assertEqual(Session.query(Member          ).filter_by(         id = self.delete_cascade_member_id).count(), 0)
        self.assertEqual(Session.query(Boom            ).filter_by(  member_id = self.delete_cascade_member_id).count(), 0)
        self.assertEqual(Session.query(GroupMembership ).filter_by(  member_id = self.delete_cascade_member_id).count(), 0)
        self.assertEqual(Session.query(Follow          ).filter_by(  member_id = self.delete_cascade_member_id).count(), 0)
        self.assertEqual(Session.query(Follow          ).filter_by(follower_id = self.delete_cascade_member_id).count(), 0)
        self.assertEqual(Session.query(MemberAssignment).filter_by(  member_id = self.delete_cascade_member_id).count(), 0)
        
        self.assertEqual(Session.query(Message         ).filter_by(  target_id = self.delete_cascade_member_id).count(), 0)
        self.assertEqual(Session.query(Message         ).filter_by(  source_id = self.delete_cascade_member_id).count(), 0)
        
        self.assertEqual(Session.query(Tag             ).filter_by(       name = u'delete_cascade'            ).count(), 1) #Tag remains at the end, this could be tidyed witha  delete orphan cascade
        
        self.assertEqual(Session.query(Member          ).filter_by(payment_account_id = self.delete_cascade_payment_account_id).count(), 0)
        self.assertEqual(Session.query(PaymentAccount  ).filter_by(                id = self.delete_cascade_payment_account_id).count(), 1) # The cascade dose not remove the payment account
        
        # Step 5: cleanup
        unittest_assignment = get_content(unittest_assingment_id)
        unittest_assignment.delete()
        
        
    #---------------------------------------------------------------------------
    # Delete Content
    #---------------------------------------------------------------------------
    def test_delete_content(self):
        
        self.assertEqual(self.num_content_public('delete_cascade'), 0)
        num_content_start = self.num_content_public()
        
        # Step 1: Create content
        self.content_id = self.create_content(type='assignment')
        
        # Step 2: Create responses, comments and accept
        self.log_in_as('unitfriend')
        #self.accept_assignment(self.content_id) # Accepting should now be done automatically when responding
        response_1_id = self.create_content(parent_id=self.content_id, title='response 1', content='delete_cascade')
        response_2_id = self.create_content(parent_id=self.content_id, title='response 2', content='delete_cascade')
        self.comment(  self.content_id, 'delete_cascade comment')
        self.comment(    response_1_id, 'delete_cascade response comment')
        
        response      = self.app.get(url('content', id=self.content_id, format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertEqual(response_json['data']['responses']['count'], 2)
        self.assertEqual(response_json['data']['comments' ]['count'], 1)
        self.assertEqual(response_json['data']['accepted_status']['count'], 1)
        
        # Step 3: Delete content
        content_delete_cascade = get_content(self.content_id)
        content_delete_cascade.delete()
        
        # Step 4: Check deleted
        response      = self.app.get(url('content', id=response_1_id, format='json'), status=200)
        self.assertIn('delete_cascade response comment', response)
        response      = self.app.get(url('content', id=response_2_id, format='json'), status=200)
        
        self.assertEqual(Session.query(Content         ).filter_by(  parent_id = self.content_id              ).count(), 0)
        self.assertEqual(Session.query(Tag             ).filter_by(       name = u'delete_cascade'            ).count(), 1) #Tag remains at the end, this could be tidyed witha  delete orphan cascade
        self.assertEqual(Session.query(MemberAssignment).filter_by( content_id = self.content_id              ).count(), 0)
