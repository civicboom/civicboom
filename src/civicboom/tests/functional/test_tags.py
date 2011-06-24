from civicboom.tests import *

from civicboom.model         import Tag
from civicboom.model.meta    import Session


class TestTags(TestController):

    tags_used = set() # Keep track of all tags used in this automated test

    def check_tags(self, content_id, tags):
        tags = [unicode(tag) for tag in tags]
        response      = self.app.get(url('content', id=content_id, format='json'), status=200)
        response_json = json.loads(response.body)
        self.assertEquals(set(response_json['data']['content']['tags']), set(tags))
        self.tags_used |= set(tags) # update the tags used set to keep track of all tags used in this automated test


    def test_tags(self):
        content_id = self.create_content(tags_string='test  ,tests,  pylons ')
        self.check_tags(    content_id,             ['test','tests','pylons'])
        self.update_content(content_id, tags_string='test,  tests , pyramid')
        self.check_tags(    content_id,            ['test','tests','pyramid'])
        self.update_content(content_id, tags_string='test')
        self.check_tags(    content_id,            ['test'])
        self.update_content(content_id, tags_string='test , bob , monkey')
        self.check_tags(    content_id,            ['test','bob','monkey'])
        self.delete_content(content_id)
        
        tags_in_db = Session.query(Tag).all()
        tags_in_db = set([tag.name for tag in tags_in_db])
        assert self.tags_used <= tags_in_db # Check every tag used in this test is a subset of all tags in DB
