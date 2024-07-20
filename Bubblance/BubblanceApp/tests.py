from django.test import TestCase

# Create your tests here.

from django.urls import reverse, resolve
from django.test import TestCase

class URLPatternTest(TestCase):
    def test_customer_ride_url(self):
        url = reverse('customer_ride_page')
        self.assertEqual(resolve(url).view_name, 'customer_ride_page')
        self.assertEqual(url, '/customer_ride/')

    def test_customer_ride_url_with_token(self):
        url = reverse('customer_ride_page') + '?token=test_token'
        self.assertEqual(resolve(url).view_name, 'customer_ride_page')
        self.assertTrue('token=test_token' in url)