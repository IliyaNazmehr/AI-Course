from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailLoginTests(TestCase):

    def setUp(self):
        self.login_url = reverse("account_login")  # AllAuth login URL

        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword123"
        )

    def test_user_can_login_with_email(self):
        response = self.client.post(self.login_url, {
            "login": "test@example.com",      # AllAuth uses "login" field
            "password": "testpassword123"
        })

        # Should redirect (login success)
        self.assertEqual(response.status_code, 302)

        # Check that user is authenticated
        self.assertTrue("_auth_user_id" in self.client.session)
