from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import BlogCategory, BlogPost, BlogComment, BlogTag, InstagramFeed, Newsletter

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color_preview', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'order']
    
    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc;"></div>',
            obj.color
        )
    color_preview.short_description = 'Color'

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'post_type', 'status', 'is_featured', 'published_at', 'view_count']
    list_filter = ['status', 'post_type', 'category', 'is_featured', 'created_at', 'author']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'is_featured']
    date_hierarchy = 'published_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category', 'post_type')
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'featured_image')
        }),
        ('Instagram Integration', {
            'fields': ('instagram_post_url', 'instagram_embed_code'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Publishing', {
            'fields': ('status', 'is_featured', 'allow_comments', 'published_at')
        }),
    )
    
    readonly_fields = ['view_count']
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new post
            obj.author = request.user
        if obj.status == 'published' and not obj.published_at:
            obj.published_at = timezone.now()
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'category')

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'name', 'email', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'content', 'post__title']
    list_editable = ['status']
    readonly_fields = ['ip_address', 'user_agent', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Comment Information', {
            'fields': ('post', 'name', 'email', 'website', 'content')
        }),
        ('Moderation', {
            'fields': ('status', 'parent')
        }),
        ('Technical Information', {
            'fields': ('ip_address', 'user_agent', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('post')

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    
    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Posts'

@admin.register(InstagramFeed)
class InstagramFeedAdmin(admin.ModelAdmin):
    list_display = ['instagram_id', 'caption_preview', 'media_type', 'timestamp', 'is_active']
    list_filter = ['media_type', 'is_active', 'timestamp']
    search_fields = ['instagram_id', 'caption', 'manual_caption']
    list_editable = ['is_active']
    readonly_fields = ['instagram_id', 'timestamp', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Instagram Data', {
            'fields': ('instagram_id', 'caption', 'image_url', 'permalink', 'timestamp', 'media_type')
        }),
        ('Manual Override', {
            'fields': ('manual_caption', 'manual_image'),
            'description': 'Use these fields to override Instagram data or add content manually'
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def caption_preview(self, obj):
        caption = obj.get_display_caption()
        return caption[:50] + "..." if len(caption) > 50 else caption
    caption_preview.short_description = 'Caption'

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at', 'categories']
    search_fields = ['email', 'name']
    list_editable = ['is_active']
    readonly_fields = ['subscribed_at', 'unsubscribed_at']
    
    fieldsets = (
        ('Subscriber Information', {
            'fields': ('email', 'name')
        }),
        ('Preferences', {
            'fields': ('categories', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('subscribed_at', 'unsubscribed_at'),
            'classes': ('collapse',)
        }),
    )

