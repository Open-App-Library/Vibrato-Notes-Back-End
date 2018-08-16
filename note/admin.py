from django.contrib import admin
from .models import Note, Notebook, Tag

# Register your models here.
admin.site.register(Note)
admin.site.register(Notebook)
admin.site.register(Tag)
