from django import forms
from .models import Actor, Category, Producer


class ActorForm(forms.ModelForm):
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

    class Meta:
        model = Actor
        fields = ('first_name', 'last_name', 'biography', 'is_published','category', 'producer')
        labels = {
            'first_name': 'First name:',
            'last_name': 'Last name:',
            'biography': 'Biography:',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-input',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-input',
            }),
            'biography': forms.Textarea(attrs={
                'cols': 50,
                'rows': 5,
            }),
            'is_published': forms.CheckboxInput()
        }