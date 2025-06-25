from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff', help_text="Hex color code")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Blog Categories"
        ordering = ['order', 'name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class BlogPost(models.Model):
    POST_STATUS = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    POST_TYPES = [
        ('article', 'Article'),
        ('news', 'News'),
        ('guide', 'Guide'),
        ('instagram', 'Instagram Post'),
        ('video', 'Video'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True)
    post_type = models.CharField(max_length=15, choices=POST_TYPES, default='article')
    
    # Content fields
    excerpt = models.TextField(max_length=300, help_text="Brief description for previews")
    content = models.TextField()
    featured_image = models.ImageField(upload_to='blog/images/', blank=True)
    
    # Instagram integration fields
    instagram_post_url = models.URLField(blank=True, help_text="Instagram post URL for embedding")
    instagram_embed_code = models.TextField(blank=True, help_text="Instagram embed code")
    
    # SEO and metadata
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    # Status and visibility
    status = models.CharField(max_length=10, choices=POST_STATUS, default='draft')
    is_featured = models.BooleanField(default=False)
    allow_comments = models.BooleanField(default=True)
    
    # Timestamps
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Analytics
    view_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.title

class BlogComment(models.Model):
    COMMENT_STATUS = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField(blank=True)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=COMMENT_STATUS, default='pending')
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    
    # Reply functionality
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"

class BlogTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    posts = models.ManyToManyField(BlogPost, blank=True, related_name='tags')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class InstagramFeed(models.Model):
    """Model to store Instagram posts for display on the website"""
    instagram_id = models.CharField(max_length=100, unique=True)
    caption = models.TextField(blank=True)
    image_url = models.URLField()
    permalink = models.URLField()
    timestamp = models.DateTimeField()
    media_type = models.CharField(max_length=20)  # IMAGE, VIDEO, CAROUSEL_ALBUM
    is_active = models.BooleanField(default=True)
    
    # Manual fields for when API is not available
    manual_caption = models.TextField(blank=True, help_text="Manual caption override")
    manual_image = models.ImageField(upload_to='instagram/', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Instagram Post {self.instagram_id}"
    
    def get_display_caption(self):
        return self.manual_caption if self.manual_caption else self.caption
    
    def get_display_image(self):
        return self.manual_image.url if self.manual_image else self.image_url

class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    
    # Preferences
    categories = models.ManyToManyField(BlogCategory, blank=True)
    
    class Meta:
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email

