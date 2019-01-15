from django.contrib import admin
from .models import Note, Notebook, Tag
from admirarchy.toolbox import HierarchicalModelAdmin

# Register your models here.


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    readonly_fields = ["sync_hash"]


@admin.register(Notebook)
class NotebookAdmin(HierarchicalModelAdmin):
    hierarchy = True
    ordering = ('row',)
    list_display = ["title", "row"]
    readonly_fields = ["sync_hash"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    readonly_fields = ["sync_hash"]
