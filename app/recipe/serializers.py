from rest_framework import serializers
from core.models import Tag, Information


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag object"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_Fields = ('id',)


class InformationSerializer(serializers.ModelSerializer):
    """Serializer for an Information object"""

    class Meta:
        model = Information
        fields = ('id', 'name')
        read_only_fields = ('id',)
