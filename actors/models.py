from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import QuerySet
from django.template.defaultfilters import slugify
from django.urls import reverse

from .services import cyrillic_to_latin


class Category(models.Model):
    """Represents a category in the database.

    Attributes:
        name (CharField): The name of the category. Has a limit of 50 characters.
        slug (SlugField): The slug of the category. Used in URL. Unique and default value is an empty string.
    """
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, unique=True, default='')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        """Returns the string representation of the category.

        Returns:
            string: The name of the category.
        """
        return self.name

    def save(self, *args, **kwargs):
        """Overrides the save method to automatically create a slug.

        The slug is based on the category's name converting it to a string and translating cyrillic to latin
        characters. It is saved in lowercase and replaces whitespaces with hyphens.
        """
        self.slug = slugify(cyrillic_to_latin(cyrillic_text=str(self.name)))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Returns the URL that shows the detail view of the category.

         Returns:
             string: The URL of the category's detail view.
         """
        return reverse(viewname='actors:category', kwargs={'category_slug': self.slug})


class Tag(models.Model):
    """Represents a tag in the database.

    Attributes:
        name (CharField): The name of the tag. Has a limit of 100 characters and must be unique.
        slug (SlugField): The slug of the tag. Used in URL. Unique and the default value is an empty string.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=255, unique=True, default='')

    class Meta:
        verbose_name_plural = 'Tags'

    def __str__(self):
        """Returns the string representation of the tag.

        Returns:
            string: The name of the tag.
        """
        return self.name

    def save(self, *args, **kwargs):
        """Overrides the save method to automatically create a slug.

        The slug is based on the tag's name converting it to a string and translating cyrillic to latin
        characters. It is saved in lowercase and replaces whitespaces with hyphens.

        Returns:
            Model instance: The saved Tag model instance.
        """
        self.slug = slugify(cyrillic_to_latin(cyrillic_text=str(self.name)))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Returns the URL that shows the detail view of the tag.

        Returns:
            string: The URL of the tag's detail view.
        """
        return reverse(viewname='actors:tag', kwargs={'tag_slug': self.slug})


class PublishedManager(models.Manager):
    """Custom manager for Actor model to handle published actors specifically.

    This manager filters out only published actors. Inherits from Django's base manager class.
    """

    def get_queryset(self) -> QuerySet:
        """Overrides get_queryset to filter for published actors.

        Returns:
            QuerySet: A QuerySet that contains only published actors.
        """
        return super().get_queryset().filter(is_published=Actor.PublishedStatus.PUBLISHED)


class Actor(models.Model):
    """Represents an actor in the database.

    Attributes:
        first_name (CharField): The first name of the actor, a maximum of 50 characters.
        last_name (CharField): The last name of the actor, a maximum of 50 characters.
        biography (TextField): A brief biography of the actor, optional.
        slug (SlugField): The slug of the actor. Used in URLs, unique, with a default value of an empty string.
        time_create (DateTimeField): The date and time the actor record was created, automatically set when the record
        is created.
        time_update (DateTimeField): The date and time the actor record was last updated, automatically set when the
        record is updated.
        is_published (BooleanField): Indicates whether the actor is published, defaults to the draft state.
        photo (ImageField): An image field to hold actor's photo, optional.
        category (ForeignKey): A foreign key relationship with the Category model.
        tags (ManyToManyField): A many-to-many relationship with the Tag model.
        producer (OneToOneField): A one-to-one relationship with the Producer model, optional.
        author (ForeignKey): The author of the actor record, a foreign key relationship with the user model.
        objects (Manager): The default manager including all records.
        published (PublishedManager): A custom manager including published records only.
    """

    class PublishedStatus(models.IntegerChoices):
        """Choices for the publish status of an actor."""
        DRAFT = 0, 'Draft',
        PUBLISHED = 1, 'Published'

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    biography = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, default='')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), PublishedStatus.choices)),
        default=PublishedStatus.DRAFT
    )
    photo = models.ImageField(upload_to='actors_photos/', blank=True, null=True)
    category = models.ForeignKey(
        related_name='actors',
        to=Category,
        on_delete=models.PROTECT,
        null=True
    )
    tags = models.ManyToManyField(
        related_name='actors',
        to=Tag,
        blank=True
    )
    producer = models.OneToOneField(
        related_name='producer',
        to='Producer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    author = models.ForeignKey(
        related_name='actors',
        to=get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
    )

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        """Returns a string representation of the Actor model.

        Returns:
            string: A string that includes the first name, last name and ID of the actor.
        """
        return f'{self.first_name} {self.last_name} | ID: {self.id}'

    def save(self, *args, **kwargs):
        """Overrides the save method to automatically create a slug.

        Returns:
            Actor: The saved Actor model instance.
        """
        self.slug = slugify(cyrillic_to_latin(cyrillic_text=self.get_full_name()))

        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Returns the URL of the actor's detail view on the site.

        Returns:
            string: The URL of the actor's detail view.
        """
        return reverse(viewname='actors:post', kwargs={'slug': self.slug})

    def get_full_name(self) -> str:
        """Return the full name of the actor

        Returns:
            string: A string that includes the first name and last name of the actor.
        """
        return f'{self.first_name} {self.last_name}'


class Producer(models.Model):
    """Represents a producer in the database.

    Attributes:
        first_name (CharField): The first name of the producer, a maximum of 50 characters.
        last_name (CharField): The last name of the producer, a maximum of 50 characters.
        age (IntegerField): The age of the producer. It can be null.
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(null=True)

    def __str__(self):
        """Returns a string representation of the Producer model.

        The string representation contains the first name and last name of the producer.

        Returns:
            string: A string that includes the first name and last name of the producer.
        """
        return f'{self.first_name} {self.last_name}'
