from django.db import models

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default="Poland Study Agency")
    tagline = models.CharField(max_length=200, default="Your Gateway to Education in Poland")
    description = models.TextField(default="We help students plan and move to Poland for studies")
    
    # Contact Information
    email = models.EmailField(default="info@polandstudyagency.com")
    phone = models.CharField(max_length=20, default="+48 123 456 789")
    address = models.TextField(default="Warsaw, Poland")
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    # Analytics
    google_analytics_id = models.CharField(max_length=20, blank=True)
    facebook_pixel_id = models.CharField(max_length=20, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return self.site_name

class HomePage(models.Model):
    # Hero Section
    hero_title = models.CharField(max_length=200, default="Study in Poland with Confidence")
    hero_subtitle = models.TextField(default="Complete support from application to integration")
    hero_image = models.ImageField(upload_to='homepage/', blank=True)
    hero_video_url = models.URLField(blank=True)
    
    # About Section
    about_title = models.CharField(max_length=200, default="Why Choose Poland for Your Studies?")
    about_content = models.TextField()
    about_image = models.ImageField(upload_to='homepage/', blank=True)
    
    # Services Section
    services_title = models.CharField(max_length=200, default="Our Services")
    services_subtitle = models.TextField(blank=True)
    
    # Statistics
    universities_count = models.IntegerField(default=400)
    students_helped = models.IntegerField(default=1000)
    success_rate = models.IntegerField(default=95)
    countries_served = models.IntegerField(default=50)
    
    # CTA Section
    cta_title = models.CharField(max_length=200, default="Ready to Start Your Journey?")
    cta_subtitle = models.TextField(default="Get personalized guidance for your study abroad journey")
    cta_button_text = models.CharField(max_length=50, default="Get Started")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Homepage Content"
        verbose_name_plural = "Homepage Content"
    
    def __str__(self):
        return f"Homepage Content - {self.hero_title}"

