from django.db import models


class Notebook(models.Model):
    sync_hash = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=70)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='children')
    user = models.ForeignKey(
        'auth.User', related_name="notebooks", on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(
        'auth.User', related_name="shared_notebooks", blank=True)
    is_public = models.BooleanField(default=False, blank=True)
    row = models.IntegerField(default=0, blank=True)

    def __str__(self):
                return self.title


class Tag(models.Model):
    sync_hash = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=100)
    user = models.ForeignKey(
        'auth.User', related_name="tags", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Note(models.Model):
    sync_hash = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=120)
    text = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        'auth.User', related_name="notes", on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(
        'auth.User', related_name="shared_notes", blank=True)
    is_public = models.BooleanField(default=False, blank=True)
    notebook = models.ForeignKey(
        Notebook,
        related_name="notes",
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, related_name="notes", blank=True)

    trashed = models.BooleanField(default=False)
    favorited = models.BooleanField(default=False)

    def __str__(self):
        return self.title
