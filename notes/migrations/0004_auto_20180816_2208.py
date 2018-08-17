# Generated by Django 2.1 on 2018-08-16 22:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0003_auto_20180816_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='shared_with',
            field=models.ManyToManyField(related_name='shared_notes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notebook',
            name='shared_with',
            field=models.ManyToManyField(related_name='shared_notebooks', to=settings.AUTH_USER_MODEL),
        ),
    ]