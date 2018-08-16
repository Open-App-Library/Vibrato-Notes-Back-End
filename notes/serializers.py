from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note, Notebook, Tag

class UserSerializer(serializers.ModelSerializer):
	notes = serializers.PrimaryKeyRelatedField(many=True, queryset=Note.objects.all())
	notebooks = serializers.PrimaryKeyRelatedField(many=True, queryset=Notebook.objects.all())
	tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())

	class Meta:
		model = User
		fields = ('id', 'username', 'notes', 'notebooks', 'tags')

class NoteSerializer(serializers.ModelSerializer):
	user = serializers.ReadOnlyField(source="user.username")
	class Meta:
		model = Note
		fields = ('id', 'title', 'text', 'notebook', 'tags', 'user', 'shared_with')

