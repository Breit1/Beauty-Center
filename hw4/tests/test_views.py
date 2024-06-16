from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse


class RegisterAPITest(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")

    def test_register_success(self):
        """
        Test successful user registration.
        """
        data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "test@example.com",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "testuser")

    def test_register_missing_fields(self):
        """
        Test registration with missing fields.
        """
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_register_existing_username(self):
        """
        Test registration with an existing username.
        """

        User.objects.create_user(
            username="testuser", password="testpassword", email="existing@example.com"
        )

        data = {
            "username": "testuser",
            "password": "newpassword",
            "email": "newuser@example.com",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_register_exception(self):
        """
        Test registration with an exception during user creation.
        """

        data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "invalidemail",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
