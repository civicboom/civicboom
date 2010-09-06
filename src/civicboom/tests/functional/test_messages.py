from civicboom.tests import *

class TestMessagesController(TestController):

    ## index -> show #########################################################

    def test_index(self):
        response = self.app.get(url('messages'))
        assert "Re: Re: singing" in response

    def test_index_as_json(self):
        response = self.app.get(url('formatted_messages', format='json'))
        assert "Re: Re: singing" in response

    def test_show(self):
        response = self.app.get(url('message', id=2))
        assert "truncation" in response

    def test_show_as_json(self):
        response = self.app.get(url('formatted_message', id=2, format='json'))
        assert "truncation" in response

    def test_show_someone_elses(self):
        response = self.app.get(url('message', id=1), status=403)


    ## new -> create #########################################################
    # there is no "new message" form page; the form is embedded in other pages for now

    def test_new(self):
        response = self.app.get(url('new_message'))

    def test_new_as_json(self):
        response = self.app.get(url('formatted_new_message', format='json'))

    def test_create(self):
        response = self.app.post(
            url('messages'),
            params={
                '_authentication_token': self.auth_token,
                'target': 'unittest',
                'subject': 'arrr, a subject',
                'content': 'I am content',
            },
            status=302
        )

    def test_create_bad_target(self):
        response = self.app.post(
            url('messages'),
            params={
                '_authentication_token': self.auth_token,
                'target': 'MrNotExists',
                'subject': 'arrr, a subject',
                'content': 'I am content',
            },
            status=302
        )
        # FIXME: follow redirect, then
        #assert "Can't find user" in response


    ## delete ################################################################

    def test_delete(self):
        response = self.app.delete(
            url('message', id=3),
            params={
                '_authentication_token': self.auth_token
            }
        )

    def test_delete_browser_fakeout(self):
        response = self.app.post(
            url('message', id=4),
            params={
                "_method": 'delete',
                '_authentication_token': self.auth_token
            }
        )

    def test_delete_someone_elses(self):
        # FIXME: failure is indicated by "302 redirect to failure message" -- how to test that this
        # is different from "302 redirect to success message"?
        response = self.app.delete(
            url('message', id=1),
            params={
                '_authentication_token': self.auth_token
            },
            status=302
        )

    ## edit -> update ########################################################
    # messages are un-updatable, so these are stubs

    def test_edit(self):
        response = self.app.get(url('edit_message', id=1))

    def test_edit_as_json(self):
        response = self.app.get(url('formatted_edit_message', id=1, format='json'))

    def test_update(self):
        response = self.app.put(url('message', id=1))

    def test_update_browser_fakeout(self):
        response = self.app.post(url('message', id=1), params=dict(_method='put'))
