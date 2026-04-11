from django.contrib import admin
from .models import Project, Contact

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display  = ('title', 'has_image', 'link')
    readonly_fields = ('image_url', 'image_preview')

    fieldsets = (
        ('Project Details', {
            'fields': ('title', 'description', 'link')
        }),
        ('Image', {
            'fields': ('image', 'image_url', 'image_preview'),
            'description': 'Upload an image below. It will be pushed to ImageKit automatically.'
        }),
    )

    def has_image(self, obj):
        return '✅' if obj.image_url else '❌'
    has_image.short_description = 'Image'

    def image_preview(self, obj):
        from django.utils.html import format_html
        if obj.image_url:
            return format_html('<img src="{}" style="max-height:150px; border-radius:6px;">', obj.image_url)
        return "No image yet."
    image_preview.short_description = 'Preview'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'subject', 'created_at')
    readonly_fields = ('created_at',)