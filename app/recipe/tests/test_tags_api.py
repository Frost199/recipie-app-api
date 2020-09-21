"""
Test for Tags  Resource in Recipe API
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTest(TestCase):
    """
    Test the publicly available tags API
    """

    def setUp(self) -> None:
        """
        Setup APi client for tags
        """
        self.client = APIClient()

    def test_login_required(self):
        """
        Test that login is required for retrieving tags
        """
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTest(TestCase):
    """
    Test the authorised user tags API
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

    def test_retrieve_tags(self):
        """
        Test retrieving tags
        """
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tag_limited_to_user(self):
        """
        Test that tags returned are for the authenticated user
        """
        user2 = get_user_model().objects.create_user(
            'other@mail.com',
            'password2'
        )
        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Comfort food')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
