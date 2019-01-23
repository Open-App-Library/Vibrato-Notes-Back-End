import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# If a user sets a notebook row to 255, it will move
# the notebook to the end
NULL_ROW_NUMBER = -255


def _fix_order_notebooks(notebooks, curNotebook=None):
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
        children_check = _fix_order_notebooks(Notebook.objects.filter(
            parent=notebook).order_by("row"), curNotebook)
        if children_check != -1:
            curNotebook_new_row_val = children_check
    return curNotebook_new_row_val


def _fix_order_tags(tags, curTag=None):
    """
    This functions takes a list of Notebooks.
    If curNotebook is set, it will return the value
    of the new row value.
    """
    curTag_new_row_val = -1
    for row_num, tag in enumerate(tags):
        Tag.objects.filter(id=tag.id).update(row=row_num)
        if curTag.id == tag.id:
            curTag_new_row_val = row_num
    return curTag_new_row_val


class Note(models.Model):
    sync_hash = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=120)
    text = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True, editable=False)
    user = models.ForeignKey(
        'auth.User', related_name="notes", on_delete=models.CASCADE)
    notebook = models.ForeignKey(
        'notes.Notebook',
        related_name="notes",
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    tags = models.ManyToManyField(
        'notes.Tag',
        related_name="notes",
        blank=True)
    favorited = models.BooleanField(default=False)
    public = models.BooleanField(default=False, blank=True)
    encrypted = models.BooleanField(default=False)
    trashed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-date_modified",)


class Notebook(models.Model):
    sync_hash = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=70)
    date_modified = models.DateTimeField(auto_now=True, editable=False)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='children')
    user = models.ForeignKey(
        'auth.User', related_name="notebooks", on_delete=models.CASCADE)
    row = models.IntegerField(default=NULL_ROW_NUMBER, blank=True)
    public = models.BooleanField(default=False, blank=True)
    encrypted = models.BooleanField(default=False)

    def fix_order(self):
        notebooks = Notebook.objects.filter(user=self.user,
                                            parent=None).order_by("row")
        return _fix_order_notebooks(notebooks, self)

    def save(self, *args, **kwargs):
        # Before the super class function
        if self.row == NULL_ROW_NUMBER:
            sibling_notebooks = \
                Notebook.objects.filter(user=self.user,
                                        parent=self.parent).order_by("-row")
            largest_row_num = 0
            for notebook in sibling_notebooks:
                largest_row_num = notebook.row
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
    date_modified = models.DateTimeField(auto_now=True, editable=False)
    user = models.ForeignKey(
        'auth.User', related_name="tags", on_delete=models.CASCADE)
    row = models.IntegerField(default=NULL_ROW_NUMBER, blank=True)
    encrypted = models.BooleanField(default=False)

    def clean(self):
        tags_with_same_name = Tag.objects.filter(
            title__iexact=self.title).exclude(id=self.id)
        count = len(tags_with_same_name)
        if count > 0:
            raise ValidationError(
                _("Tag names must be unique. They are case-insensitive."))

    def fix_order(self):
        tags = Tag.objects.filter(user=self.user).order_by("row")
        return _fix_order_tags(tags, self)

    def save(self, *args, **kwargs):
        # Before the super class function
        if self.row == NULL_ROW_NUMBER:
            tags_id_desc = Tag.objects.filter(user=self.user).order_by("-row")
            largest_row_num = 0
            for tag in tags_id_desc:
                largest_row_num = tag.row
                if tag != self:
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
