from django.db import models  
from django.forms import fields  
from .models import UploadImage  
from django import forms  
  
  
class ImageForm(forms.ModelForm):
 
    class Meta:
        model = UploadImage
        fields = ['name','img', 'style']
