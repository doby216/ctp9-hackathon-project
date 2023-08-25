from django.db import models

styles = (
    ("Shinkai", "Shinkai"),
    ("Hayao", "Hayao"),
    ("Paprika", "Paprika"),
    ("Hosoda", "Hosoda")
)
# Create your models here.
def update_filename(instance, filename):
    filename = "input.png"
    return filename
class UploadImage(models.Model): 
    name = models.CharField(max_length=50, null=True)
    img = models.ImageField(upload_to=update_filename)
    style = models.CharField(max_length=50, choices=styles, default="Shinkai")
    
    def __str__(self):
        return self.title
    