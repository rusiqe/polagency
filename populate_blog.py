#!/usr/bin/env python
import os
import django
import random
from datetime import timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poland_study_agency.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import BlogCategory, BlogPost
from django.utils.text import slugify
from django.utils import timezone

# Get author and category
author = User.objects.filter(is_superuser=True).first()
category = BlogCategory.objects.first()

if not author or not category:
    print('Please create a superuser and a blog category first.')
    exit()

titles = [
    'Top 5 Nursing Programs in Poland for International Students',
    'How to Study Nursing in Poland on a Budget: A Complete Guide',
    'Poland Student Visa for African Citizens: A Step-by-Step Guide',
    'Why You Need an Education Agent for Your Poland University Application',
    'From Lagos to Warsaw: A Nigerian Student\'s Nursing Journey in Poland',
    'Is a Polish Nursing Degree Recognized Internationally? All You Need to Know',
    'Choosing the Best Study Abroad Consultant for Poland: 5 Key Questions to Ask',
    'Cost of Living in Warsaw vs. Krakow for African Students in 2025',
    'Admission Requirements for Top Nursing Schools in Poland',
    'Career Opportunities After Graduating from a Polish Nursing School'
]

for i, title in enumerate(titles):
    if not BlogPost.objects.filter(title=title).exists():
        content = f"""## {title}

This is a comprehensive guide about **{title}**. Poland has become an increasingly popular destination for international students, especially those from Africa seeking quality nursing education.

### Key Benefits of Studying Nursing in Poland

- **High-quality education standards** - Polish universities follow European education standards
- **Affordable tuition and living costs** - Much more affordable than Western European countries
- **English-taught programs** - Many programs are available in English
- **Globally recognized degrees** - Degrees are recognized worldwide
- **Rich cultural experience** - Experience European culture while studying

### Getting Started

When considering nursing studies in Poland, it's important to:

1. Research different universities and their requirements
2. Understand the visa application process
3. Plan your finances and accommodation
4. Connect with education agents for guidance

### Next Steps

For more detailed information about studying nursing in Poland, contact our experienced education consultants who specialize in helping African students achieve their academic dreams in Poland.

**Ready to start your journey?** Get in touch with us today!
"""
        
        post = BlogPost.objects.create(
            author=author,
            category=category,
            title=title,
            slug=slugify(title),
            excerpt=f'A comprehensive guide to {title.lower()}. Learn about the key requirements, benefits, and steps to get started.',
            content=content,
            status='published',
            published_at=timezone.now() - timedelta(days=i*2),
            view_count=random.randint(150, 2000),
            meta_keywords='nursing study Poland, African students, education agents, study abroad, nursing programs',
            is_featured=(i < 3)  # Make first 3 posts featured
        )
        print(f'Created post: {post.title}')
    else:
        print(f'Post already exists: {title}')

print(f'Blog population complete! Total posts: {BlogPost.objects.count()}')
