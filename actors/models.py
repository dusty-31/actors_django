from django.db import models
from django.urls import reverse


class Actor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    biography = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, default='')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name} | ID: {self.id}'

    def save(self, *args, **kwargs):
        self.slug = f'{str(self.first_name).lower().replace(' ', '-')}-{str(self.last_name).lower().replace(' ', '-')}'
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(viewname='actors:post', kwargs={'post_slug': self.slug})
