from django.contrib import admin
from .models import Note, Notebook, Tag

# Register your models here.


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    readonly_fields = ["sync_hash"]


@admin.register(Notebook)
class NotebookAdmin(admin.ModelAdmin):
    hierarchy = True
    ordering = ('row',)
    list_display = ["title", "row"]
    readonly_fields = ["sync_hash"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    readonly_fields = ["sync_hash"]
    list_display = ["title", "row"]
