from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import AdoptionRequest


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs['class'] = 'form-control'


class AdoptionForm(forms.ModelForm):
    previous_pet_experience = forms.TypedChoiceField(
        label="Have you owned a pet before?",
        choices=[(True, 'Yes'), (False, 'No')],
        coerce=lambda v: v in (True, 'True'),
        widget=forms.RadioSelect,
        initial=False,
    )

    class Meta:
        model = AdoptionRequest
        fields = ['address', 'phone', 'reason', 'previous_pet_experience', 'message']
        labels = {
            'reason': 'Why do you want this pet?',
            'message': 'Additional message (optional)',
        }
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }
