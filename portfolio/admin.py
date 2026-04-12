from django.contrib import admin
from django.utils.html import format_html
from .models import Project, ProjectImage, Contact


class ProjectImageInline(admin.TabularInline):
    model           = ProjectImage
    extra           = 3
    fields          = ('image', 'image_url_display', 'is_main', 'caption', 'thumbnail')
    readonly_fields = ('image_url_display', 'thumbnail')

    def image_url_display(self, obj):
        return obj.image_url or '—'
    image_url_display.short_description = 'ImageKit URL'

    def thumbnail(self, obj):
        url = obj.get_url()
        if url != '/static/images/default.jpg':
            return format_html('<img src="{}" style="height:60px;border-radius:4px;object-fit:cover;">', url)
        return '—'
    thumbnail.short_description = 'Preview'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_count', 'has_main_image', 'link')
    inlines      = [ProjectImageInline]
    fieldsets    = (
        ('Project Details', {'fields': ('title', 'description', 'link')}),
    )

    def image_count(self, obj):
        return obj.images.count()
    image_count.short_description = '# Images'

    def has_main_image(self, obj):
        return '✅' if obj.images.filter(is_main=True).exists() else '❌'
    has_main_image.short_description = 'Main Set'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display    = ('name', 'email', 'subject', 'created_at')
    readonly_fields = ('created_at',)