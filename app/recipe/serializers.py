"""
Serializers for the recipe resources
"""
from rest_framework import serializers

from core.models import Tag, Ingredient, Recipe


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
