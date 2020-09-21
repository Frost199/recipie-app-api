"""
Serializers for the recipe resources
"""
from rest_framework import serializers

from core.models import Tag


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
