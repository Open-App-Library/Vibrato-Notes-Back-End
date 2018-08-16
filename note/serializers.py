from rest_framework import serializers
from .models import Note, Notebook, Tag

class NoteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Note
		fields = ('id', 'title', 'text', 'user', 'notebook', 'tag_set')

