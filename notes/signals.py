from .models import Note, Notebook, Tag
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.crypto import get_random_string


# Assign a sync_hash to newly created notes, notebooks and tags
@receiver(post_save, sender=Note)
@receiver(post_save, sender=Notebook)
@receiver(post_save, sender=Tag)
def gen_sync_hash(sender, instance, created, **kwargs):
    if created:
        instance.sync_hash = get_random_string(50)
        instance.save()


def fix_order(notebooks):
    for row_num, notebook in enumerate(notebooks):
        Notebook.objects.filter(id=notebook.id).update(row=row_num)
        fix_order(Notebook.objects.filter(parent=notebook).order_by("row"))


# Whenever a notebook is created, updated or deleted
# ensure that the row ordering is correct.
@receiver(post_save, sender=Notebook)
@receiver(post_delete, sender=Notebook)
def reorder_notebooks(sender, instance, **kwargs):
    notebooks = Notebook.objects.filter(parent=None).order_by("row")
    fix_order(notebooks)
