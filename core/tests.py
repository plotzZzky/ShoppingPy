from django.test import TestCase


class PagesTest(TestCase):

    def test_get_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def test_get_home_redirect(self):
        response = self.client.get("/list/")
        self.assertRedirects(response, "/users/login/?next=/list/")

    def test_about(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)
