# FS Basic

A modern Django + React SaaS boilerplate with built-in multi-tenancy, role-based access control, and authentication.

## Features

- **Multi-Tenancy Support**: Organize users into isolated organizations
- **Role-Based Access Control**: Three roles - Super Admin, Admin, and Member
- **User Authentication**: Django Allauth with headless support
- **Member Management**: Manage organization members with membership tracking
- **REST API**: Built with Django REST Framework
- **CORS Support**: Ready for frontend integration
- **PostgreSQL Support**: Flexible database configuration
- **Production Ready**: Environment-based configuration for different deployment targets

## Tech Stack

### Backend
- **Django 6.0.4**: Web framework
- **Django REST Framework**: API development
- **Django Allauth**: Authentication and authorization
- **django-cors-headers**: CORS handling
- **PostgreSQL**: Database (via psycopg2)
- **python-dotenv**: Environment configuration

### Frontend
- **React**: UI framework (with Vite)
- **Vite**: Build tool and dev server

## Project Structure
```
fs-basic/
├── backend/
│   ├── core/
│   │   ├── settings.py          # Django settings
│   │   ├── urls.py              # Main URL configuration
│   │   ├── asgi.py              # ASGI configuration
│   │   └── wsgi.py              # WSGI configuration
│   ├── api/
│   │   ├── models.py            # Data models
│   │   ├── views.py             # API views
│   │   ├── urls.py              # API routes
│   │   ├── admin.py             # Admin configuration
│   │   └── migrations/          # Database migrations
│   ├── manage.py                # Django management script
│   └── requirements.txt          # Python dependencies
└── .gitignore                   # Git ignore rules
```


## Database Models

### Organization
Represents a tenant/organization in the system.
- `name`: Organization name (max 255 characters)
- `is_active`: Boolean flag for active status
- `created_at`: Timestamp of creation

### User
Custom user model extending Django's AbstractUser with multi-tenancy support.
- Extends Django's AbstractUser (includes username, email, password, etc.)
- `organization`: ForeignKey to Organization (nullable for super admins)
- `role`: Choices - SUPER_ADMIN, ADMIN, MEMBER

### Member
Represents organization members/customers (can exist without linked user accounts).
- `organization`: ForeignKey to Organization
- `user`: Optional OneToOneField to User (for offline customers)
- `membership_number`: Unique membership identifier
- `name`: Full name
- `email`: Contact email
- `phone_number`: Contact phone
- `member_type`: LIFETIME or NORMAL
- `job`: Job title/position
- `mailing_address`: Physical address

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip/virtualenv
- PostgreSQL (optional, SQLite works for development)
- Node.js 16+ (for frontend)

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/haririabd/fs-basic.git
   cd fs-basic/backend
2. **Create and activate virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
4. **Set up environment variables Create a `.env` file in the `backend/` directory:**
    ```bash
    DJANGO_SECRET_KEY=your-secret-key-here
    DJANGO_DEBUG=True
    ON_CODESPACE=False
    ON_RAILWAY=False
    DATABASE_URL=postgresql://user:password@localhost:5432/fs_basic
5. **Run migrations**
    ```bash
    python manage.py migrate
6. **Create superuser**
    ```bash
    python manage.py createsuperuser
7. **Start development server**
    ```bash
    python manage.py runserver
The API will be available at `http://localhost:8000/api/`