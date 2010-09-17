from civicboom.tests import *

class TestContentsController(TestController):

    ## index -> show #########################################################

    def test_index(self):
        response = self.app.get(url('contents'))
        # Test response...

    def test_index_as_xml(self):
        response = self.app.get(url('formatted_contents', format='xml'))

    def test_show_article(self):
        response = self.app.get(url('content', id=1))

    def test_show_draft(self):
        response = self.app.get(url('content', id=3))

    def test_show_no_perm(self):
        response = self.app.get(url('content', id=4))

    def test_show_no_exist(self):
        response = self.app.get(url('content', id=0), status=404)

    def test_show_comment(self):
        # comments should not be shown individually -- or should they? With threaded comments,
        # linking to a subthread may be useful
        response = self.app.get(url('content', id=5), status=404)

    def test_show_as_xml(self):
        response = self.app.get(url('formatted_content', id=1, format='xml'))



    ## new -> create #########################################################

    def test_new(self):
        response = self.app.get(url('new_content'))

    def test_new_as_xml(self):
        response = self.app.get(url('formatted_new_content', format='xml'))

    def test_create_ok(self):
        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'form_title': "a response",
                'form_parent_id': "1",
                'form_type': "comment",
                'form_content': 'content of a test comment',
            },
            status=201
        )

    def test_create_invalid(self):
        # comment without parent is one type of invalid; there are others
        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'form_title': "a response",
                'form_type': "comment",
                'form_content': 'content of a test comment',
            },
            status=400
        )

    def test_create_response_to_no_exist(self):
        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'form_title': "a response",
                'form_parent_id': "0",
                'form_type': "comment",
                'form_content': 'content of a test comment',
            },
            status=404
        )

    def test_create_response_to_no_perm(self):
        # users shouldn't be able to comment on things they can't see
        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'form_title': "a response",
                'form_parent_id': "4",
                'form_type': "comment",
                'form_content': 'content of a test comment',
            },
            status=403
        )


    ## edit -> update ########################################################

    def test_edit(self):
        response = self.app.get(url('edit_content', id=1))

    def test_edit_as_xml(self):
        response = self.app.get(url('formatted_edit_content', id=1, format='xml'))

    def test_edit_no_perm(self):
        response = self.app.get(url('edit_content', id=2), status=403)

    def test_edit_no_exist(self):
        response = self.app.get(url('edit_content', id=0), status=404)

    def test_update(self):
        response = self.app.put(
            url('content', id=1),
            params={
                '_authentication_token': self.auth_token
            }
        )

    def test_update_browser_fakeout(self):
        response = self.app.post(
            url('content', id=1),
            params={
                "_method": 'put',
                '_authentication_token': self.auth_token
            }
        )

    def test_update_no_perm(self):
        response = self.app.put(
            url('content', id=2),
            params={
                '_authentication_token': self.auth_token
            },
            status=403
        )

    def test_update_no_exist(self):
        response = self.app.put(
            url('content', id=0),
            params={
                '_authentication_token': self.auth_token
            },
            status=404
        )


    ## delete ################################################################

    def test_delete(self):
        response = self.app.delete(
            url('content', id=8, format="json"),
            params={
                '_authentication_token': self.auth_token
            },
            status=200
        )

    def test_delete_browser_fakeout(self):
        response = self.app.post(
            url('content', id=9, format="json"),
            params={
                "_method": 'delete',
                '_authentication_token': self.auth_token
            },
            status=200
        )

    def test_delete_no_perm(self):
        # FACT: a user should not be able to delete another user's article
        response = self.app.delete(
            url('content', id=2, format="json"),
            params={
                '_authentication_token': self.auth_token
            },
            status=403
        )

    def test_delete_no_exist(self):
        # FACT: a user should not be able to delete an article that does not exist
        response = self.app.delete(
            url('content', id=0, format="json"),
            params={
                '_authentication_token': self.auth_token
            },
            status=404
        )

    # TODO: a group admin should be able to delete articles owned by the group?
