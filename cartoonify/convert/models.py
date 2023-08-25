from django.db import models

# Create your models here.
def update_filename(instance, filename):
    filename = "input.png"
    return filename
class UploadImage(models.Model): 
    name = models.CharField(max_length=50, null=True)
    img = models.ImageField(upload_to=update_filename)

    def __str__(self):
        return self.title
    