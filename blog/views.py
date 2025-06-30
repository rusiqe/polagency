
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone

from .models import BlogPost, BlogCategory, BlogTag, InstagramFeed, Newsletter


def blog_home(request):
    """Blog homepage with featured posts and Instagram feed"""
    # Get featured posts
    featured_posts = BlogPost.objects.filter(
        status='published',
        is_featured=True
    ).select_related('author', 'category')[:3]
    
    # Get recent posts
    recent_posts = BlogPost.objects.filter(
        status='published'
    ).select_related('author', 'category')[:6]
    
    # Get Instagram feed
    instagram_posts = InstagramFeed.objects.filter(is_active=True)[:6]
    
    # Get categories
    categories = BlogCategory.objects.filter(is_active=True)
    
    context = {
        'featured_posts': featured_posts,
        'recent_posts': recent_posts,
        'instagram_posts': instagram_posts,
        'categories': categories,
    }
    
    return render(request, 'blog/home.html', context)

def post_list(request):
    """List all blog posts with filtering and pagination"""
    posts = BlogPost.objects.filter(status='published').select_related('author', 'category')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
    
    # Category filter
    category_slug = request.GET.get('category', '')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(BlogCategory, slug=category_slug)
        posts = posts.filter(category=selected_category)
    
    # Post type filter
    post_type = request.GET.get('type', '')
    if post_type:
        posts = posts.filter(post_type=post_type)
    
    # Tag filter
    tag_slug = request.GET.get('tag', '')
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)
    
    # Pagination
    paginator = Paginator(posts, 9)  # Show 9 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories and tags for filters
    categories = BlogCategory.objects.filter(is_active=True)
    popular_tags = BlogTag.objects.all()[:10]
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'selected_category': selected_category,
        'selected_type': post_type,
        'categories': categories,
        'popular_tags': popular_tags,
        'post_types': BlogPost.POST_TYPES,
    }
    
    return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
    """Display individual blog post with comments"""
    post = get_object_or_404(
        BlogPost.objects.select_related('author', 'category'),
        slug=slug,
        status='published'
    )
    
    # Increment view count
    BlogPost.objects.filter(id=post.id).update(view_count=F('view_count') + 1)
    
    
    # Get related posts
    related_posts = BlogPost.objects.filter(
        status='published',
        category=post.category
    ).exclude(id=post.id)[:3]
    
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    
    return render(request, 'blog/post_detail.html', context)


def category_posts(request, slug):
    """Display posts from a specific category"""
    category = get_object_or_404(BlogCategory, slug=slug, is_active=True)
    posts = BlogPost.objects.filter(
        status='published',
        category=category
    ).select_related('author', 'category')
    
    # Pagination
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    
    return render(request, 'blog/category_posts.html', context)

def tag_posts(request, slug):
    """Display posts with a specific tag"""
    tag = get_object_or_404(BlogTag, slug=slug)
    posts = tag.posts.filter(status='published').select_related('author', 'category')
    
    # Pagination
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
    }
    
    return render(request, 'blog/tag_posts.html', context)

def instagram_feed(request):
    """Display Instagram feed page"""
    instagram_posts = InstagramFeed.objects.filter(is_active=True)
    
    # Pagination
    paginator = Paginator(instagram_posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'blog/instagram_feed.html', context)

@csrf_exempt
def newsletter_subscribe(request):
    """Handle newsletter subscription"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        name = request.POST.get('name', '').strip()
        
        if not email:
            return JsonResponse({'success': False, 'message': 'Email is required.'})
        
        # Check if already subscribed
        if Newsletter.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': 'This email is already subscribed.'})
        
        try:
            Newsletter.objects.create(email=email, name=name)
            return JsonResponse({'success': True, 'message': 'Successfully subscribed to newsletter!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'An error occurred. Please try again.'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def search_posts(request):
    """Search posts with advanced filtering"""
    query = request.GET.get('q', '')
    posts = BlogPost.objects.filter(status='published')
    
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    # Pagination
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    
    return render(request, 'blog/search_results.html', context)


