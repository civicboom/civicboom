from civicboom.tests import *
from civicboom.model.meta import Session
from civicboom.model import Message, Member
#import json


class TestMessagesController(TestController):
    def test_all(self):
        self.part_setup()

        self.part_new()
        self.part_new_frag()
        self.part_create()
        self.part_create_bad_target()
        self.part_create_no_content()

        self.part_index()
        self.part_index_lists()
        self.part_index_as_json()
        self.part_show()
        self.part_show_as_json()
        self.part_show_someone_elses()
        self.part_show_non_exist()

        self.part_edit()
        self.part_edit_as_json()
        self.part_update()

        self.part_delete_message()
        self.part_delete_notification()
        self.part_delete_someone_elses()
        self.part_delete_non_exist()
        
        #TODO
        # view sent messages
        #  try delete sent
        # view notifications
        # view recived
        # set read


    def part_setup(self):
        # notifications can't be created manually
        n1 = Message()
        n1.target = Session.query(Member).get("unittest")
        n1.subject = u"Notification! A test"
        n1.content = u"A test is happening now :O"

        n2 = Message()
        n2.target = Session.query(Member).get("unitfriend")
        n2.subject = u"Another notification! A test"
        n2.content = u"A test part 2 is happening now :O"

        n3 = Message()
        n3.target = Session.query(Member).get("unittest")
        n3.subject = u"deleteme"
        n3.content = u"This is a notification to test deletion with"

        Session.add_all([n1, n2, n3])
        Session.commit()

        self.n1_id = n1.id
        self.n2_id = n2.id
        self.n3_id = n3.id


    ## new -> create #########################################################

    def part_new(self):
        response = self.app.get(url('new_message', format='json'))

    def part_new_frag(self):
        response = self.app.get(url('new_message', format='frag'))

    def part_create(self):
        self.send_member_message('unittest', 'arrr, a subject', 'I am content')
        
        self.log_in_as("unittest")
        self.m1_id = self.send_member_message('unitfriend', 'Re: singing'    , 'My singing is fine!')
        
        self.log_in_as("unitfriend")
        self.m2_id = self.send_member_message('unittest'  , 'Re: Re: singing', 'It is totally not! And to explain, I will use a sentence that is over 50 characters long, to test the Message.__unicode__ truncation feature')
        
        self.m5_id = self.send_member_message('unittest'  , 'deleteme'       , 'this is a message to test deletion with')
        
        self.log_in_as("unittest")


    def part_create_bad_target(self):
        response = self.app.post(
            url('messages'),
            params={
                '_authentication_token': self.auth_token,
                'target': 'MrNotExists',
                'subject': 'arrr, a subject',
                'content': 'I am content',
            },
            status=400
        )

    def part_create_no_content(self):
        response = self.app.post(
            url('messages'),
            params={
                '_authentication_token': self.auth_token,
                'target': 'unittest',
                'subject': 'arrr, a subject',
            },
            status=400
        )


    ## index -> show #########################################################

    def part_index(self):
        response = self.app.get(url('messages', format="frag"))
        self.assertIn("Re: Re: singing", response)

    def part_index_lists(self):
        response = self.app.get(url('messages', format="json", list="notification"))
        response = self.app.get(url('messages', format="json", list="to"))
        response = self.app.get(url('messages', format="json", list="sent"))
        # TODO: need asserts here to check is actual messages are included
        response = self.app.get(url('messages', format="json", list="whgarbl"), status=400)

    def part_index_as_json(self):
        response = self.app.get(url('messages', format='json'))
        self.assertIn("Re: Re: singing", response)

    def part_show(self):
        response = self.app.get(url('message', id=self.m2_id, format="frag"))
        # TODO - check read status after viewing
        self.assertIn("truncation", response)

    def part_show_as_json(self):
        response = self.app.get(url('message', id=self.m2_id, format='json'))
        self.assertIn("truncation", response)

    def part_show_someone_elses(self):
        self.log_in_as('kitten')
        response = self.app.get(url('message', id=self.m1_id), status=403)
        self.log_in()

    def part_show_non_exist(self):
        response = self.app.get(url('message', id=0), status=404)


    ## edit -> update ########################################################
    # messages are un-updatable, so these are stubs

    def part_edit(self):
        response = self.app.get(url('edit_message', id=1), status=501)

    def part_edit_as_json(self):
        response = self.app.get(url('edit_message', id=1, format='json'), status=501)

    def part_update(self):
        response = self.app.put(url('message', id=1), status=501)


    ## delete ################################################################

    def part_delete_message(self):
        response = self.app.post(
            url('message', id=self.m5_id, format="json"),
            params={
                '_method': 'delete',
                '_authentication_token': self.auth_token
            }
        )

    def part_delete_notification(self):
        response = self.app.post(
            url('message', id=self.n3_id, format="json"),
            params={
                '_method': 'delete',
                '_authentication_token': self.auth_token
            }
        )

    def part_delete_someone_elses(self):
        response = self.app.post(
            url('message', id=self.m1_id, format="json"),
            params={
                '_method': 'delete',
                '_authentication_token': self.auth_token
            },
            status=403
        )

    def part_delete_non_exist(self):
        response = self.app.post(
            url('message', id=0, format="json"),
            params={
                '_method': 'delete',
                '_authentication_token': self.auth_token
            },
            status=404
        )
