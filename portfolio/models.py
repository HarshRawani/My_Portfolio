from django.db import models

# Create your models here.
from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(blank=True, null=True)

    # Upload widget in Admin — temp storage only
    image       = models.ImageField(
                    upload_to='temp_uploads/',
                    blank=True, null=True,
                    help_text="Upload an image — it will be saved to ImageKit automatically."
                  )

    # Final CDN URL stored after ImageKit upload
    image_url   = models.URLField(blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        # If a new image file was just uploaded
        if self.image and not self.image_url:
            from .utils import upload_to_imagekit
            import os

            # Upload to ImageKit
            self.image_url = upload_to_imagekit(self.image.file, self.title)

            # Clear the local ImageField so nothing is saved to disk
            local_path = self.image.path if self.image.name else None
            self.image = None  # don't save locally

            super().save(*args, **kwargs)

            # Delete the temp file from disk
            if local_path and os.path.exists(local_path):
                os.remove(local_path)
        else:
            super().save(*args, **kwargs)

    def get_image_url(self):
        return self.image_url or '/static/images/default.jpg'

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