from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#a78bfa')

    def __str__(self):
        return self.name

class Project(models.Model):
    title       = models.CharField(max_length=200)
    description = models.TextField()
    link        = models.URLField(blank=True, null=True)
    tags        = models.ManyToManyField(Tag, blank=True)
    is_archived = models.BooleanField(default=False)


    def get_main_image_url(self):
        main = self.images.filter(is_main=True).first()
        if main:
            return main.get_url()
        first = self.images.first()
        if first:
            return first.get_url()
        return '/static/images/default.jpg'

    def get_all_images(self):
        return self.images.all()

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project   = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image     = models.ImageField(upload_to='temp_uploads/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True, editable=False)
    is_main   = models.BooleanField(default=False, help_text="Use as cover image for the project card.")
    caption   = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-is_main', 'id']

    def save(self, *args, **kwargs):
        if self.image and not self.image_url:
            from .utils import upload_to_imagekit
            import os
            self.image_url = upload_to_imagekit(self.image, self.project.title)
            old_name = self.image.name
            self.image = None
            super().save(*args, **kwargs)
            from django.conf import settings
            if old_name:
                local_path = os.path.join(settings.MEDIA_ROOT, old_name)
                if os.path.exists(local_path):
                    os.remove(local_path)
        else:
            super().save(*args, **kwargs)

        if self.is_main:
            ProjectImage.objects.filter(project=self.project, is_main=True).exclude(pk=self.pk).update(is_main=False)

    def get_url(self):
        return self.image_url or '/static/images/default.jpg'

    def __str__(self):
        return f"{self.project.title} — image {self.pk}{' ★' if self.is_main else ''}"


class Contact(models.Model):
    name       = models.CharField(max_length=100)
    email      = models.EmailField()
    subject    = models.CharField(max_length=200, blank=True)
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"