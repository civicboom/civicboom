from civicboom.tests import *

class TestMessagesController(TestController):

    ## index -> show #########################################################

    def test_index(self):
        response = self.app.get(url('messages'), format="frag")
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

    def test_show_non_exist(self):
        response = self.app.get(url('message', id=0), status=404)


    ## new -> create #########################################################
    # there is no "new message" form page; the form is embedded in other pages for now

    def test_new(self):
        response = self.app.get(url('new_message'), status=501)

    def test_new_as_json(self):
        response = self.app.get(url('formatted_new_message', format='json'), status=501)

    def test_create(self):
        response = self.app.post(
            url('messages'),
            params={
                '_authentication_token': self.auth_token,
                'target': 'unittest',
                'subject': 'arrr, a subject',
                'content': 'I am content',
            },
            status=201
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
            status=404
        )

    def test_create_no_content(self):
        response = self.app.post(
            url('messages'),
            params={
                '_authentication_token': self.auth_token,
                'target': 'unittest',
                'subject': 'arrr, a subject',
            },
            status=400
        )


    ## delete ################################################################

    def test_delete_message(self):
        response = self.app.delete(
            url('message', id=5, format="json"),
            params={
                '_authentication_token': self.auth_token
            }
        )

    def test_delete_browser_fakeout(self):
        response = self.app.post(
            url('message', id=6, format="json"),
            params={
                "_method": 'delete',
                '_authentication_token': self.auth_token
            }
        )

    def test_delete_notification(self):
        response = self.app.delete(
            url('message', id=7, format="json"),
            params={
                '_authentication_token': self.auth_token
            }
        )

    def test_delete_someone_elses(self):
        response = self.app.delete(
            url('message', id=1, format="json"),
            params={
                '_authentication_token': self.auth_token
            },
            status=403
        )

    def test_delete_non_exist(self):
        response = self.app.delete(
            url('message', id=0, format="json"),
            params={
                '_authentication_token': self.auth_token
            },
            status=404
        )


    ## edit -> update ########################################################
    # messages are un-updatable, so these are stubs

    def test_edit(self):
        response = self.app.get(url('edit_message', id=1), status=501)

    def test_edit_as_json(self):
        response = self.app.get(url('formatted_edit_message', id=1, format='json'), status=501)

    def test_update(self):
        response = self.app.put(url('message', id=1), status=501)

    def test_update_browser_fakeout(self):
        response = self.app.post(url('message', id=1), params=dict(_method='put'), status=501)
