from django.contrib import admin
from .models import SiteSettings, HomePage

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'tagline', 'description')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url', 'linkedin_url', 'youtube_url')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords')
        }),
        ('Analytics', {
            'fields': ('google_analytics_id', 'facebook_pixel_id')
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False

@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Hero Section', {
            'fields': ('hero_title', 'hero_subtitle', 'hero_image', 'hero_video_url')
        }),
        ('About Section', {
            'fields': ('about_title', 'about_content', 'about_image')
        }),
        ('Services Section', {
            'fields': ('services_title', 'services_subtitle')
        }),
        ('Statistics', {
            'fields': ('universities_count', 'students_helped', 'success_rate', 'countries_served')
        }),
        ('Call to Action', {
            'fields': ('cta_title', 'cta_subtitle', 'cta_button_text')
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
    )
    
    list_display = ['hero_title', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at']

