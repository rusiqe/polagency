# Generated by Django 5.2.3 on 2025-06-24 11:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('description', models.TextField(blank=True)),
                ('color', models.CharField(default='#007bff', help_text='Hex color code', max_length=7)),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Blog Categories',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='InstagramFeed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instagram_id', models.CharField(max_length=100, unique=True)),
                ('caption', models.TextField(blank=True)),
                ('image_url', models.URLField()),
                ('permalink', models.URLField()),
                ('timestamp', models.DateTimeField()),
                ('media_type', models.CharField(max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('manual_caption', models.TextField(blank=True, help_text='Manual caption override')),
                ('manual_image', models.ImageField(blank=True, upload_to='instagram/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('post_type', models.CharField(choices=[('article', 'Article'), ('news', 'News'), ('guide', 'Guide'), ('instagram', 'Instagram Post'), ('video', 'Video')], default='article', max_length=15)),
                ('excerpt', models.TextField(help_text='Brief description for previews', max_length=300)),
                ('content', models.TextField()),
                ('featured_image', models.ImageField(blank=True, upload_to='blog/images/')),
                ('instagram_post_url', models.URLField(blank=True, help_text='Instagram post URL for embedding')),
                ('instagram_embed_code', models.TextField(blank=True, help_text='Instagram embed code')),
                ('meta_description', models.CharField(blank=True, max_length=160)),
                ('meta_keywords', models.CharField(blank=True, max_length=255)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published'), ('archived', 'Archived')], default='draft', max_length=10)),
                ('is_featured', models.BooleanField(default=False)),
                ('allow_comments', models.BooleanField(default=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.blogcategory')),
            ],
            options={
                'ordering': ['-published_at', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('website', models.URLField(blank=True)),
                ('content', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Pending Approval'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('ip_address', models.GenericIPAddressField()),
                ('user_agent', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='blog.blogcomment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.blogpost')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='BlogTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('posts', models.ManyToManyField(blank=True, related_name='tags', to='blog.blogpost')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('subscribed_at', models.DateTimeField(auto_now_add=True)),
                ('unsubscribed_at', models.DateTimeField(blank=True, null=True)),
                ('categories', models.ManyToManyField(blank=True, to='blog.blogcategory')),
            ],
            options={
                'ordering': ['-subscribed_at'],
            },
        ),
    ]
