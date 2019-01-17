import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# If a user sets a notebook row to 255, it will move
# the notebook to the end
NULL_ROW_NUMBER = -255


def _fix_order(notebooks, curNotebook=None):
    """
    This functions takes a list of Notebooks.
    If curNotebook is set, it will return the value
    of the new row value.
    """
    curNotebook_new_row_val = -1
    for row_num, notebook in enumerate(notebooks):
        Notebook.objects.filter(id=notebook.id).update(row=row_num)
        if curNotebook.id == notebook.id:
            curNotebook_new_row_val = row_num
        children_check = _fix_order(Notebook.objects.filter(
            parent=notebook).order_by("row"), curNotebook)
        if children_check != -1:
            curNotebook_new_row_val = children_check
    return curNotebook_new_row_val


class Notebook(models.Model):
    sync_hash = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=70)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='children')
    user = models.ForeignKey(
        'auth.User', related_name="notebooks", on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(
        'auth.User', related_name="shared_notebooks", blank=True)
    is_public = models.BooleanField(default=False, blank=True)
    row = models.IntegerField(default=NULL_ROW_NUMBER, blank=True)

    def fix_order(self):
        notebooks = Notebook.objects.filter(user=self.user,
                                            parent=None).order_by("row")
        return _fix_order(notebooks, self)

    def save(self, *args, **kwargs):
        # Before the super class function
        if self.row == NULL_ROW_NUMBER:
            sibling_notebooks = \
                Notebook.objects.filter(parent=self.parent).order_by("-row")
            largest_row_num = 0
            for notebook in sibling_notebooks:
                largest_row_num = notebook.row
                print("Examining", notebook.title, notebook.row)
                if notebook != self:
                    break
            self.row = largest_row_num + 1

        # The super class function
        super().save(*args, **kwargs)

        # After the super class function
        self.row = self.fix_order()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('row',)


class Tag(models.Model):
    sync_hash = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    user = models.ForeignKey(
        'auth.User', related_name="tags", on_delete=models.CASCADE)

    def clean(self):
        tags_with_same_name = len(Tag.objects.filter(title__iexact=self.title))
        if tags_with_same_name > 0:
            raise ValidationError(
                _("Tag names must be unique. They are case-insensitive."))

    def __str__(self):
        return self.title


class Note(models.Model):
    sync_hash = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=120)
    text = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
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

    class Meta:
        ordering = ("-date_modified",)
