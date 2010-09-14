from civicboom.tests import *

class TestContentsController(TestController):

    ## index -> show #########################################################

    def test_index(self):
        response = self.app.get(url('contents'))
        # Test response...

    def test_index_as_xml(self):
        response = self.app.get(url('formatted_contents', format='xml'))

    def test_show(self):
        response = self.app.get(url('content', id=1))

    def test_show_article(self):
        response = self.app.get(url('content', id=2))
        # 2 just happens to be the ID of an Article, so we can test the view counter

    def test_show_non_exist(self):
        response = self.app.get(url('content', id=0))

    def test_show_comment(self):
        # comments should not be shown individually -- or should they? With threaded comments,
        # linking to a subthread may be useful
        response = self.app.get(url('content', id=3), status=404)

    def test_show_as_xml(self):
        response = self.app.get(url('formatted_content', id=1, format='xml'))



    ## new -> create #########################################################

    def test_new(self):
        response = self.app.get(url('new_content'))

    def test_new_as_xml(self):
        response = self.app.get(url('formatted_new_content', format='xml'))

    def test_create(self):
        response = self.app.post(
            url('contents'),
            params={
                '_authentication_token': self.auth_token,
                'form_title': "a response",
                'form_parent_id': "1",
                'form_type': "comment",
                'form_content': 'content of a test comment',
            }
        )

    ## edit -> update ########################################################

    def test_edit(self):
        response = self.app.get(url('edit_content', id=2))

    def test_edit_no_perm(self):
        response = self.app.get(url('edit_content', id=1), status=401)

    def test_edit_as_xml(self):
        response = self.app.get(url('formatted_edit_content', id=2, format='xml'))

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

    def test_update_non_exist(self):
        response = self.app.put(
            url('content', id=9999),
            params={
                '_authentication_token': self.auth_token
            },
            status=404
        )

    ## delete ################################################################

    def test_delete(self):
        response = self.app.delete(
            url('content', id=1),
            params={
                '_authentication_token': self.auth_token
            }
        )

    def test_delete_browser_fakeout(self):
        response = self.app.post(
            url('content', id=1),
            params={
                "_method": 'delete',
                '_authentication_token': self.auth_token
            }
        )

    def test_delete_non_exist(self):
        response = self.app.delete(
            url('content', id=9999),
            params={
                '_authentication_token': self.auth_token
            },
            status=404
        )

