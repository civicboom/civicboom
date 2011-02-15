from civicboom.tests import *

from base64 import b64encode, b64decode

import logging
log = logging.getLogger(__name__)


class TestDeleteCascadesController(TestController):

    def num_members_public(self):
        response      = self.app.get(url('members', format='json'), status=200)
        response_json = json.loads(response.body)
        return response_json['data']['list']['count']
    
    def num_content_public(self):
        response      = self.app.get(url('contents', format='json'), status=200)
        response_json = json.loads(response.body)
        return response_json['data']['list']['count']

    #---------------------------------------------------------------------------
    # Delete User 
    #---------------------------------------------------------------------------
    def test_delete_user(self):
        num_members_start = self.num_members_public()
        num_content_start = self.num_content_public()
        
        # Create user
        self.sign_up_as('delete_cascade')
        assert self.num_members_public() == num_members_start + 1
        
        # Create a record in every related table to member
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
                'title'         : u'Testing delete_cascade',
                'contents'      : u'delete_cascade delete_cascade' ,
                'type'          : u'article' ,
                'submit_publish': u'publish' ,
            },
            upload_files = [("media_file", "1x1.png", self.png1x1)],
            status=201
        )
        response_json = json.loads(response.body)
        self.content_id = int(response_json['data']['id'])
        assert self.content_id > 0
        
        # Follow, message send, comment
        self.follow('unittest')
        self.send_member_message('unittest', 'testing delete_cascade', 'this message should never be seen as it part of the delete_cascade test')
        self.comment(self.content_id, 'delete_cascade')
        
        # Following, message recive, boom, comment
        self.log_in_as('unittest')
        self.follow('delete_cascade')
        self.send_member_message('delete_cascade', 'testing delete_cascade', 'this message should never be seen as it part of the delete_cascade test')
        self.boom_content(self.content_id)
        self.comment(self.content_id, 'delete_cascade')
        self.log_in_as('delete_cascade')
        

        # Create comment
        # Boom
        # Create group - and therefor become a member
        

