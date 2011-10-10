from civicboom.tests import *
#import json


class TestFeedsController(TestController):
    def test_all(self):
        self.part_new()
        self.part_create()

        self.part_index()
        self.part_index_as_xml()
        self.part_show()
        self.part_show_as_xml()

        self.part_edit()
        self.part_update()

        self.part_delete()


    def part_new(self):
        response = self.app.get(url('new_feed'))

    # FIXME: needs data to be submitted, data format isn't set yet
    def part_create(self):
        response = self.app.post(
            url('feeds', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'name': 'test feed #1',
            },
            status=201
        )
        self.f1_id = json.loads(response.body)['data']['id']

        response = self.app.post(
            url('feeds', format='json'),
            params={
                '_authentication_token': self.auth_token,
                'name': 'deleteme',
            },
            status=201
        )
        self.f2_id = json.loads(response.body)['data']['id']


    def part_index(self):
        response = self.app.get(url('feeds'))
        # Test response...

    def part_index_as_xml(self):
        response = self.app.get(url('feeds', format='xml'))

    def part_show(self):
        response = self.app.get(url('feed', id=self.f1_id))

    def part_show_as_xml(self):
        response = self.app.get(url('feed', id=self.f1_id, format='xml'))


    def part_edit(self):
        response = self.app.get(url('edit_feed', id=self.f1_id))

    def part_update(self):
        response = self.app.put(
            url('feed', id=self.f1_id, format='json'),
            params={
                "name": "new name from put",
            }
        )


    def part_delete(self):
        response = self.app.post(url('feed', id=self.f2_id, format='json'),
            params= {'_method': 'delete',})
