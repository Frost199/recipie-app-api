"""
User Api test
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """
    helper function to create user
    """
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """
    Test the user API (public)
    """

    def setUp(self) -> None:
        """
        Setup an API client
        """
        self.client = APIClient()
        self.payload = {
            'email': 'test@gmail.com',
            'password': 'password1',
            'name': 'Don Joe'
        }

    def test_create_valid_user_success(self):
        """
        Test creating user with valid payload is successful
        """
        res = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(self.payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """
        Test creating a user that already exists fails
        """
        create_user(**self.payload)
        res = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """
        Test that the password must be more than 5 characters
        """
        self.payload['password'] = 'pass'
        res = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=self.payload['email']
        ).exists()
        self.assertFalse(user_exists)
