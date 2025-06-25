# Poland Study Agency - Django Website

A comprehensive Django-based agency website that helps students plan and move to Poland for studies.

## 🌟 Features

### Core Functionality
- **University Search**: Comprehensive database of Polish universities with advanced filtering
- **Support Bot**: AI-powered chatbot for instant student assistance
- **Service Packages**: Three-tier consulting service packages ($250, $500, $750)
- **Blog System**: Integrated blog with Instagram feed support
- **Admin Panel**: Full Django admin interface for content management

### Service Packages
1. **Basic Support Package ($250)**
   - University selection guidance
   - Application document review
   - Visa requirements checklist
   - Basic interview tips
   - Accommodation recommendations
   - Pre-arrival information package

2. **Complete Support Package ($500)** ⭐ Featured
   - Personal agent for university applications
   - Direct communication with admissions officers
   - Complete document folder preparation
   - Interview preparation and coaching
   - Visa process assistance
   - Airport arrival and pickup
   - Hostel/accommodation initiation
   - Integration into Polish society

3. **Premium Support Package ($750)**
   - All Complete Package features
   - Priority application processing
   - Multiple university applications
   - Scholarship application assistance
   - 24/7 support hotline
   - First month accommodation included
   - City orientation tour
   - 6-month follow-up support

## 🏗️ Technical Architecture

### Django Apps Structure
```
poland_study_agency/
├── core/           # Homepage and main pages
├── universities/   # University search and database
├── support/        # Chatbot and support system
├── services/       # Service packages and orders
├── blog/          # Blog and Instagram integration
├── static/        # CSS, JS, images
└── templates/     # HTML templates
```

### Database Models
- **Universities**: University information, programs, locations
- **Service Packages**: Consulting service offerings
- **Orders**: Customer purchases and tracking
- **Blog Posts**: Content management with categories and tags
- **Support System**: Chat sessions, FAQ, contact requests
- **Instagram Feed**: Social media integration

### Key Technologies
- **Backend**: Django 5.2.3, Python 3.11
- **Frontend**: Bootstrap 5.3, HTML5, CSS3, JavaScript
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Styling**: Custom CSS with Polish flag colors (red/white/gold)
- **Icons**: Font Awesome 6.4
- **Fonts**: Inter (Google Fonts)

## 🚀 Installation & Setup

### Prerequisites
- Python 3.11+
- pip package manager

### Quick Start
1. **Clone the repository**
   ```bash
   cd poland_study_agency
   ```

2. **Install dependencies**
   ```bash
   pip install django
   ```

3. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start development server**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

6. **Access the website**
   - Website: http://localhost:8000
   - Admin: http://localhost:8000/admin

## 📱 Pages & Functionality

### Public Pages
- **Homepage** (`/`): Hero section, services overview, statistics, testimonials
- **About** (`/about/`): Company information and team details
- **Universities** (`/universities/`): Searchable university database
- **Services** (`/services/`): Service packages and pricing
- **Blog** (`/blog/`): Articles and Instagram integration
- **Support** (`/support/`): Chatbot and FAQ
- **Contact** (`/contact/`): Contact form and information

### Admin Features
- University management
- Service package configuration
- Order tracking and management
- Blog content creation
- Instagram feed management
- Customer support tools

## 🎨 Design Features

### Visual Design
- **Color Scheme**: Polish flag inspired (Red #dc143c, White #ffffff, Gold #ffd700)
- **Typography**: Inter font family for modern, clean look
- **Layout**: Responsive Bootstrap-based design
- **Icons**: Font Awesome for consistent iconography

### User Experience
- **Mobile-First**: Fully responsive design
- **Fast Loading**: Optimized CSS and JavaScript
- **Accessibility**: Semantic HTML and ARIA labels
- **SEO-Friendly**: Meta tags and structured content

## 🤖 Support Bot Features

### Chatbot Functionality
- Session-based conversations
- FAQ integration
- Admin connection system
- Real-time messaging
- Mobile-friendly interface

### Support Features
- Live chat widget
- FAQ accordion
- Contact form integration
- Admin notification system

## 📝 Content Management

### Blog System
- **Post Types**: Article, News, Guide, Instagram, Video
- **Categories**: Organized content classification
- **Tags**: Flexible content labeling
- **Comments**: Moderated user engagement
- **Instagram Integration**: Manual and API-ready

### Instagram Integration
- Manual content management
- Embed code support
- Future API integration ready
- Mobile-optimized display

## 🛒 E-commerce Features

### Service Packages
- Three-tier pricing structure
- Feature comparison
- Purchase tracking
- Customer testimonials
- Progress monitoring

### Order Management
- Customer information collection
- Payment integration ready
- Order status tracking
- Progress updates
- Communication tools

## 🔧 Configuration

### Settings
- **Debug Mode**: Set to False for production
- **Allowed Hosts**: Configure for your domain
- **Database**: SQLite for development, PostgreSQL recommended for production
- **Static Files**: Configured for CDN deployment
- **Media Files**: User upload handling

### Environment Variables
```python
# Key settings to configure
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECRET_KEY = 'your-secret-key'
```

## 📊 Analytics & SEO

### SEO Features
- Meta descriptions and keywords
- Open Graph tags
- Structured data ready
- Sitemap generation
- Clean URL structure

### Analytics Ready
- Google Analytics integration points
- Facebook Pixel support
- Custom event tracking
- Performance monitoring

## 🔒 Security Features

### Django Security
- CSRF protection
- SQL injection prevention
- XSS protection
- Secure headers
- User authentication

### Data Protection
- Form validation
- Input sanitization
- File upload security
- Session management

## 🌐 Deployment

### Production Checklist
- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up PostgreSQL database
- [ ] Configure static file serving
- [ ] Set up SSL certificate
- [ ] Configure email backend
- [ ] Set up monitoring

### Recommended Hosting
- **Platform**: Heroku, DigitalOcean, AWS
- **Database**: PostgreSQL
- **Static Files**: AWS S3 or CDN
- **Domain**: Custom domain with SSL

## 📞 Support & Maintenance

### Admin Tasks
- Regular database backups
- Content moderation
- University database updates
- Performance monitoring
- Security updates

### User Support
- Chatbot management
- FAQ updates
- Customer service
- Technical support

## 🎯 Future Enhancements

### Planned Features
- Payment gateway integration (Stripe/PayPal)
- Real Instagram API integration
- Multi-language support (Polish/English)
- Advanced university filtering
- Student portal
- Mobile app

### Technical Improvements
- Caching implementation
- API development
- Performance optimization
- Advanced analytics
- Automated testing

## 📄 License & Credits

### Technologies Used
- Django Framework
- Bootstrap CSS Framework
- Font Awesome Icons
- Google Fonts (Inter)
- jQuery for interactions

### Development Notes
- Built with modern web standards
- Responsive design principles
- SEO best practices
- Security-first approach
- Scalable architecture

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

### Code Standards
- PEP 8 Python style guide
- Clean, commented code
- Responsive design
- Cross-browser compatibility
- Performance optimization

---

**Poland Study Agency** - Your Gateway to Education in Poland 🇵🇱

For support or questions, contact: info@polandstudyagency.com

