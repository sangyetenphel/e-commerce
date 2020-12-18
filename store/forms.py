"""A module for all django forms."""
from django.contrib.auth.models import User
from django import forms

class ReviewForm(forms.Form):
    """Form for product review."""
    review = forms.CharField(label="", widget=forms.Textarea)


class UserForm(forms.ModelForm):
    """Create a new user."""
    # To not display password as a plain text.
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
