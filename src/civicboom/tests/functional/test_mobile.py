from civicboom.tests import *
from base64 import b64encode, b64decode
import json
import warnings

class TestMobileController(TestController):

    def test_latest_version(self):
        response = self.app.get(url(controller='mobile', action='latest_version'))


    def test_media_raw(self):
        self.png1x1 = b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAAAAAA6fptVAAAAAXNSR0IArs4c6QAAAApJREFUCNdj+AcAAQAA/8I+2MAAAAAASUVORK5CYII=')

        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'title': "mobile upload test",
                'type': "article",
                'content': "upload test article",
                'license': 'CC-BY',
                'location': "1.0707 51.2999",
            },
            status=201
        )
        self.my_article_id = json.loads(response.body)["data"]["id"]

        response = self.app.post(
            url(controller='mobile', action='media_init', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'content_id': self.my_article_id,
            },
            status=201
        )
        response = self.app.post(
            url(controller='mobile', action='media_part', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'content_id': self.my_article_id,
                'file_data': self.png1x1[0:30]
            },
            status=201
        )
        response = self.app.post(
            url(controller='mobile', action='media_part', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'content_id': self.my_article_id,
                'file_data': self.png1x1[30:60]
            },
            status=201
        )
        response = self.app.post(
            url(controller='mobile', action='media_part', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'content_id': self.my_article_id,
                'file_data': self.png1x1[60:]
            },
            status=201
        )
        response = self.app.post(
            url(controller='mobile', action='media_finish', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'content_id': self.my_article_id,
                'file_name': 'test.png',
            },
            status=201
        )

    def test_media_base64(self):
        self.png1x1 = b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAAAAAA6fptVAAAAAXNSR0IArs4c6QAAAApJREFUCNdjYAIAAAQAA0VqAKYAAAAASUVORK5CYII=')

        response = self.app.post(
            url('contents', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'title': "mobile upload test",
                'type': "article",
                'content': "upload test article",
                'license': 'CC-BY',
                'location': "1.0707 51.2999",
            },
            status=201
        )
        self.my_article_id = json.loads(response.body)["data"]["id"]

        response = self.app.post(
            url(controller='mobile', action='media_init', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'content_id': self.my_article_id,
            },
            status=201
        )
        response = self.app.post(
            url(controller='mobile', action='media_part', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'content_id': self.my_article_id,
                'encoding': "base64",
                'file_data': b64encode(self.png1x1[0:30])
            },
            status=201
        )
        response = self.app.post(
            url(controller='mobile', action='media_part', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'content_id': self.my_article_id,
                'encoding': "base64",
                'file_data': b64encode(self.png1x1[30:60])
            },
            status=201
        )
        response = self.app.post(
            url(controller='mobile', action='media_part', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'content_id': self.my_article_id,
                'encoding': "base64",
                'file_data': b64encode(self.png1x1[60:])
            },
            status=201
        )
        response = self.app.post(
            url(controller='mobile', action='media_finish', format="json"),
            params={
                '_authentication_token': self.auth_token,
                'content_id': self.my_article_id,
                'file_name': 'test.png',
            },
            status=201
        )


    def test_error(self):
        response = self.app.get(url(controller='mobile', action='error', format="json"))
