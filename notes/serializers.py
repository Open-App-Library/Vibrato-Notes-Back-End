from rest_framework import serializers
from .models import Note, Notebook, Tag


class NotebookChildren(serializers.Serializer):
    """
    A magical recursive field.
    This is used in the NotebookSerializer to
    display child notebooks.
    """

    def to_representation(self, value):
        serializer = NotebookSerializer(value, context=self.context)
        return serializer.data


class NotebookSerializer(serializers.ModelSerializer):
    children = NotebookChildren(read_only=True, many=True)

    class Meta:
        model = Notebook
        fields = ('sync_hash', 'id', 'title', 'parent', 'shared_with', 'row',
                  'children',)
        read_only_fields = ('sync_hash', 'id', 'children')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('sync_hash', 'id', 'title')
        read_only_fields = ('sync_hash',)


class NoteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Note
        fields = ('sync_hash', 'id', 'date_created', 'date_modified', 'title', 'text',
                  'notebook', 'tags', 'user', 'shared_with', 'trashed',
                  'favorited')
        read_only_fields = ('sync_hash',)
