"""
Basic tests for ogocarshare.ca
"""
from django.test import TestCase


class OgoBasicTestCase(TestCase):
    """
    Basic tests for ogocarshare.ca
    """
    fixtures = ['ogo_pages.yaml']

    def test_home_page_nav(self):
        """
        Test that the navigation links expected appear on the homepage.
        """
        response = self.client.get('/')
        self.assertContains(response, "OGO", status_code=200)
        # "Universal Nav" links should appear in header and footer:
        self.assertContains(response, "Log In", count=2, status_code=200)
        self.assertContains(response, "Join OGO!", count=2, status_code=200)
        self.assertContains(response, "Help", count=2, status_code=200)
