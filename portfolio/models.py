from django.db import models

# Create your models here.
from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(blank=True, null=True)

    # Store the ImageKit URL directly as a string
    image_url   = models.URLField(blank=True, null=True,
                                  help_text='Paste the ImageKit URL here')
 
    def get_image_url(self):
        """Returns the image URL (ImageKit CDN or placeholder)."""
        if self.image_url:
            return self.image_url
        return '/static/images/default.jpg'  # fallback


    def __str__(self):
        return self.title
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"