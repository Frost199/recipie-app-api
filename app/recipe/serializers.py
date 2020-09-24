"""
Serializers for the recipe resources
"""
from rest_framework import serializers

from core.models import Tag, Ingredient, Recipe


class BaseMetaForTagAndIngredients:
    """
    Base Meta for both tags and Ingredients
    """
    fields = ('id', 'name')
    read_only_fields = ('id',)


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for tag objects
    """

    class Meta(BaseMetaForTagAndIngredients):
        """
        Meta objets for Tag Serializer
        """
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for ingredients object
    """

    class Meta(BaseMetaForTagAndIngredients):
        """
        Meta object for ingredients serializer
        """
        model = Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serialize a recipe
    """

    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )

    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        """
        Meta object for Recipe serializer
        """
        model = Recipe
        fields = ('id', 'title', 'link', 'ingredients', 'tags', 'time_minutes',
                  'price', 'currency',)
        read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    """
    Serialize a recipe detail
    """
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
