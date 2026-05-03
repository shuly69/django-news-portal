# NewsHub - Professional News Platform

A full-featured, production-ready news aggregation and content management platform built with Django. This project demonstrates enterprise-level web development capabilities, featuring custom user authentication, content management, advanced search functionality, and a modern, responsive user interface.

**Live Demo:** [https://newsproject-m07i.onrender.com/](https://newsproject-m07i.onrender.com/)

---

## 🎯 Project Overview

NewsHub is a comprehensive news platform that enables users to discover, create, and manage news articles across multiple categories. The platform serves as a demonstration of full-stack development expertise, showcasing proficiency in backend architecture, database design, user authentication, content management, and modern web development practices.

---

## ✨ Key Features

### 🔐 Authentication & User Management
- **Custom User Registration System**: Email-based registration with comprehensive user profile creation
- **Secure Authentication**: Custom login system with "Remember Me" functionality and session management
- **User Profiles**: Detailed user profiles with bio, specialization, and avatar support
- **Account Management**: Complete user dashboard for managing personal information and account settings
- **Password Management**: Secure password change functionality with validation

### 📝 Content Management System
- **Article Creation**: Rich text editor (Quill) for creating formatted articles with images
- **Article Editing**: Full CRUD operations for article management
- **Draft System**: Save articles as drafts before publishing
- **SEO Optimization**: Meta descriptions and keywords for each article
- **Image Management**: Cloudinary integration for efficient image storage and delivery
- **Slug Generation**: Automatic URL-friendly slug generation for articles

### 🔍 Search & Discovery
- **Full-Text Search**: PostgreSQL-powered search across article titles, content, and excerpts
- **Category Browsing**: Organized content by categories (News, Technology, Sport, Lifestyle, Business, Culture)
- **Subcategory Filtering**: Advanced filtering by subcategories within main categories
- **Date Sorting**: Sort articles by newest or oldest publication date
- **Pagination**: Efficient pagination for large article collections

### 📊 User Dashboard
- **Article Management**: View all user-created articles in a centralized dashboard
- **Quick Actions**: Edit and delete articles directly from the dashboard
- **Account Settings**: Comprehensive settings page for updating profile information
- **Activity Tracking**: Monitor article publication status and dates

### 🎨 User Interface
- **Responsive Design**: Mobile-first, fully responsive layout
- **Modern UI/UX**: Clean, professional interface with intuitive navigation
- **Breadcrumb Navigation**: Clear navigation hierarchy throughout the application
- **Category Pages**: Dedicated pages for each category with featured articles
- **Article Detail Pages**: Rich article viewing experience with author information

### 🚀 Production Features
- **Cloud Storage**: Cloudinary integration for media file management
- **Database**: PostgreSQL for robust data management
- **Static File Management**: WhiteNoise for efficient static file serving
- **Environment Configuration**: Secure environment variable management
- **Deployment Ready**: Configured for production deployment on Render

---

## 🛠️ Technology Stack

### Backend
- **Django 4.2.24**: High-level Python web framework
- **PostgreSQL**: Advanced relational database system
- **Gunicorn**: Production-ready WSGI HTTP server
- **WhiteNoise**: Efficient static file serving

### Frontend
- **HTML5/CSS3**: Modern markup and styling
- **JavaScript**: Interactive user interface elements
- **Quill Editor**: Rich text editing capabilities
- **Responsive Design**: Mobile-first approach

### Third-Party Services
- **Cloudinary**: Cloud-based image and video management
- **Render**: Cloud hosting platform for deployment

### Development Tools
- **Django Debug Toolbar**: Development debugging assistance
- **django-environ**: Environment variable management
- **python-dotenv**: Environment configuration

---

## 📁 Project Structure

```
newsproject/
├── articles/              # Article management application
│   ├── models.py         # Article, Category, SubCategory models
│   ├── views.py          # Article views (CRUD, search, category)
│   ├── forms.py          # Article creation/editing forms
│   ├── urls.py           # Article URL routing
│   └── templates/        # Article-related templates
├── user/                  # User management application
│   ├── models.py         # CustomUser model
│   ├── views.py          # Authentication and profile views
│   ├── forms.py          # Registration and authentication forms
│   ├── urls.py           # User URL routing
│   └── templates/        # User-related templates
├── newsproject/           # Main project configuration
│   ├── settings.py       # Django settings
│   ├── urls.py           # Root URL configuration
│   └── wsgi.py           # WSGI configuration
├── templates/             # Base templates and shared layouts
├── static/                # Static files (CSS, JavaScript)
├── media/                 # Media files (user uploads)
├── requirements.txt       # Python dependencies
└── manage.py             # Django management script
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- PostgreSQL database
- Cloudinary account (for media storage)
- SMTP server credentials (for email functionality)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd news
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   cd newsproject
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the `newsproject` directory with the following variables:
   ```env
   DJANGO_SECRET_KEY=your-secret-key
   DB_NAME=your-database-name
   DB_USER=your-database-user
   DB_PASSWORD=your-database-password
   DB_HOST=your-database-host
   CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
   CLOUDINARY_API_KEY=your-cloudinary-api-key
   CLOUDINARY_API_SECRET=your-cloudinary-api-secret
   E_HOST=your-smtp-host
   E_PORT=your-smtp-port
   E_NAME=your-email-username
   E_PASSWORD=your-email-password
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Application: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

---

## 🌐 Deployment

The application is currently deployed on Render and configured for production use. The deployment includes:

- **Database**: PostgreSQL on Render
- **Static Files**: Served via WhiteNoise
- **Media Files**: Stored on Cloudinary
- **WSGI Server**: Gunicorn for production serving

### Deployment Configuration
- `gunicorn_config.py`: Gunicorn server configuration
- `build.sh`: Build script for deployment
- `Dockerfile`: Docker containerization (optional)
- `entrypoint.sh`: Entry point script for containerized deployment

---

## 👤 Demo Credentials

For demonstration purposes, the following test accounts are available:

| Email | Password |
|-------|----------|
| sss@gmail.com | 1212 |
| zzz@gmail.com | 1212 |
| xxx@gmail.com | 1212 |

**Note**: These are demonstration accounts. Please use responsibly.

---

## 🔮 Planned Enhancements

The following features are planned for future implementation to enhance the platform's functionality and user experience:

### Authentication Improvements
- **Email Verification**: Email confirmation system for new user registrations
- **Password Reset**: Secure password reset functionality via email
- **Social Authentication**: OAuth integration with Google and Facebook for seamless login

### User Experience Enhancements
- **Favorites/Bookmarks**: Allow users to save and organize favorite articles
- **Newsletter System**: Email newsletter subscription and management
- **User Notifications**: Real-time notifications for article updates and interactions

### Content Features
- **Interactive Elements**: Enhanced article interactivity with polls, quizzes, and embedded media
- **News Feeds**: Personalized news feed based on user preferences and reading history
- **Video Content**: Support for video formats and embedded video players
- **Mini Games**: Engaging interactive games and quizzes related to news content

### Advanced Functionality
- **Comment System**: User comments and discussions on articles
- **Rating System**: Article rating and review functionality
- **Tag System**: Enhanced content organization with tags
- **Analytics Dashboard**: Content performance analytics for authors
- **API Development**: RESTful API for third-party integrations

---

## 📊 Database Schema

### CustomUser Model
- Email (unique identifier)
- Username
- First Name, Last Name
- Bio
- Specialization (category preference)
- Avatar (Cloudinary field)

### Articles Model
- Title
- Content (rich text)
- Excerpt
- Slug (URL-friendly identifier)
- Category (Foreign Key)
- Subcategory (Foreign Key, optional)
- Image (Cloudinary field)
- Meta Description & Keywords (SEO)
- Status (Draft/Published)
- Published Date
- User (Author, Foreign Key)

### Categories & SubCategories
- Hierarchical category structure
- Slug-based URL routing
- Description fields

---

## 🔒 Security Features

- **CSRF Protection**: Django's built-in CSRF protection
- **Password Hashing**: Secure password storage using Django's password hashers
- **Session Management**: Configurable session expiration
- **SQL Injection Prevention**: Django ORM protection
- **XSS Protection**: Template auto-escaping
- **Environment Variables**: Sensitive data stored securely

---

## 📈 Performance Optimizations

- **Database Indexing**: Optimized queries with proper indexing
- **Static File Compression**: WhiteNoise compression for static assets
- **Cloudinary CDN**: Fast image delivery via Cloudinary's CDN
- **Pagination**: Efficient data pagination for large datasets
- **Query Optimization**: Optimized database queries with select_related and prefetch_related

---

## 🧪 Testing

The project includes a test suite located in the `tests/` directory. Run tests using:

```bash
python manage.py test
```

---

## 📝 License

This project is licensed under the terms specified in the LICENSE file.

---

## 👨‍💻 Development Notes

This project represents a comprehensive full-stack web application demonstrating:

- **Backend Development**: Django framework mastery, database design, API development
- **Frontend Development**: Responsive design, modern UI/UX principles
- **DevOps**: Deployment configuration, environment management, cloud services integration
- **Security**: Authentication, authorization, data protection
- **Best Practices**: Code organization, maintainability, scalability considerations

---

## 🤝 Contributing

This is a portfolio project. For inquiries or collaboration opportunities, please reach out through the contact information provided in the application.

---

## 📧 Contact

For questions, feedback, or professional inquiries, please use the contact form on the application or reach out through the provided channels.

---

**Built with ❤️ using Django**

*Last Updated: 2025*
