from civicboom.tests import *

from civicboom.lib.database.get_cached import get_member, get_group, get_content, get_membership

from civicboom.model         import Boom, Content, Media, Member, Follow, GroupMembership, Message, Tag, MemberAssignment
from civicboom.model.meta    import Session

from base64 import b64encode, b64decode

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

    def create_content(self, parent_id=None, title=u'Testing delete_cascade', type='article'):
        params={
            '_authentication_token': self.auth_token,
            'title'         : title ,
            'contents'      : u'delete_cascade delete_cascade' ,
            'type'          : type ,
            'tags'          : u'delete_cascade' ,
            'submit_publish': u'publish' ,
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
        assert content_id > 0
        return content_id


    #---------------------------------------------------------------------------
    # Delete User 
    #---------------------------------------------------------------------------
    def test_delete_user(self):
        
        assert self.num_members_public('delete_cascade') == 0
        assert self.num_content_public('delete_cascade') == 0
        
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
        assert self.delete_cascade_member_id > 0
        
        assert self.num_members_public() == num_members_start + 1
        
        # Setup known objects for delete cascade - Create a record in every related table to 'delete_cascade' member
        # when searching through the database after the deletion has occoured there should be NO trace of the string 'delete_cascade' anywhere!
        #  - follow
        #  - messages
        #  - content
        #  - group membership
        
        # Create content with media
        self.png1x1 = b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAAAAAA6fptVAAAAAXNSR0IArs4c6QAAAApJREFUCNdj+AcAAQAA/8I+2MAAAAAASUVORK5CYII=')
        response = self.app.post(
            url('contents', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'title'         : u'Testing delete_cascade' ,
                'contents'      : u'delete_cascade delete_cascade' ,
                'type'          : u'assignment' ,
                'tags'          : u'delete_cascade' ,
                'submit_publish': u'publish' ,
            },
            upload_files = [("media_file", "1x1.png", self.png1x1)],
            status=201
        )
        response_json = json.loads(response.body)
        self.content_id = int(response_json['data']['id'])
        assert self.content_id > 0
        response      = self.app.get(url('content', id=self.content_id, format='json'), status=200)
        response_json = json.loads(response.body)
        self.media_id = response_json['data']['content']['attachments'][0]['id']
        assert self.media_id   > 0



        
        # record current number of
        response      = self.app.get(url('member', id='unittest', format='json'), status=200)
        response_json = json.loads(response.body)
        num_following      = response_json['data']['following']['count']
        num_followers      = response_json['data']['followers']['count']
        num_boomed_content = response_json['data']['boomed_content']['count']
        #num_sent_messages =
        
        # Following, message recive, boom, comment
        self.log_in_as('unittest')
        self.follow('delete_cascade')
        self.send_member_message('delete_cascade', 'testing delete_cascade', 'this message should never be seen as it part of the delete_cascade test')
        self.boom_content(self.content_id)
        self.comment(self.content_id, 'delete_cascade comment')
        
        # Follow, message send, comment
        self.log_in_as('delete_cascade')
        self.follow('unittest')
        self.send_member_message('unittest', 'testing delete_cascade', 'this message should never be seen as it part of the delete_cascade test')
        self.comment(self.content_id, 'delete_cascade comment')
        
        response      = self.app.get(url('member', id='unittest', format='json'), status=200)
        response_json = json.loads(response.body)
        assert num_following      + 1 == response_json['data']['following'     ]['count']
        assert num_followers      + 1 == response_json['data']['followers'     ]['count']
        assert num_boomed_content + 1 == response_json['data']['boomed_content']['count']
        
        
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
        assert self.group_id > 0
        
        #-----------------------------------------------------------------------
        # Step 2: check data is in database
        #-----------------------------------------------------------------------
        # check tables deeply for all instances of the member id for removal
        
        assert self.num_members_public('delete_cascade') == 2 # 'delete_cascade' and 'delete_cascade_group'
        assert self.num_content_public('delete_cascade') == 1 # 'delete_cascade' in public content
        
        assert Session.query(Media          ).filter_by(         id = self.media_id                ).count() == 1
        assert Session.query(Content        ).filter_by(         id = self.content_id              ).count() == 1
        assert Session.query(Content        ).filter_by(  parent_id = self.content_id              ).count() == 2
        assert Session.query(Boom           ).filter_by( content_id = self.content_id              ).count() == 1
        
        assert Session.query(Member         ).filter_by(         id = self.delete_cascade_member_id).count() == 1
        #assert Session.query(Boom           ).filter_by(  member_id = self.delete_cascade_member_id).count() == 1 # The boom didnt come from the member 'delete_cascade'
        assert Session.query(GroupMembership).filter_by(  member_id = self.delete_cascade_member_id).count() == 1
        assert Session.query(Follow         ).filter_by(  member_id = self.delete_cascade_member_id).count() == 1
        assert Session.query(Follow         ).filter_by(follower_id = self.delete_cascade_member_id).count() == 1
        
        #assert Session.query(Message        ).filter_by(  target_id = self.delete_cascade_member_id).count() == 1 # cant == 1 as notifications are generated and it is more than 1
        assert Session.query(Message        ).filter_by(  source_id = self.delete_cascade_member_id).count() == 1
        
        assert Session.query(Tag            ).filter_by(       name = 'delete_cascade'             ).count() == 1
        
        #-----------------------------------------------------------------------
        # Step 3: Delete objects
        #-----------------------------------------------------------------------
        
        member_delete_cascade = get_member('delete_cascade')
        member_delete_cascade.delete()
        
        group_delete_cascade = get_group('delete_cascade_group')
        assert group_delete_cascade.num_members == 0
        group_delete_cascade.delete()
        
        #-----------------------------------------------------------------------
        # Step 4: Check for successful removal
        #-----------------------------------------------------------------------
        
        assert self.num_members_public('delete_cascade') == 0
        assert self.num_content_public('delete_cascade') == 0
        assert num_members_start == self.num_members_public()
        assert num_content_start == self.num_content_public()
        
        # check current number of
        response      = self.app.get(url('member', id='unittest', format='json'), status=200)
        response_json = json.loads(response.body)
        assert num_following      == response_json['data']['following']['count']
        assert num_followers      == response_json['data']['followers']['count']
        assert num_boomed_content == response_json['data']['boomed_content']['count']
        
        # check tables deeply for all instances of the member id for removal
        assert Session.query(Media          ).filter_by(         id = self.media_id                ).count() == 0
        assert Session.query(Content        ).filter_by(         id = self.content_id              ).count() == 0
        assert Session.query(Content        ).filter_by(  parent_id = self.content_id              ).count() == 0
        assert Session.query(Boom           ).filter_by( content_id = self.content_id              ).count() == 0
        
        assert Session.query(Member         ).filter_by(         id = self.delete_cascade_member_id).count() == 0        
        assert Session.query(Boom           ).filter_by(  member_id = self.delete_cascade_member_id).count() == 0
        assert Session.query(GroupMembership).filter_by(  member_id = self.delete_cascade_member_id).count() == 0
        assert Session.query(Follow         ).filter_by(  member_id = self.delete_cascade_member_id).count() == 0
        assert Session.query(Follow         ).filter_by(follower_id = self.delete_cascade_member_id).count() == 0
        
        assert Session.query(Message        ).filter_by(  target_id = self.delete_cascade_member_id).count() == 0
        assert Session.query(Message        ).filter_by(  source_id = self.delete_cascade_member_id).count() == 0
        
        assert Session.query(Tag            ).filter_by(       name = 'delete_cascade'             ).count() == 1 #Tag remains at the end, this could be tidyed witha  delete orphan cascade
        
        
    #---------------------------------------------------------------------------
    # Delete Content
    #---------------------------------------------------------------------------
    def test_delete_content(self):
        
        assert self.num_content_public('delete_cascade') == 0
        num_content_start = self.num_content_public()
        
        # Step 1: Create content
        self.content_id = self.create_content(type='assignment')
        
        # Step 2: Create responses, comments and accept
        self.log_in_as('unitfriend')
        response_1_id = self.create_content(self.content_id, 'response 1')
        response_2_id = self.create_content(self.content_id, 'response 2')
        self.comment(  self.content_id, 'delete_cascade comment')
        self.comment(    response_1_id, 'delete_cascade response comment')
        
        response = self.app.post( # Accept assignment
            url('content_action', action='accept', id=self.content_id, format='json') ,
            params = {'_authentication_token': self.auth_token,} ,
            status = 200
        )
        
        response      = self.app.get(url('content', id=self.content_id, format='json'), status=200)
        response_json = json.loads(response.body)
        assert response_json['data']['responses']['count'] == 2
        assert response_json['data']['comments' ]['count'] == 1
        assert response_json['data']['accepted_status']['count'] == 1
        
        # Step 3: Delete content
        content_delete_cascade = get_content(self.content_id)
        content_delete_cascade.delete()
        
        # Step 4: Check deleted
        response      = self.app.get(url('content', id=response_1_id, format='json'), status=200)
        assert 'delete_cascade response comment' in response
        response      = self.app.get(url('content', id=response_2_id, format='json'), status=200)
        
        assert Session.query(Content         ).filter_by(  parent_id = self.content_id              ).count() == 0
        assert Session.query(Tag             ).filter_by(       name = 'delete_cascade'             ).count() == 1 #Tag remains at the end, this could be tidyed witha  delete orphan cascade
        assert Session.query(MemberAssignment).filter_by( content_id = self.content_id              ).count() == 0
        
