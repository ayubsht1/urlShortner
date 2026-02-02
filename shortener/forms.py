from django import forms
from .models import ShortURL

class ShortURLForm(forms.ModelForm):
    custom_key = forms.CharField(required=False, max_length=10)

    class Meta:
        model = ShortURL
        fields = ['original_url', 'expires_at']