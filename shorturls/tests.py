import json
import random
from unittest.mock import patch

from django.test import Client, TestCase
from graphene_django.utils.testing import GraphQLTestCase

from settings.schema import schema

from . import models


class TestGraphQL(GraphQLTestCase):
    """Test entire GraphQL API"""

    GRAPHQL_SCHEMA = schema
    fixtures = ["shorturls"]

    def test_fetch_url(self):
        """It should return the original URL when given the short URL identifier"""
        response = self.query(
            """
            query {
              urlByShortUrl(shortUrl: "A7dw") {
                originalUrl, shortUrl
              }
            }
            """
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        assert content == {
            "data": {
                "urlByShortUrl": {
                    "originalUrl": "http://www.google.ca/somelongpath",
                    "shortUrl": "http://localhost/A7dw",
                }
            }
        }

    def test_fetch_nonexistent_url(self):
        """It should return an error if the short URL does not exist"""
        # Note: this prints an exception even on success
        # Haven't found a way to suppress it
        response = self.query(
            """
            query {
              urlByShortUrl(shortUrl: "dne") {
                originalUrl, shortUrl
              }
            }
            """
        )
        assert "errors" in response.json()

    @patch("shorturls.models.URLMapping.generate_short_url", return_value="tDot")
    def test_add_url(self, mock_urlmapping):
        """It should create a new short URL and return it"""
        response = self.query(
            """
            mutation {
              createShortUrl(originalUrl: "http://hollybecker.net") {
                urlMapping {
                  originalUrl, shortUrl
                }
              }
            }
            """,
            op_name="createShortUrl",
            input_data={"original_url": "http://hollybecker.net"},
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        assert content == {
            "data": {
                "createShortUrl": {
                    "urlMapping": {
                        "originalUrl": "http://hollybecker.net",
                        "shortUrl": "http://localhost/tDot",
                    }
                }
            }
        }


class TestURLMapping(TestCase):
    """Test URLMapping model"""

    fixtures = ["shorturls"]

    def test_generate_short_url(self):
        """It should generate a unique short URL identifier"""
        random.seed(1)  # Set seed so we can test producing an existing URL
        short_url = models.URLMapping.generate_short_url()
        assert len(short_url) == 4
        assert not models.URLMapping.objects.filter(short_url=short_url).exists()


class TestViews(TestCase):

    fixtures = ["shorturls"]

    def setUp(self):
        self.client = Client()

    def test_redirect(self):
        """It should redirect from the short URL to the original URL"""
        response = self.client.get("/A7dw")
        assert response.status_code == 302
        assert response.url == "http://www.google.ca/somelongpath"

    def test_redirect_dne(self):
        """It should return a 404 error when the short URL does not exist"""
        response = self.client.get("/dne1")
        assert response.status_code == 404
