"""
Test for Recipe resource in Recipe API
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """
    Return recipe detail url
    """
    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_tags(user, name='Main cuisine'):
    """
    Create and return a sample tag
    """
    return Tag.objects.create(user=user, name=name)


def sample_ingredients(user, name='pepper'):
    """
    Create and return a sample ingredient
    """
    return Ingredient.objects.create(user=user, name=name)


def sample_recipe(user, **kwargs):
    """
    Create and return a sample recipe
    """
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 15,
        'price': 500.00,
        'currency': 'NGN',
    }
    defaults.update(kwargs)
    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeAPiTest(TestCase):
    """
    Test unauthenticated recipe API access
    """

    def setUp(self) -> None:
        """
        Setup APi client for Recipe
        """
        self.client = APIClient()

    def test_auth_required(self):
        """
        Test that auth is required
        """
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
    """
    Test authenticated recipe API Access
    """

    def setUp(self) -> None:
        """
        create a user for testing the private API resource
        """
        self.user = get_user_model().objects.create_user(
            'mail@mail.com',
            'password1'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieving_recipes(self):
        """
        Test retrieving a list of recipes
        """
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_limited_to_user(self):
        """
        Test retrieving recipes for user
        """
        user2 = get_user_model().objects.create_user(
            'mail@mail2.com',
            'password2'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):
        """
        Test viewing a recipe detail
        """
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tags(user=self.user))
        recipe.ingredients.add(sample_ingredients(user=self.user))

        url = detail_url(recipe_id=recipe.id)
        res = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.data, serializer.data)
