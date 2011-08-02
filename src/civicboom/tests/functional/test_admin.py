from civicboom.tests import *
import logging


class TestAdminController(TestController):
    def get_https(self, url):
        logging.debug(url)
        return self.app.get(url, extra_environ={'HTTP_X_URL_SCHEME': 'https'})


    def test_admin(self):
        response = self.get_https(url(controller='admin', action='models')) # "models" is the admin index


    #---------------------------------------------------------------------------
    # Custom pages

    def test_threads(self):
        response = self.get_https(url(controller='admin', action='threads'))

    def test_event_log(self):
        response = self.get_https(url(controller='test', action='fill_log'))
        response = self.get_https(url(controller='admin', action='event_log'))
        self.assertIn("debug", response)
        # test searching
        response = self.get_https(url(controller='admin', action='event_log', module='civicboom/controllers/test.py'))
        response = self.get_https(url(controller='admin', action='event_log', line_num='20'))
        response = self.get_https(url(controller='admin', action='event_log', username='None'))
        response = self.get_https(url(controller='admin', action='event_log', address='127.0.0.1'))
        response = self.get_https(url(controller='admin', action='event_log', url='http://waffle.com'))

    def test_user_emails(self):
        response = self.get_https(url(controller='admin', action='user_emails', format='csv'))
        
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
        response = self.get_https("/admin/User/models?User--username=jammy")
        # tests ints
        response = self.get_https("/admin/Group/models?Group--num_members=1")


    types = [
        ("License",   "CC-BY"),
        # ("Tag",
        # ("Media",   # these are blank
        ("Member",          1),
        ("User",            1),
        ("Group",           3),
        ("Content",         1),
        ("ArticleContent",  3),
    ]

    def test_lists(self):
        for t,i in self.types:
            response = self.get_https("/admin/%s/models" % t)

    def test_news(self):
        for t,i in self.types:
            response = self.get_https("/admin/%s/models/new" % t)

    def test_edits(self):
        for t,i in self.types:
            response = self.get_https("/admin/%s/models/%s/edit?" % (t,i))


    # FIXME: these error out when the pages are empty ._.?

    #def test_history_list(self):
    #    response = self.get_https("/admin/ContentEditHistory/models")

    #def test_content_status(self):
    #    response = self.get_https("/admin/Content/models?Content--status=pending")

    #def test_user_status(self):
    #    response = self.get_https("/admin/User/models?User--status=pending")
    #    response = self.get_https("/admin/User/models?User--status=suspended")

    def test_datepicker_and_enummer_and_usercompleter(self):
        response = self.get_https("/admin/ArticleContent/models/3/edit?")
