from django.shortcuts import render, redirect
from django.conf import settings
from .forms import ImageForm
from .serializer import DownloadImageSerializer
from rest_framework import status
import subprocess, os
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(["POST", "GET"])
def upload(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        remove_image('media')
        if form.is_valid():
            form.save()
            style = form["style"].value()
            subprocess.run(["python3", "convert/CartoonGAN/convert.py", "--style",style])
            data = {
            'name' : request.data.get('name'),
            'style' : request.data.get('style'),
            'img_url': "http://208.167.255.60/media/output.png"
            }
            serializer = DownloadImageSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                res = Response(serializer.data, status=status.HTTP_201_CREATED)
                res['Access-Control-Allow-Origin'] = '*'
                res['Access-Control-Allow-Headers'] = 'Content-Type'
                res['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
                return res
    else:
        form = ImageForm()
        return render(request,'index.html', {'form': form})

def result(request):
    return render(request,'result.html')

def remove_image(dir):
    if len(os.listdir(dir)) > 0:
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
