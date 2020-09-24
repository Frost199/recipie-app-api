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

    def test_create_basic_recipe(self):
        """
        Test Creating Recipe
        """
        payload = {
            'title': 'Ede Soup',
            'time_minutes': 45,
            'price': 1500.00,
            'currency': 'NGN',
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def evaluate_recipe(self, ingredient_or_tag1, ingredient_or_tag2,
                        payload, ingredient_or_tag_model_identifier):
        """
        Helper function to evaluate either Ingredient or Recipe
        """
        res = self.client.post(RECIPES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        obj = Recipe.objects.get(id=res.data['id'])
        if ingredient_or_tag_model_identifier == 'tag':
            ingredients_or_tags = obj.tags.all()
        else:
            ingredients_or_tags = obj.ingredients.all()
        self.assertEqual(ingredients_or_tags.count(), 2)
        self.assertIn(ingredient_or_tag1, ingredients_or_tags)
        self.assertIn(ingredient_or_tag2, ingredients_or_tags)

    def test_creating_recipe_with_tags(self):
        """
        Test Creating a recipe with Tags
        """
        tag1 = sample_tags(user=self.user, name='Vegan')
        tag2 = sample_tags(user=self.user, name='Dessert')

        payload = {
            'title': 'Avocado lime cheesecake',
            'time_minutes': 60,
            'price': 5000.00,
            'currency': 'NGN',
            'tags': [tag1.id, tag2.id]
        }
        self.evaluate_recipe(tag1, tag2, payload, 'tag')

    def test_creating_recipe_with_ingredients(self):
        """
        Test Creating a recipe with Ingredients
        """
        ingredient1 = sample_ingredients(user=self.user, name='Prawns')
        ingredient2 = sample_ingredients(user=self.user, name='Garlic')

        payload = {
            'title': 'Avocado lime cheesecake',
            'time_minutes': 20,
            'price': 500.00,
            'currency': 'NGN',
            'ingredients': [ingredient1.id, ingredient2.id]
        }
        self.evaluate_recipe(ingredient1, ingredient2, payload, 'ingredient')

    def test_partial_update_recipe(self):
        """
        Test Updating a recipe wih PATCH
        """
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tags(user=self.user))
        new_tag = sample_tags(user=self.user, name='Cabbage')

        payload = {'title': 'Salad', 'tags': [new_tag.id]}
        url = detail_url(recipe_id=recipe.id)
        self.client.patch(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        tags = recipe.tags.all()
        self.assertEqual(len(tags), 1)
        self.assertIn(new_tag, tags)

    def test_full_update_recipe(self):
        """
        Test Updating a Recipe with PUT
        """
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tags(user=self.user))
        payload = {
            'title': 'Jollof Spaghetti',
            'time_minutes': 30,
            'price': 5.00,
            'currency': 'USD',
        }
        url = detail_url(recipe_id=recipe.id)
        self.client.put(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.time_minutes, payload['time_minutes'])
        self.assertEqual(recipe.price, payload['price'])
        self.assertEqual(recipe.currency, payload['currency'])
        tags = recipe.tags.all()
        self.assertEqual(len(tags), 0)
