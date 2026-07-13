from django.test import TestCase
from django.urls import reverse


class HomeRedirectTests(TestCase):
    def test_root_redirects_to_login(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('accounts:login'), fetch_redirect_response=False)

    def test_accounts_login_alias_returns_login_page(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
