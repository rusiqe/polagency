# Deployment Guide - Poland Study Agency

## 🚀 Quick Deployment Options

### Option 1: Local Development
```bash
cd poland_study_agency
python manage.py runserver 0.0.0.0:8000
```
Access at: http://localhost:8000

### Option 2: Production Deployment

#### Using Heroku
1. Install Heroku CLI
2. Create Heroku app
3. Configure environment variables
4. Deploy with Git

#### Using DigitalOcean/VPS
1. Set up Ubuntu server
2. Install Python, PostgreSQL, Nginx
3. Configure Django settings
4. Set up SSL certificate

## 🔧 Configuration Steps

### 1. Environment Setup
```python
# settings.py changes for production
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'poland_study_agency',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 2. Static Files
```python
# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### 3. Security Settings
```python
# Security settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

## 📊 Admin Setup

### Default Admin Credentials
- Username: admin
- Email: admin@polandstudyagency.com
- Password: admin123

**⚠️ IMPORTANT: Change these credentials immediately in production!**

### Admin Tasks
1. **Create Homepage Content**
   - Go to Core > Homepage Content
   - Add hero section content
   - Upload images
   - Set statistics

2. **Add Service Packages**
   - Go to Services > Service Packages
   - Create the three packages ($250, $500, $750)
   - Mark the $500 package as featured
   - Add detailed features

3. **Setup Universities**
   - Go to Universities > Universities
   - Add Polish universities
   - Include logos and descriptions
   - Set up study programs

4. **Configure Blog**
   - Go to Blog > Blog Categories
   - Create content categories
   - Add initial blog posts
   - Set up Instagram feed

## 🌐 Domain & SSL

### Domain Setup
1. Point domain to server IP
2. Configure DNS records
3. Set up SSL certificate (Let's Encrypt recommended)
4. Update ALLOWED_HOSTS in settings

### SSL Certificate
```bash
# Using Certbot for Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## 📧 Email Configuration

### SMTP Setup
```python
# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## 🔍 SEO Configuration

### Google Analytics
1. Create Google Analytics account
2. Add tracking ID to settings
3. Update base template with tracking code

### Search Console
1. Verify domain ownership
2. Submit sitemap
3. Monitor search performance

## 🛡️ Security Checklist

- [ ] Change default admin password
- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up SSL certificate
- [ ] Configure secure headers
- [ ] Set up database backups
- [ ] Configure error logging
- [ ] Set up monitoring

## 📱 Testing Checklist

### Functionality Tests
- [ ] Homepage loads correctly
- [ ] University search works
- [ ] Service packages display
- [ ] Support chat functions
- [ ] Blog pages work
- [ ] Admin panel accessible
- [ ] Forms submit properly
- [ ] Mobile responsiveness

### Performance Tests
- [ ] Page load times < 3 seconds
- [ ] Images optimized
- [ ] CSS/JS minified
- [ ] Database queries optimized

## 🔧 Maintenance

### Regular Tasks
- Update university database
- Moderate blog comments
- Review support chat logs
- Monitor server performance
- Update content regularly

### Backup Strategy
- Daily database backups
- Weekly full site backups
- Media files backup
- Configuration backup

## 📞 Support

### Technical Issues
- Check Django logs
- Monitor server resources
- Review error reports
- Contact hosting support

### Content Updates
- Use Django admin panel
- Follow content guidelines
- Test changes on staging
- Monitor user feedback

---

**Ready to launch your Poland Study Agency website!** 🚀

