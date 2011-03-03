# vim: set fileencoding=utf8:

from civicboom.tests import *
#import json
import warnings


class TestContentsController(TestController):
    def test_all(self):
        self.part_setup()

        self.part_index()
        self.part_index_as_xml()
        self.part_content_results()
        self.part_content_results_rss()
        self.part_content_results_json()
        self.part_content_no_results()
        self.part_content_no_query()
        self.part_content_rss()
        self.part_content_location()
        self.part_content_location_radius()
        self.part_content_type()
        self.part_content_author()
        self.part_content_response_to()
        self.part_can_show_own_article()
        self.part_can_show_someone_elses_article()
        self.part_can_show_own_draft()
        self.part_cant_show_someone_elses_draft()
        self.part_cant_show_comment_that_doesnt_exist()
        self.part_cant_show_individual_comment()
        self.part_show_as_xml()

        self.part_new_redirects_to_edit()
        self.part_comment_has_no_license()
        self.part_comment_has_no_license_even_if_specified_and_parent_has_preference()
        self.part_response_has_parent_preference_license_by_default()
        self.part_response_has_own_license_if_specified()
        self.part_cant_create_comment_without_parent()
        self.part_cant_comment_on_something_that_doesnt_exist()
        self.part_cant_comment_on_what_cant_be_seen()

        self.part_edit()
        self.part_edit_as_xml()
        self.part_edit_no_perm()
        self.part_edit_no_exist()
        self.part_can_update_article_owned_by_group_i_am_admin_of()
        self.part_can_update_article_owned_by_group_i_am_member_of()
        self.part_can_update_own_article()
        self.part_cant_update_someone_elses_article()
        self.part_cant_update_article_that_doesnt_exist()

        self.part_can_delete_own_article()
        self.part_cant_delete_someone_elses_article()
        self.part_cant_delete_article_that_doesnt_exist()
        self.part_can_delete_article_owned_by_group_i_am_admin_of()


    def part_setup(self):
        self.log_in_as("unittest")

        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'title': "A test article by the test user",
                'type': "article",
                'content': """
ここにいくつかのテキストです。
وهنا بعض النص.
这里是一些文字。
הנה כמה טקסט.
εδώ είναι ένα κείμενο.
यहाँ कुछ पाठ है.
здесь некий текст.
여기에 일부 텍스트입니다.
דאָ איז עטלעכע טעקסט.
""",
                'license': 'CC-BY',
                'location': "1.0707 51.2999",
            },
            status=201
        )
        self.my_article_id = json.loads(response.body)["data"]["id"]

        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'title': "A test draft by the test user",
                'content': "a test draft",
                'license': 'CC-BY',
                'location': "1.0707 51.2999",
            },
            status=201
        )
        self.my_draft_id = json.loads(response.body)["data"]["id"]

        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'title': "A test comment by the test user",
                'type': 'comment',
                'parent_id': self.my_article_id,
                'content': "a test comment",
                'license': 'CC-BY',
                'location': "1.0707 51.2999",
            },
            status=201
        )
        self.my_comment_id = json.loads(response.body)["data"]["id"]

        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'title': "Assignment for the world to see",
                'type': 'assignment',
                'content': "a test assignment",
                'license': 'CC-BY',
                'location': "1.0707 51.2999",
            },
            status=201
        )
        self.my_assignment_id = json.loads(response.body)["data"]["id"]


        self.log_in_as("unitfriend")

        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'type': 'article',
                'title': "A test article by unitfriend",
                'content': "Here is some text",
                'license': 'CC-BY',
                'location': "1.0707 51.2999",
            },
            status=201
        )
        self.his_article_id = json.loads(response.body)["data"]["id"]

        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'title': "A test draft by the test user",
                'content': "a test draft",
                'license': 'CC-BY',
                'location': "1.0707 51.2999",
            },
            status=201
        )
        self.his_draft_id = json.loads(response.body)["data"]["id"]

        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'title': "A test comment by unitfriend",
                'type': 'comment',
                'parent_id': self.my_article_id,
                'content': "a test comment",
                'license': 'CC-BY',
                'location': "1.0707 51.2999",
            },
            status=201
        )
        self.his_comment_id = json.loads(response.body)["data"]["id"]

        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'title': "There once was an assignment by unitfriend",
                'type': 'assignment',
                'content': "with suggestion of CC-PD",
                'license': 'CC-PD',
                'location': "1.0707 51.2999",
            },
            status=201
        )
        self.my_assignment_id = json.loads(response.body)["data"]["id"]

        self.log_in_as("unittest")


    ## index -> show #########################################################

    def part_index(self):
        response = self.app.get(url('formatted_contents', format="json"))
        # Test response...

    def part_index_as_xml(self):
        response = self.app.get(url('formatted_contents', format='xml'))


    def part_can_show_own_article(self):
        response = self.app.get(url('content', id=self.my_article_id))

    def part_can_show_someone_elses_article(self):
        response = self.app.get(url('content', id=self.his_article_id))

    def part_can_show_own_draft(self):
        response = self.app.get(url('content', id=self.my_draft_id))

    def part_cant_show_someone_elses_draft(self):
        response = self.app.get(url('content', id=self.his_draft_id), status=403)

    def part_cant_show_comment_that_doesnt_exist(self):
        response = self.app.get(url('content', id=0), status=404)

    def part_cant_show_individual_comment(self):
        # comments should not be shown individually -- or should they? With threaded comments,
        # linking to a subthread may be useful
        response = self.app.get(url('content', id=self.my_comment_id), status=302)
        # AllanC - currently redirects to parent ... could be considered in the future with threaded comments (see Shish's comment)

    def part_show_as_xml(self):
        response = self.app.get(url('formatted_content', id=self.my_article_id, format='xml'))


    ##########################################################################
    # Content search
    ##########################################################################

    def part_content_results(self):
        response = self.app.get(url('contents', query='test'))
        self.assertIn("A test article by unitfriend", response)
        self.assertIn("Friend", response)
        #self.assertIn("0 responses", response)

    def part_content_results_rss(self):
        response = self.app.get(url('contents', format="rss", query='test'))
        self.assertIn("A test article by unitfriend", response)
        self.assertIn("Friend", response)

    def part_content_results_json(self):
        response = self.app.get(url('contents', format="json", query='test'))
        self.assertIn("A test article by unitfriend", response)
        self.assertIn("Friend", response)

    def part_content_no_results(self):
        response = self.app.get(url('contents', query='cake'))
        # FIXME: term is no longer used in output
        #self.assertIn("'cake' did not match any articles", response)

    def part_content_no_query(self):
        response = self.app.get(url('contents'))
        response = self.app.get(url('contents', format="frag"))

    def part_content_rss(self):
        response = self.app.get(url('contents', format='xml'))

    def part_content_location(self):
        response = self.app.get(url('contents', location='1,51', format="frag"))
        # FIXME: article list has no content, only title
        #self.assertIn("Here is some text", response)

    def part_content_location_radius(self):
        response = self.app.get(url('contents', location='1,51,10', format="frag"))
        #self.assertIn("Here is some text", response)

    def part_content_type(self):
        response = self.app.get(url('contents', type='assignment', format="frag"))
        self.assertIn("There once was", response)

    def part_content_author(self):
        response = self.app.get(url('contents', author='unittest', format="frag"))
        self.assertIn("Assignment for the world to see", response)

    def part_content_response_to(self):
        response = self.app.get(url('contents', response_to=2, format="frag"))
        # FIXME: create a response as test data
        #self.assertIn("something", response)


    ## new -> create #########################################################

    # new requires auth as it creates something
    def part_new_redirects_to_edit(self):
        response = self.app.post(
            url('new_content'),
            params={
                '_authentication_token': self.auth_token,
            },
            status=302
        )

    def part_comment_has_no_license(self):
        pass
        #warnings.warn("test not implemented")

    def part_comment_has_no_license_even_if_specified_and_parent_has_preference(self):
        pass
        #warnings.warn("test not implemented")

    def part_response_has_parent_preference_license_by_default(self):
        pass
        #warnings.warn("test not implemented")

    def part_response_has_own_license_if_specified(self):
        pass
        #warnings.warn("test not implemented")

    def part_cant_create_comment_without_parent(self):
        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'title': "a response",
                'type': "comment",
                'content': 'content of a test comment',
            },
            status=400
        )
        self.assertIn('invalid', response)

    def part_cant_comment_on_something_that_doesnt_exist(self):
        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'title': "a response",
                'parent_id': "0",
                'type': "comment",
                'content': 'content of a test comment',
            },
            status=400
        )
        self.assertIn('invalid', response)

    def part_cant_comment_on_what_cant_be_seen(self):
        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'title': "a response",
                'parent_id': self.his_draft_id,
                'type': "comment",
                'content': 'content of a test comment',
            },
            status=400
        )

    def part_can_update_article_owned_by_group_i_am_admin_of(self):
        pass
        #warnings.warn("test not implemented")

    def part_can_update_article_owned_by_group_i_am_member_of(self):
        pass
        #warnings.warn("test not implemented")


    ## edit -> update ########################################################

    def part_edit(self):
        response = self.app.get(url('edit_content', id=self.my_article_id))

    def part_edit_as_xml(self):
        response = self.app.get(url('formatted_edit_content', id=self.my_article_id, format='xml'))

    def part_edit_no_perm(self):
        response = self.app.get(url('edit_content', id=self.his_article_id), status=403)

    def part_edit_no_exist(self):
        response = self.app.get(url('edit_content', id=0), status=404)


    def part_can_update_own_article(self):
        response = self.app.put(
            url('content', id=self.my_article_id, format='json'),
            params={
                '_authentication_token': self.auth_token
            }
        )

    def part_cant_update_someone_elses_article(self):
        response = self.app.put(
            url('content', id=self.his_article_id),
            params={
                '_authentication_token': self.auth_token
            },
            status=403
        )

    def part_cant_update_article_that_doesnt_exist(self):
        response = self.app.put(
            url('content', id=0),
            params={
                '_authentication_token': self.auth_token
            },
            status=404
        )


    ## delete ################################################################

    def part_can_delete_own_article(self):
        response = self.app.delete(
            url('content', id=self.my_article_id, format="json"),
            params={
                '_authentication_token': self.auth_token
            },
            status=200
        )

    def part_cant_delete_someone_elses_article(self):
        response = self.app.delete(
            url('content', id=self.his_article_id, format="json"),
            params={
                '_authentication_token': self.auth_token
            },
            status=403
        )

    def part_cant_delete_article_that_doesnt_exist(self):
        response = self.app.delete(
            url('content', id=0, format="json"),
            params={
                '_authentication_token': self.auth_token
            },
            status=404
        )

    def part_can_delete_article_owned_by_group_i_am_admin_of(self):
        pass
        #warnings.warn("test not implemented")
