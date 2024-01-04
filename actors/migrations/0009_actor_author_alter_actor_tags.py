# Generated by Django 5.0 on 2024-01-02 18:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actors', '0008_alter_actor_photo'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='actor',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='actors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='actor',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='actors', to='actors.tag'),
        ),
    ]