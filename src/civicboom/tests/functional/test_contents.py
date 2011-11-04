# vim: set fileencoding=utf8:

from civicboom.tests import *
#import json
import warnings


class TestContentsController(TestController):
    
    def test_content_qrcode(self):
        response = self.app.get(url('content_action', id='1', action='qrcode'))
        response = self.app.get(url('content_action', id='1', action='qrcode', format='jpeg', size=300))
    
    def test_character_escaping(self):
        # AllanC - We should be able to send actual unicode in content ... we should be able to send '€' ... this may need additional investigation
        before = u'&euro;<moose><p class="TEST">&</p>' # humm .. I wanted to put an actuall euro in ... humm ...  is this an error with the request generator not accepting unicode? or our site? €
        after  = u'&euro;<p>&amp;</p>' # &euro; should be preserved and <tag should be stripped> & should be escaped
        
        content_id = self.create_content(content=before)
        response      = self.app.get(url('content', id=content_id, format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertIn(after, response_json['data']['content']['content']) 
    
    def test_index(self):
        
        # AllanC - More index tests needed!
        
        #-----
        # Lists of drafts should not have other article types in them .. especially not for logged out users!!!
        
        self.log_in_as('unittest')
        response = self.app.get(url('contents', creator='unittest', list="drafts", format='json'))
        response_json = json.loads(response.body)
        for draft in response_json['data']['list']['items']:
            self.assertEqual(draft['type'],'draft')
        
        self.log_out()
        response = self.app.get(url('contents', creator='unittest', list='drafts', format='json'))
        response_json = json.loads(response.body)
        for draft in response_json['data']['list']['items']:
            self.assertEqual(draft['type'],'draft')
        self.assertEquals(response_json['data']['list']['count'], 0) # Anon users can never see drafts (this could change in future with public drafts)
        
    def test_index_order(self):
        contents = []
        for i in range(3):
            contents.append(self.create_content())
        
        # Change the order of the content to check the index action is sorting by default correctly
        from civicboom.model.meta import Session
        from civicboom.model      import Content
        import datetime
        content_2 = Session.query(Content).get(contents[2])
        content_2.update_date = content_2.update_date - datetime.timedelta(weeks=10)
        content_0 = Session.query(Content).get(contents[0])
        content_0.update_date = content_0.update_date + datetime.timedelta(weeks=10)
        Session.commit()
        
        # Check order
        # There could be other items of content in the list. We want to check for the order of our contents 0,1,2 to be in the order 0 (Newest) then 1 (Now) then 2 (Oldest)
        response      = self.app.get(url('contents', creator='unittest', limit='100', format='json'))
        response_json = json.loads(response.body)
        
        next_index = 0
        for content_id in [content_item['id'] for content_item in response_json['data']['list']['items']]:
            if content_id == contents[next_index]:
                next_index += 1
        self.assertEquals(next_index, len(contents)) # It found the id's in the oder of contents
        
        for content_id in contents:
            self.delete_content(content_id)


    def test_markdown_content(self):
        """
        Test the markdown format is correct processed to HTML
        """
        markdown_content = """
Markdown Title
==============

Title again
-----------

Now lets get marking down

* Yeah
* This
* List

Thats *all* folks

"""
        id = self.create_content(title='Markdown Test', content=markdown_content, content_text_format='markdown')
        
        content = self.get_content(id)['content']
        
        self.assertIn('<li>List'    , content['content'])
        self.assertIn('<h1>'        , content['content'])
        self.assertIn('<em>all</em>', content['content'])
        
        self.delete_content(id)

    def test_html_cleaning(self):
        """
        Test the cleaning of HTML content
        """
        html_content = """
<h1>HTML Cleaner</h1>
<p style="BIG">OH FEAR MY HACKER POWERS <a href="url" onclick="js-h4ckzor">clean me</a></p>
"""
        
        id = self.create_content(title='HTML Clean Test', content=html_content)
        content = self.get_content(id)['content']

        self.assertNotIn('style='               , content['content'])
        self.assertNotIn('js-h4ckzor'           , content['content'])
        self.assertIn   ('<h1>HTML Cleaner</h1>', content['content'])
        ##self.assertIn   ('<a href="url">'       , content['content'])
        
        self.delete_content(id)

    def test_delete_redirect(self):
        """
        When an item of content is deleted in standard redirect mode, it redirects to the item that has just been deleted, because the item is not there, it returns a content not found message
        """
        # POST delete format=redirect fake_http_referer as url(list fo content)
        # POST delete format=html     fake_http_referer as url(this content)
        # POST delete format=html     when no logged in ?
        pass
        
    
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
        self.part_null_tags_removed()

        self.part_can_delete_own_article()
        self.part_cant_delete_someone_elses_article()
        self.part_cant_delete_article_that_doesnt_exist()
        self.part_can_delete_article_owned_by_group_i_am_admin_of()
        
        # GregM: Test private content with followers
        # AllanC: could this be moved to test_permissions.py? I think it fits better
        #self.part_create_private_content()
        #self.part_view_private_content_not_trusted()
        #self.part_view_private_content_trusted()
        #self.part_distrust_check()

    def part_setup(self):
        
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
        response = self.app.get(url('contents', format="json"))
        # Test response...

    def part_index_as_xml(self):
        response = self.app.get(url('contents', format='xml'))


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
        response = self.app.get(url('content', id=self.my_article_id, format='xml'))


    ##########################################################################
    # Content search
    ##########################################################################

    def part_content_results(self):
        response = self.app.get(url('contents', query='test', limit=20))
        self.assertIn("A test article by unitfriend", response)
        #self.assertIn("Friend", response)
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

    def part_content_location_empty(self):
        response = self.app.get(url('contents', location='', format="frag"))
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
        response = self.app.get(url('edit_content', id=self.my_article_id, format='xml'))

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

    def part_null_tags_removed(self):
        response = self.app.put(
            url('content', id=self.my_article_id, format='json'),
            params={
                '_authentication_token': self.auth_token,
                'tags_string': ', ,, ,,    ,',
            }
        )
        # for now, just check that there is no error code


    ## delete ################################################################

    def part_can_delete_own_article(self):
        response = self.app.post(
            url('content', id=self.my_article_id, format="json"),
            params={
                '_method': 'delete',
                '_authentication_token': self.auth_token
            },
            status=200
        )

    def part_cant_delete_someone_elses_article(self):
        response = self.app.post(
            url('content', id=self.his_article_id, format="json"),
            params={
                '_method': 'delete',
                '_authentication_token': self.auth_token
            },
            status=403
        )

    def part_cant_delete_article_that_doesnt_exist(self):
        response = self.app.post(
            url('content', id=0, format="json"),
            params={
                '_method': 'delete',
                '_authentication_token': self.auth_token
            },
            status=404
        )

    def part_can_delete_article_owned_by_group_i_am_admin_of(self):
        pass
        #warnings.warn("test not implemented")
