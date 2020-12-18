"""A module for all django forms."""
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class ReviewForm(forms.Form):
    """Form for product review."""
    review = forms.CharField(label="", widget=forms.Textarea)


class RegisterForm(UserCreationForm):
    """Create a new user."""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
    
