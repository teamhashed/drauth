from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class AuthTestCase(APITestCase):
    def setUp(self):
        self.email = "test@test.test"
        self.password = "test12345"
        self.user = get_user_model().objects.create(
            email=self.email,
            password=self.password
        )
        Token.objects.create(user=self.user)
        self.token = Token.objects.get(user__email=self.email)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.key)

    def test_unauthorized_access(self):
        response = self.client.get(reverse('rest_user_details'))
        self.assertEqual(401, response.status_code)

    def test_authorized_access(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        response = self.client.get(reverse('rest_user_details'))
        self.assertEqual(200, response.status_code)

    def test_logout(self):
        self.client.logout()
        response = self.client.get(reverse('rest_user_details'))
        self.assertEqual(401, response.status_code)
