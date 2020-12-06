from .models import Person
from django import forms


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ("name", "last_name", "email", "phone")
        help_texts = {
            'email': 'A valid unique email address',
            'phone': '+380..',
        }
