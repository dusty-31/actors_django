from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, unique=True, default='')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = str(self.name).lower().replace(' ', '-')
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(viewname='actors:category', kwargs={'category_slug': self.slug})


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Actor.PublishedStatus.PUBLISHED)


class Actor(models.Model):
    class PublishedStatus(models.IntegerChoices):
        DRAFT = 0, 'Draft',
        PUBLISHED = 1, 'Published'

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    biography = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, default='')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=PublishedStatus.choices, default=PublishedStatus.DRAFT)
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT, null=True)

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name} | ID: {self.id}'

    def save(self, *args, **kwargs):
        self.slug = f'{str(self.first_name).lower().replace(' ', '-')}-{str(self.last_name).lower().replace(' ', '-')}'
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(viewname='actors:post', kwargs={'post_slug': self.slug})
