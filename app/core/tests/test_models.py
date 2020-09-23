"""
Test case for core.model
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from .. import models


def sample_user(email='mail@example.com', password='password1'):
    """
    create a sample user
    """
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
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
        user = get_user_model().objects.create_user(email,
                                                    'qwerty  uiop12')

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

    def test_tag_str(self):
        """
        Test the tag string representation
        """
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredients_str(self):
        """
        Test the ingredients string representation
        """

        ingredients = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredients), ingredients.name)

    def test_recipe_str(self):
        """
        The the recipe string representation
        """
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Egusi Soup',
            time_minutes=30,
            price=1500.00,
            currency='NGN'
        )
        self.assertEqual(str(recipe), recipe.title)
