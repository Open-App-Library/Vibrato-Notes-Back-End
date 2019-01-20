import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

"""
# Commentary

-----------------------------------
-- How notebook row numbers work --
-----------------------------------

I would like to explain how row numbers work with notebooks because the
first variable defined in this file NULL_ROW_NUMBER.

Row numbers are used to define the order you want your notebooks to appear in.

Here is a diagram that makes this a little easier to grasp:

0 - Recipes
1 - Journaling
2 - CompSci
0   - Python
1   - C++
3 Fitness Tracking

Get it? The row tracks the current index number of the current notebook in the
current level of hierarchy.

It is worth noting that the back-end API will normalize notebook rows. What
does that mean? It means that when you create a new notebook with a custom row
or if you update the row of an existing notebook, it will make sure the row
numbers of your notebooks start at zero and ONLY increment by 1.

So...If you try to update your notebooks with these row values...

 0 - Recipes
23 - CompSci

It will be corrected to this...

0 - Recipes
1 - CompSci

Now what is NULL_ROW_NUMBER about?

This variable is used when creating and editing notebooks. If
you insert a notebook with a row value of -255, that notebook will be inserted
at the bottom of your notebook list. This is the default value as it is most
logical to append your notebook to the bottom of your notebook list rather than
at the beginning.

--------------------------------------------
-- Optional encryption using is_encrypted --
--------------------------------------------

Note: Note/Notebook/Tag data is never encrypted on the back-end. This is all up
to the apps to do. Official Vibrato Notes apps will encrypt data on the
client-side by default.

However, there might be some things you don't want to have encrypted. There are
various reasons you might not. Perhaps, the data you are sending is intended to
be public. Perhaps you just want the convinience of accessing data from the
REST API without having to deal with decrypting and re-encrypting it.

Nothing is stopping you from sending un-encrypted data to the back-end. But
what happens if you open up this un-encrypted data in an official Vibrato
Notes app? How will it know that the data is not encrypted and it is just
plain-text? Well, the answer is the 'is_encrypted' BooleanField.

By default, when you create notes, notebooks or tags into the REST API,
is_encrypted will be set to False. Once again, official Vibrato Notes apps
will set is_encrypted to True by default since it encrypts notes on the
client-side by default.
"""

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
    is_public = models.BooleanField(default=False, blank=True)
    row = models.IntegerField(default=NULL_ROW_NUMBER, blank=True)
    date_modified = models.DateTimeField(auto_now=True, editable=False)
    is_encrypted = models.BooleanField(default=False)

    def fix_order(self):
        notebooks = Notebook.objects.filter(user=self.user,
                                            parent=None).order_by("row")
        return _fix_order(notebooks, self)

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
    user = models.ForeignKey(
        'auth.User', related_name="tags", on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True, editable=False)
    is_encrypted = models.BooleanField(default=False)

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
    date_modified = models.DateTimeField(auto_now=True, editable=False)
    user = models.ForeignKey(
        'auth.User', related_name="notes", on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False, blank=True)
    notebook = models.ForeignKey(
        Notebook,
        related_name="notes",
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, related_name="notes", blank=True)
    is_encrypted = models.BooleanField(default=False)

    trashed = models.BooleanField(default=False)
    favorited = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-date_modified",)
