"""A module for all django forms."""
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class ReviewForm(forms.Form):
    """Form for product review."""
    review = forms.CharField(label="", widget=forms.Textarea)


class RegisterForm(UserCreationForm):
    """Create a new user."""

    class Meta:
        model = User
        fields = ('username', 'email')
