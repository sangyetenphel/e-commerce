"""A module for all django forms."""
from django import forms

class ReviewForm(forms.Form):
    """Form for product review."""
    review = forms.CharField(label="", widget=forms.Textarea)
    