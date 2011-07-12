from civicboom.tests import *
from pylons import config
from random import random

#import json


class TestListsController(TestController):

    def test_lists(self):
        """
        Create a large number of articles and members to test list functionality
        """
        def create_content(title):
            response = self.app.post(
                url('contents', format='json'),
                params={
                    '_authentication_token': self.auth_token,
                    'title'         : title      ,
                    'contents'      : title      ,
                    'type'          : u'article' ,
                    'submit_publish': u'publish' ,
                    'location'      : '%f %f' % (1+random(), 51+random()),
                },
                status=201
            )
            response_json = json.loads(response.body)
            id = int(response_json['data']['id'])
            self.assertNotEqual(id, 0)
            return id
        
        def create_member(name, salt):
            self.sign_up_as(name)
            response = self.app.post(
                url('setting',id="me",format="frag"),
                params={
                    '_method': 'PUT',
                    '_authentication_token': self.auth_token,
                },
                upload_files = [("avatar", "3x3.png", self.generate_image((3, 3), 100+salt))],
                status=200
            )
            self.follow('unittest')
        
        # make sure to overflow all limits
        limits = [
            config['search.default.limit.members'],
            config['search.default.limit.contents']
        ]
        for count in range(max(limits) + 1):
            create_member('list_member_%s' % count, count)
            create_content('list_content_%s' % count)
