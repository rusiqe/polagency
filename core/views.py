from django.shortcuts import render
from django.db.models import Count
from .models import HomePage, SiteSettings
from services.models import ServicePackage, Testimonial
from blog.models import BlogPost, InstagramFeed

def home(request):
    """Homepage view"""
    # Get homepage content
    homepage = HomePage.objects.filter(is_active=True).first()
    if not homepage:
        # Create default homepage content if none exists
        homepage = HomePage.objects.create()
    
    # Get featured service packages
    featured_packages = ServicePackage.objects.filter(is_active=True, is_featured=True)[:3]
    
    # Get recent testimonials
    testimonials = Testimonial.objects.filter(is_approved=True, is_featured=True)[:6]
    
    # Get recent blog posts
    recent_posts = BlogPost.objects.filter(status='published')[:3]
    
    # Get Instagram posts
    instagram_posts = InstagramFeed.objects.filter(is_active=True)[:4]
    
    
    context = {
        'homepage': homepage,
        'featured_packages': featured_packages,
        'testimonials': testimonials,
        'recent_posts': recent_posts,
        'instagram_posts': instagram_posts,
        'university_stats': None,
    }
    
    return render(request, 'core/home.html', context)

def about(request):
    """About page view"""
    # Get testimonials for about page
    testimonials = Testimonial.objects.filter(is_approved=True)[:8]
    
    # Get some statistics
    stats = {
        'students_helped': 1000,  # This could be from orders or a separate model
        'success_rate': 95,
        'years_experience': 5,
    }
    
    context = {
        'testimonials': testimonials,
        'stats': stats,
    }
    
    return render(request, 'core/about.html', context)

def contact(request):
    """Contact page view"""
    return render(request, 'core/contact.html')

def privacy_policy(request):
    """Privacy policy page"""
    return render(request, 'core/privacy_policy.html')

def terms_of_service(request):
    """Terms of service page"""
    return render(request, 'core/terms_of_service.html')

def sitemap(request):
    """Sitemap page for SEO"""
    # Get all public URLs
    blog_posts = BlogPost.objects.filter(status='published')[:50]
    service_packages = ServicePackage.objects.filter(is_active=True)
    
    context = {
        'universities': None,
        'blog_posts': blog_posts,
        'service_packages': service_packages,
    }
    
    return render(request, 'core/sitemap.html', context)

