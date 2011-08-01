from civicboom.tests import *


class TestAdminController(TestController):
    def test_admin(self):
        response = self.app.get(url(controller='admin', action='models')) # "models" is the admin index


    #---------------------------------------------------------------------------
    # Custom pages

    def test_threads(self):
        response = self.app.get(url(controller='admin', action='threads'))

    def test_event_log(self):
        response = self.app.get(url(controller='test', action='fill_log'))
        response = self.app.get(url(controller='admin', action='event_log'), extra_environ={'HTTP_X_URL_SCHEME': 'https'})
        self.assertIn("debug", response)
        # test searching
        response = self.app.get(url(controller='admin', action='event_log', module='civicboom/controllers/test.py'), extra_environ={'HTTP_X_URL_SCHEME': 'https'})
        response = self.app.get(url(controller='admin', action='event_log', line_num='20'), extra_environ={'HTTP_X_URL_SCHEME': 'https'})
        response = self.app.get(url(controller='admin', action='event_log', username='None'), extra_environ={'HTTP_X_URL_SCHEME': 'https'})
        response = self.app.get(url(controller='admin', action='event_log', address='127.0.0.1'), extra_environ={'HTTP_X_URL_SCHEME': 'https'})
        response = self.app.get(url(controller='admin', action='event_log', url='http://waffle.com'), extra_environ={'HTTP_X_URL_SCHEME': 'https'})

    def test_user_emails(self):
        response = self.app.get(url(controller='admin', action='user_emails', format='csv'), extra_environ={'HTTP_X_URL_SCHEME': 'https'})
        
        found_unittest = False
        for line in response.body.split('\n'):
            for item in line.split(','):
                item = item.strip()
                if item=='unittest':
                    found_unittest = True
        
        assert found_unittest


    #---------------------------------------------------------------------------
    # Formalchemy bits

    def test_admin_search(self):
        # tests strings
        response = self.app.get("/admin/User/models?User--username=jammy")
        # tests ints
        response = self.app.get("/admin/Group/models?Group--num_members=1")


    types = [
        "License", "Tags", "Media",
        "Member", "User", "Group",
        "Content", "ArticleContent",
    ]

    def test_lists(self):
        for t in self.types:
            response = self.app.get("/admin/%s/models" % t)

    def test_news(self):
        for t in self.types:
            response = self.app.get("/admin/%s/models/new" % t)

    def test_edits(self):
        for t in self.types:
            response = self.app.get("/admin/%s/models/1/edit?" % t)


    # FIXME: these error out when the pages are empty ._.?

    #def test_history_list(self):
    #    response = self.app.get("/admin/ContentEditHistory/models")

    #def test_content_status(self):
    #    response = self.app.get("/admin/Content/models?Content--status=pending")

    #def test_user_status(self):
    #    response = self.app.get("/admin/User/models?User--status=pending")
    #    response = self.app.get("/admin/User/models?User--status=suspended")

    def test_datepicker_and_enummer_and_usercompleter(self):
        response = self.app.get("/admin/ArticleContent/models/2/edit?")
