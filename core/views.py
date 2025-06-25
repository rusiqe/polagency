from django.shortcuts import render
from django.db.models import Count
from .models import HomePage, SiteSettings
from universities.models import University
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
    
    # Get university statistics
    university_stats = {
        'total_universities': University.objects.count(),
        'public_universities': University.objects.filter(university_type='public').count(),
        'private_universities': University.objects.filter(university_type='private').count(),
        'english_programs': University.objects.filter(english_programs=True).count(),
    }
    
    context = {
        'homepage': homepage,
        'featured_packages': featured_packages,
        'testimonials': testimonials,
        'recent_posts': recent_posts,
        'instagram_posts': instagram_posts,
        'university_stats': university_stats,
    }
    
    return render(request, 'core/home.html', context)

def about(request):
    """About page view"""
    # Get testimonials for about page
    testimonials = Testimonial.objects.filter(is_approved=True)[:8]
    
    # Get some statistics
    stats = {
        'universities': University.objects.count(),
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
    if request.method == 'POST':
        # Handle contact form submission
        # This could integrate with the support app's ContactRequest model
        pass
    
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
    universities = University.objects.all()[:50]  # Limit for performance
    blog_posts = BlogPost.objects.filter(status='published')[:50]
    service_packages = ServicePackage.objects.filter(is_active=True)
    
    context = {
        'universities': universities,
        'blog_posts': blog_posts,
        'service_packages': service_packages,
    }
    
    return render(request, 'core/sitemap.html', context)

