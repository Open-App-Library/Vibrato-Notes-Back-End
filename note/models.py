from django.db import models
from django.contrib.auth.models import User

# Database Models

class Notebook(models.Model):
	title = models.CharField(max_length=70)
	parent = models.ForeignKey('Notebook', null=True, blank=True, on_delete=models.SET_NULL)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	def __str__(self):
		return self.title

class Note(models.Model):
	title = models.CharField(max_length=120)
	text = models.TextField(blank=True, null=True)
	user = models.ForeignKey(User,  on_delete=models.CASCADE)
	notebook = models.ForeignKey(Notebook, null=True, blank=True, on_delete=models.SET_NULL)
	def __str__(self):
		return self.title

class Tag(models.Model):
	title = models.CharField(max_length=100)
	note = models.ForeignKey(Note, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	def __str__(self):
		return self.title

