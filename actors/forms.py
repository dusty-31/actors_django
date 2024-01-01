from django import forms

from .models import Category, Producer


class ActorForm(forms.Form):
    first_name = forms.CharField(max_length=50,
                                 label='First name:',
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-input',
                                     'placeholder': 'Enter your first name...',
                                 }))
    last_name = forms.CharField(max_length=50,
                                label='Last name:',
                                widget=forms.TextInput(attrs={
                                    'class': 'form-input',
                                    'placeholder': 'Enter your last name...'
                                }))
    slug = forms.SlugField(label='URL(optional):',
                           required=False)
    is_published = forms.BooleanField(label='Publish:',
                                      required=False,
                                      initial=True,
                                      )
    biography = forms.CharField(label='Biography:',
                                widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}))
    category = forms.ModelChoiceField(label='Category',
                                      queryset=Category.objects.all(),
                                      empty_label='Select category')
    producer = forms.ModelChoiceField(label='Producer(optional):',
                                      queryset=Producer.objects.all(),
                                      empty_label='Select producer',
                                      required=False)
