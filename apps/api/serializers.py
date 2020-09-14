from rest_framework import serializers
from apps.api.models import Category, Note


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Note
        fields = ('id', 'title', 'description', 'owner', 'category', 'solution', 'reference', 'created_at',
                  'updated_at', 'is_public')


class CategorySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    notes = NoteSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Category
        fields = ('id', 'title', 'owner', 'notes', 'created_at', 'updated_at')
