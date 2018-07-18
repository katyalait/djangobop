from django import forms
from .models import User_Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = User_Image
        fields = ['image', 'name']
    
