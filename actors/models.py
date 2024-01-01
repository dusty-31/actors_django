from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from .services import cyrillic_to_latin


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, unique=True, default='')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(cyrillic_to_latin(cyrillic_text=str(self.name)))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(viewname='actors:category', kwargs={'category_slug': self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=255, unique=True, default='')

    class Meta:
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = str(self.name).lower().replace(' ', '-')
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(viewname='actors:tag', kwargs={'tag_slug': self.slug})


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
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), PublishedStatus.choices)),
                                       default=PublishedStatus.DRAFT)
    category = models.ForeignKey(related_name='actors', to=Category, on_delete=models.PROTECT, null=True)
    tags = models.ManyToManyField(related_name='tags', to=Tag, blank=True)
    producer = models.OneToOneField(related_name='producer', to='Producer', on_delete=models.SET_NULL, null=True,
                                    blank=True)

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name} | ID: {self.id}'

    def save(self, *args, **kwargs):
        self.slug = slugify(cyrillic_to_latin(cyrillic_text=self.get_full_name()))

        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(viewname='actors:post', kwargs={'post_slug': self.slug})

    def get_full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Producer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
