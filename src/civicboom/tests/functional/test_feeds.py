from civicboom.tests import *

class TestFeedsController(TestController):

    def test_index(self):
        response = self.app.get(url('feeds'))
        # Test response...

    def test_index_as_xml(self):
        response = self.app.get(url('formatted_feeds', format='xml'))

    def test_create(self):
        response = self.app.post(url('feeds'))

    def test_new(self):
        response = self.app.get(url('new_feed'))

    def test_new_as_xml(self):
        response = self.app.get(url('formatted_new_feed', format='xml'))

    def test_update(self):
        response = self.app.put(url('feed', id=1))

    def test_update_browser_fakeout(self):
        response = self.app.post(url('feed', id=1), params=dict(_method='put'))

    def test_delete(self):
        response = self.app.delete(url('feed', id=1))

    def test_delete_browser_fakeout(self):
        response = self.app.post(url('feed', id=1), params=dict(_method='delete'))

    def test_show(self):
        response = self.app.get(url('feed', id=1))

    def test_show_as_xml(self):
        response = self.app.get(url('formatted_feed', id=1, format='xml'))

    def test_edit(self):
        response = self.app.get(url('edit_feed', id=1))

    def test_edit_as_xml(self):
        response = self.app.get(url('formatted_edit_feed', id=1, format='xml'))
