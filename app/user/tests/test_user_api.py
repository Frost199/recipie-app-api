"""
User Api test
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
PROFILE_URL = reverse('user:profile')


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

    def test_create_token_for_user(self):
        """
        Test that a token is created for a user
        """
        create_user(**self.payload)
        res = self.client.post(TOKEN_URL, self.payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """
        Test that token is not created if invalid credentials are given
        """
        create_user(**self.payload)
        wrong_payload = self.payload
        wrong_payload['password'] = 'wrong pass'
        res = self.client.post(TOKEN_URL, wrong_payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """
        Test that token is not created if user does not exist
        """
        self.payload['email'] = 'new_user_not_available@example.com'
        res = self.client.post(TOKEN_URL, self.payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """
        Test that email and password are required
        """
        res = self.client.post(TOKEN_URL, {'email': 'mail', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_users_unauthorized(self):
        """
        Test that authentication is required for users
        """
        res = self.client.get(PROFILE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    """
    Test Api requests that require Authentication
    """

    def setUp(self) -> None:
        """
        Set up a user by creating a user
        """
        self.user = create_user(
            email='email@exaple.com',
            password='password1',
            name='John Doe'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """
        Test retrieving profile for logged in user
        """
        res = self.client.get(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })
        self.assertNotIn('password', res.data)

    def test_post_profile_not_allowed(self):
        """
        Test that POST is not allowed in the profile URL
        """
        res = self.client.post(PROFILE_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """
        Test updating the user profile for authenticated users
        """
        payload = {'name': 'Jane Doe', 'password': 'password2'}
        res = self.client.patch(PROFILE_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
