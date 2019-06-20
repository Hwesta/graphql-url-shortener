import random

from django.test import Client, TestCase

from . import models


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
