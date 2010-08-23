from civicboom.tests import *

class TestMessagesController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='messages', action='index'))
        assert "Re: Re: singing" in response

    def test_read(self):
        response = self.app.get(url(controller='messages', action='read', id=2))
        assert "truncation" in response

    def test_read_someone_elses(self):
        response = self.app.get(url(controller='messages', action='read', id=1), status=403)

    def test_send(self):
        response = self.app.post(
            url(controller='messages', action='send'),
            params={
                '_authentication_token': self.auth_token
            }
        )

    # FIXME: we need to create some more test data -- since tests are run in random
    # order, these can sometimes delete messages and then other tests look for them
#    def test_delete(self):
#        response = self.app.post(
#            url(controller='messages', action='delete'),
#            params={
#                'type': 'message',
#                'msg_id': 2,
#                '_authentication_token': self.auth_token
#            }
#        )

#    def test_delete_someone_elses(self):
#        response = self.app.post(
#            url(controller='messages', action='delete'),
#            params={
#                'type': 'message',
#                'msg_id': 1,
#                '_authentication_token': self.auth_token
#            }
#        )
