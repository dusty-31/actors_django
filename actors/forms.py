from django import forms
from .models import Actor, Category, Producer, Tag


class ActorForm(forms.ModelForm):
    """Form for the 'Actor' model.

    Provides form fields to collect data for an Actor instance.

    Attributes:
        category (ModelChoiceField): Dropdown list of all available Category instances.
        producer (ModelChoiceField): Dropdown list of all available Producer instances, label as optional.
        is_published (BooleanField): Checkbox to mark if the Actor instance is published, default is True.
        tags (ModelMultipleChoiceField): Multiple selection field of all available Tag instances, not required.

    Subclasses:
        Meta: Defines additional metadata for the ActorForm, such as the model it's associated with,
        the fields included in the form (first_name, last_name, biography, photo, is_published, category,
        tags, producer), the labels for each field, and widgets to control the rendering of 'first_name',
        'last_name', 'biography', and 'is_published' fields.
    """
    category = forms.ModelChoiceField(
        label='Category',
        queryset=Category.objects.all(),
        empty_label='Select category'
    )
    producer = forms.ModelChoiceField(
        label='Producer(optional):',
        queryset=Producer.objects.filter(producer=None),
        empty_label='Select producer',
        required=False
    )
    is_published = forms.BooleanField(
        label='Publish:',
        required=False,
        initial=True
    )
    tags = forms.ModelMultipleChoiceField(
        label='Tags:',
        queryset=Tag.objects.all(),
        required=False
    )

    class Meta:
        model = Actor
        fields = ('first_name', 'last_name', 'biography', 'photo', 'is_published', 'category', 'tags', 'producer')
        labels = {
            'first_name': 'First name:',
            'last_name': 'Last name:',
            'biography': 'Biography:',
            'photo': 'Photo:'
        }
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-input',
                }),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-input',
                }),
            'biography': forms.Textarea(
                attrs={
                    'cols': 50,
                    'rows': 5,
                }),
            'is_published': forms.CheckboxInput()
        }
