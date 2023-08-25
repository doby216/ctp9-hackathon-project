from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import ImageForm
import subprocess, os

def upload(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        remove_image('media')
        if form.is_valid():
            form.save()
            subprocess.call(["python", "convert/CartoonGAN/convert.py"])
            return redirect("result")
    else:
        form = ImageForm()
    return render(request,'index.html', {'form': form})

def result(request):
    return render(request,'result.html')

def remove_image(dir):
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))