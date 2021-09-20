from django import forms
from .models import Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('main',)
        labels = {
            'main':''
        }
        widgets = {
            'main': forms.FileInput(attrs={
                'accept':'image/*',
                'capture':'environment'
            })
        }