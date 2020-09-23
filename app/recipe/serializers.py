"""
Serializers for the recipe resources
"""
from rest_framework import serializers

from core.models import Tag, Ingredient


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for tag objects
    """

    class Meta:
        """
        Meta objets for Tag Serializer
        """
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for ingredients object
    """

    class Meta:
        """
        Meta object for ingredients serializer
        """
        model = Ingredient
        fields = ('id', 'name',)
        read_only_fields = ('id',)
