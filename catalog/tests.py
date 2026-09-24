from django.test import TestCase


class HomePageTest(TestCase):
    def test_home_page_status(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_contacts_page_status(self):
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)
