from django.test import Client, TestCase


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
