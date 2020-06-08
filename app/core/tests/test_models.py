"""
Test case for core.model
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    """
    Model Test class
    """

    def test_create_user_with_email_successful(self):
        """
        Test creating a new user with an email is successful
        :return:
        """
        email = 'don.joe@example.com'
        password = 'qwerty  uiop12'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test the email for a new user is normalized

        Returns:

        """
        email = 'don.joe@EXAMPLE.COM'
        user = get_user_model().objects.create_user(email, 'qwerty  uiop12')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """
        Test creating new user with no email raises error
        Returns:
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "testPass")

    def test_create_new_superuser(self):
        """
        Test creating a new super user
        Returns:

        """
        user = get_user_model().objects.create_superuser(
            'jane.joe@example.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
