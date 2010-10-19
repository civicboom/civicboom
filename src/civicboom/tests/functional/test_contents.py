from civicboom.tests import *

class TestContentsController(TestController):

    ## index -> show #########################################################

    def test_index(self):
        response = self.app.get(url('formatted_contents', format="json"))
        # Test response...

    def test_index_as_xml(self):
        response = self.app.get(url('formatted_contents', format='xml'))


    def test_can_show_own_article(self):
        response = self.app.get(url('content', id=1))

    def test_can_show_someone_elses_article(self):
        response = self.app.get(url('content', id=1))

    def test_can_show_own_draft(self):
        response = self.app.get(url('content', id=3))

    def test_cant_show_someone_elses_draft(self):
        response = self.app.get(url('content', id=4), status=403)

    def test_cant_show_comment_that_doesnt_exist(self):
        response = self.app.get(url('content', id=0), status=404)

    def test_cant_show_individual_comment(self):
        # comments should not be shown individually -- or should they? With threaded comments,
        # linking to a subthread may be useful
        response = self.app.get(url('content', id=5), status=404)

    def test_show_as_xml(self):
        response = self.app.get(url('formatted_content', id=1, format='xml'))



    ## new -> create #########################################################

    # new requires auth as it creates something
    def test_new_redirects_to_edit(self):
        response = self.app.post(
            url('new_content'),
            params={
                '_authentication_token': self.auth_token,
            },
            status=302
        )

    def test_create_comment(self):
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

    def test_direct_create_draft(self):
        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'form_title': "a response",
                'form_parent_id': "1",
                'form_type': "draft",
                'form_content': 'content of a test draft',
            },
            status=201
        )

    def test_direct_create_article(self):
        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'form_title': "a response",
                'form_type': "article",
                'form_content': 'content of a directly-created article',
            },
            status=201
        )

    def test_cant_create_comment_without_parent(self):
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

    def test_cant_comment_on_something_that_doesnt_exist(self):
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

    def test_cant_comment_on_what_cant_be_seen(self):
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

    def test_can_update_article_owned_by_group_i_am_admin_of(self):
        pass

    def test_can_update_article_owned_by_group_i_am_member_of(self):
        pass


    ## edit -> update ########################################################

    def test_edit(self):
        response = self.app.get(url('edit_content', id=1))

    def test_edit_as_xml(self):
        response = self.app.get(url('formatted_edit_content', id=1, format='xml'))

    def test_edit_no_perm(self):
        response = self.app.get(url('edit_content', id=2), status=403)

    def test_edit_no_exist(self):
        response = self.app.get(url('edit_content', id=0), status=404)


    def test_can_update_own_article(self):
        response = self.app.put(
            url('content', id=1, format='json'),
            params={
                '_authentication_token': self.auth_token
            }
        )

    def test_update_browser_fakeout(self):
        response = self.app.post(
            url('content', id=1, format='json'),
            params={
                "_method": 'put',
                '_authentication_token': self.auth_token
            }
        )

    def test_cant_update_someone_elses_article(self):
        response = self.app.put(
            url('content', id=2),
            params={
                '_authentication_token': self.auth_token
            },
            status=403
        )

    def test_cant_update_article_that_doesnt_exist(self):
        response = self.app.put(
            url('content', id=0),
            params={
                '_authentication_token': self.auth_token
            },
            status=404
        )


    ## delete ################################################################

    def test_can_delete_own_article(self):
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

    def test_cant_delete_someone_elses_article(self):
        response = self.app.delete(
            url('content', id=2, format="json"),
            params={
                '_authentication_token': self.auth_token
            },
            status=403
        )

    def test_cant_delete_article_that_doesnt_exist(self):
        response = self.app.delete(
            url('content', id=0, format="json"),
            params={
                '_authentication_token': self.auth_token
            },
            status=404
        )

    def test_can_delete_article_owned_by_group_i_am_admin_of(self):
        pass
