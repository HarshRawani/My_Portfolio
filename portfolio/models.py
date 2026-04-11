from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(blank=True, null=True)

    image = models.ImageField(
                    upload_to='temp_uploads/',
                    blank=True, null=True,
                    help_text="Upload an image — it will be saved to ImageKit automatically."
                )
    image_url = models.URLField(blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        if self.image and not self.image_url:
            from .utils import upload_to_imagekit
            import os

            # ✅ Pass self.image (InMemoryUploadedFile), NOT self.image.file
            self.image_url = upload_to_imagekit(self.image, self.title)

            old_name   = self.image.name  # save before clearing
            self.image = None             # don't persist locally

            super().save(*args, **kwargs)

            # Clean up if it somehow landed on disk
            from django.conf import settings
            if old_name:
                local_path = os.path.join(settings.MEDIA_ROOT, old_name)
                if os.path.exists(local_path):
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