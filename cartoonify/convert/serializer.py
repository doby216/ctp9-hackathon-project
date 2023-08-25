from rest_framework import serializers
from .models import DownloadImage

class DownloadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownloadImage
        fields = ['name','img_url', 'style']