# Full Stack Basic

A modern, production-ready Django + React SaaS boilerplate with built-in multi-tenancy, role-based access control (RBAC), and enterprise-grade authentication.

**Perfect for building multi-tenant SaaS applications, CRM systems, or any platform where users belong to organizations.**

Notes: All port in below examples are set as 0000. Use your own port where applicable

---
## 🚀 Key Features

### Core Features
- **🏢 Multi-Tenancy Support**: Organize users into isolated organizations with complete data separation
- **🔐 Role-Based Access Control (RBAC)**: Three roles - Super Admin, Admin, and Member with granular permissions
- **👤 User Authentication**: Django Allauth with headless/API-first support
- **👥 Member Management**: Track organization members with flexible membership types (Lifetime, Normal)
- **🔗 Flexible User-Member Linking**: Create members first, then generate login credentials on-demand
- **🚪 REST API**: Full-featured Django REST Framework API
- **🌐 CORS Support**: Ready for frontend integration
- **📊 Database Flexibility**: SQLite for development, PostgreSQL for production
- **⚡ Production Ready**: Environment-based configuration, security headers, logging, rate limiting

### Security Features
- Environment-based configuration (works on localhost, Codespace, Railway, VPS, Docker, K8s)
- CSRF and CORS protection
- Rate limiting (10 requests/min for unauthenticated, 1000/day for authenticated)
- Secure password validation
- Custom permission classes with isolation rules
- HTTPS/SSL support with security headers

---

## 📋 Tech Stack

### Backend
- **Django 6.0.4**: Web framework
- **Django REST Framework**: API development
- **Django Allauth**: Authentication and authorization (headless mode)
- **django-cors-headers**: CORS handling
- **PostgreSQL** (production) / **SQLite** (development)
- **python-dotenv**: Environment configuration

### Frontend
- **React**: UI framework
- **Vite**: Modern build tool and dev server
- **Axios**: HTTP client

---

## 📁 Project Structure

```
fs-basic/
├── backend/
│   ├── core/
│   │   ├── settings.py              # Universal Django configuration
│   │   ├── urls.py                  # Main URL router
│   │   ├── asgi.py                  # ASGI configuration
│   │   ├── wsgi.py                  # WSGI configuration
│   │   └── __init__.py
│   ├── api/
│   │   ├── models.py                # Organization, User, Member models
│   │   ├── views.py                 # API ViewSets
│   │   ├── serializers.py           # DRF Serializers
│   │   ├── permissions.py           # Custom permission classes
│   │   ├��─ adapters.py              # Allauth custom adapter
│   │   ├── urls.py                  # API routes
│   │   ├── admin.py                 # Django admin config
│   │   ├── apps.py
│   │   ├── tests.py
│   │   ├── migrations/              # Database migrations
│   │   └── __init__.py
│   ├── commando/                    # Custom Django commands
│   ├── manage.py                    # Django CLI
│   ├── requirements.txt             # Python dependencies
│   ├── .env.example                 # Example environment variables
│   └── __init__.py
├── frontend/                        # React + Vite (structure varies)
│   ├── src/
│   ├── public/
│   ├── vite.config.js
│   └── package.json
├── .gitignore
└── README.md
```

---

## 🏗️ Architecture

### Multi-Tenancy Model

```
┌─────────────────────────────────────┐
│      Organization (Tenant)          │
│  ┌─────────────────────────────────┐│
│  │  Users                          ││
│  │  - Super Admin (Platform owner) ││
│  │  - Admins (Org admins)          ││
│  │  - Members (Regular users)      ││
│  └─────────────────────────────────┘│
│  ┌─────────────────────────────────┐│
│  │  Members (CRM contacts)         ││
│  │  - Can link to Users (optional) ││
│  │  - Membership tracking          ││
│  └─────────────────────────────────┘│
└─────────────────────────────────────┘
```

### Role Hierarchy & Permissions

| Role | Users | Members | Org Config |
|------|-------|---------|------------|
| **Super Admin** | View all | View all | Full access |
| **Admin** | Manage own org | Manage own org | Own org only |
| **Member** | View self only | View self only | View self only |

### Data Isolation

- **Organization-level isolation**: Admins and Members only see data from their organization
- **User-level isolation**: Members can only view and edit their own profile
- **API-enforced**: Permissions checked at both ViewSet and object level

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** (3.10+ recommended)
- **Node.js 16+**
- **PostgreSQL 12+** (optional for production; SQLite for development)
- **Git**

### Option 1: Local Development Setup

#### Backend Setup

```bash
# 1. Clone and navigate
git clone https://github.com/haririabd/fs-basic.git
cd fs-basic/backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file (copy from .env.example)
cp .env.example .env

# 5. Generate SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(f'DJANGO_SECRET_KEY={get_random_secret_key()}')" >> .env

# 6. Run migrations
python manage.py migrate

# 7. Create superuser
python manage.py createsuperuser

# 8. Start development server
python manage.py runserver

# Server runs at http://localhost:0000
# Admin at http://localhost:0000/admin
# API at http://localhost:0000/api/
```

#### Frontend Setup

```bash
# From project root
cd frontend

# Install dependencies
npm install

# Start dev server (runs on http://localhost:0000)
npm run dev

# Build for production
npm run build
```

---

## 🔧 Environment Configuration

### Universal Configuration (Works Everywhere)

The project uses **environment variables only** - no deployment-specific code branches. Set these variables and it works on localhost, Docker, VPS, Railway, Vercel, Kubernetes, etc.

### Environment Variables Reference

```bash
# ============================================
# REQUIRED
# ============================================

# Django
DJANGO_DEBUG=True                    # False in production
DJANGO_SECRET_KEY=your-secret-key   # Generate with get_random_secret_key()

# Frontend URL (for email links, CORS, CSRF)
# Examples:
#   Local: http://localhost:0000
#   Railway: https://fs-basic-frontend.railway.app
#   VPS: https://example.com
#   Vercel: https://your-app.vercel.app
FRONTEND_URL=http://localhost:0000

# ============================================
# OPTIONAL (has sensible defaults)
# ============================================

# Allowed hosts (comma-separated)
# Default: localhost,127.0.0.1
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS allowed origins (comma-separated)
# Default: http://localhost:0000,http://localhost:0000
CORS_ALLOWED_ORIGINS=http://localhost:0000,http://localhost:0000

# CSRF trusted origins (comma-separated)
# Default: http://localhost:0000,http://localhost:0000
CSRF_TRUSTED_ORIGINS=http://localhost:0000,http://localhost:0000

# Database URL (PostgreSQL connection string)
# Leave empty for SQLite (development only)
# Format: postgresql://user:password@host:port/dbname
# Example: postgresql://postgres:password@localhost:0000/fs_basic
DATABASE_URL=

# ============================================
# OPTIONAL (Codespace only)
# ============================================
ON_CODESPACE=False

# ============================================
# OPTIONAL (Email configuration)
# ============================================
EMAIL_HOST=smtp.zeptomail.com
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=noreply@example.com
ZEPTOMAIL_API_TOKEN=your-token

# ============================================
# OPTIONAL (Local development only)
# ============================================
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=securepassword123
```

### .env.example File

Copy `backend/.env.example` to `backend/.env` and update values:

```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your configuration
```

---

## 🌍 Deployment Guides

### Deploy to Railway

Railway is the easiest way to deploy. It auto-detects Django and PostgreSQL.

```bash
# 1. Install Railway CLI
npm i -g @railway/cli

# 2. Login
railway login

# 3. Create new project
railway init

# 4. Set environment variables
railway variables set \
  DJANGO_DEBUG=False \
  FRONTEND_URL=https://your-frontend-railway-url.railway.app \
  ALLOWED_HOSTS=your-backend-railway-url.railway.app \
  CORS_ALLOWED_ORIGINS=https://your-frontend-railway-url.railway.app \
  CSRF_TRUSTED_ORIGINS=https://your-frontend-railway-url.railway.app

# 5. Deploy
railway up

# View logs
railway logs
```

**After deployment:**
- Backend URL: `https://your-backend-service.railway.app`
- Frontend URL: `https://your-frontend-service.railway.app`

### Deploy to VPS (Ubuntu/Debian)

```bash
# 1. Connect to VPS
ssh user@your-vps-ip

# 2. Install dependencies
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip postgresql postgresql-contrib nginx

# 3. Clone repo
cd /opt
sudo git clone https://github.com/haririabd/fs-basic.git
cd fs-basic/backend

# 4. Setup Python environment
sudo python3.10 -m venv venv
source venv/bin/activate

# 5. Install Python dependencies
pip install -r requirements.txt

# 6. Create .env
sudo nano .env
# Add your environment variables (see above)

# 7. Create PostgreSQL database
sudo -u postgres psql
CREATE DATABASE fs_basic;
CREATE USER fs_basic_user WITH PASSWORD 'your-secure-password';
ALTER ROLE fs_basic_user SET client_encoding TO 'utf8';
ALTER ROLE fs_basic_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE fs_basic_user SET default_transaction_deferrable TO on;
ALTER ROLE fs_basic_user SET default_transaction_deferrable TO on;
GRANT ALL PRIVILEGES ON DATABASE fs_basic TO fs_basic_user;
\q

# 8. Update DATABASE_URL in .env
DATABASE_URL=postgresql://fs_basic_user:your-secure-password@localhost:0000/fs_basic

# 9. Run migrations
python manage.py migrate
python manage.py createsuperuser

# 10. Collect static files
python manage.py collectstatic --noinput

# 11. Configure Gunicorn + Nginx (see next section)
```

### Configure Gunicorn + Nginx

**Install Gunicorn:**
```bash
source /opt/fs-basic/backend/venv/bin/activate
pip install gunicorn
```

**Create systemd service** (`/etc/systemd/system/fs-basic-backend.service`):
```ini
[Unit]
Description=FS Basic Django Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/fs-basic/backend
ExecStart=/opt/fs-basic/backend/venv/bin/gunicorn \
    --workers 4 \
    --bind 127.0.0.1:0000 \
    --timeout 120 \
    core.wsgi:application

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Start service:**
```bash
sudo systemctl daemon-reload
sudo systemctl start fs-basic-backend
sudo systemctl enable fs-basic-backend
```

**Configure Nginx** (`/etc/nginx/sites-available/fs-basic`):
```nginx
upstream fs_basic_backend {
    server 127.0.0.1:0000;
}

server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://fs_basic_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /opt/fs-basic/backend/local-cdn/;
    }
    
    location /media/ {
        alias /opt/fs-basic/backend/media/;
    }
}
```

**Enable and restart:**
```bash
sudo ln -s /etc/nginx/sites-available/fs-basic /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**Setup HTTPS with Let's Encrypt:**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Deploy to Docker

**Dockerfile** (create in `backend/`):
```dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0.0.0.0:0000", "--workers", "4", "core.wsgi:application"]
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: fs_basic
      POSTGRES_USER: fs_basic_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports:
      - "0000:0000"
    environment:
      DJANGO_DEBUG: 'False'
      DJANGO_SECRET_KEY: your-secret-key
      FRONTEND_URL: http://localhost:0000
      DATABASE_URL: postgresql://fs_basic_user:secure_password@postgres:0000/fs_basic
    depends_on:
      - postgres
    volumes:
      - ./backend:/app

  frontend:
    image: node:18
    working_dir: /app
    command: npm run dev
    ports:
      - "0000:0000"
    volumes:
      - ./frontend:/app
    environment:
      VITE_API_URL: http://localhost:0000

volumes:
  postgres_data:
```

**Run:**
```bash
docker-compose up -d
```

---

## 📡 API Endpoints

All endpoints require authentication (except `/api/_allauth/` for signup/login).

### Authentication Endpoints
```
POST   /api/_allauth/login/               # Login
POST   /api/_allauth/signup/              # Register
POST   /api/_allauth/account/logout/      # Logout
POST   /api/_allauth/account/password/change/  # Change password
```

### User Endpoints
```
GET    /api/users/                        # List users (org-filtered)
POST   /api/users/                        # Create user (admin only)
GET    /api/users/{id}/                   # Get user details
PUT    /api/users/{id}/                   # Update user
DELETE /api/users/{id}/                   # Delete user (admin only)
```

### Organization Endpoints
```
GET    /api/organizations/                # List organizations (org-filtered)
GET    /api/organizations/{id}/           # Get organization details
```

### Member Endpoints
```
GET    /api/members/                      # List members (org-filtered)
POST   /api/members/                      # Create member (admin only)
GET    /api/members/{id}/                 # Get member details
PUT    /api/members/{id}/                 # Update member
DELETE /api/members/{id}/                 # Delete member
POST   /api/members/{id}/activate_login/  # Create login for member
```

---

## 🔐 Security Architecture

### Multi-Tenancy Isolation

```python
# Organization Level
user.organization != request.user.organization  # ❌ Denied

# User Level
member.organization != request.user.organization  # ❌ Denied

# Self Level
user.id != request.user.id  # ❌ Denied (Members only)
```

### Permission Classes

**IsOrgAdminOrOwner**: Custom permission enforcing organization isolation

```python
# Superuser: Access everything
# Admin: Access own organization only
# Member: Access self only (GET/PUT) - no POST/DELETE
```

### Security Headers (Production)

- ✅ HTTPS redirect
- ✅ HSTS (HTTP Strict Transport Security)
- ✅ Secure cookies (HTTPS only)
- ✅ CSRF protection
- ✅ X-Frame-Options
- ✅ Content Security Policy ready

---

## 📝 Data Models

### Organization
```python
{
    "id": 1,
    "name": "Acme Corp",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z"
}
```

### User
```python
{
    "id": 1,
    "username": "john@example.com",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "ADMIN",  # SUPER_ADMIN, ADMIN, MEMBER
    "organization": 1,
    "organization_name": "Acme Corp",
    "is_active": true
}
```

### Member
```python
{
    "id": 1,
    "name": "Jane Smith",
    "email": "jane@example.com",
    "phone_number": "+1234567890",
    "member_type": "LIFETIME",  # LIFETIME, NORMAL
    "membership_number": "MEM-001",
    "job": "Manager",
    "mailing_address": "123 Main St",
    "organization": 1,
    "organization_name": "Acme Corp",
    "user": null  # Links to User when they need login access
}
```

---

## 🛠️ Common Tasks

### Create a New Organization & Admin User

```bash
python manage.py shell

from api.models import Organization, User

# Create organization
org = Organization.objects.create(name="My Company")

# Create admin user
admin = User.objects.create_superuser(
    username="admin@mycompany.com",
    email="admin@mycompany.com",
    password="securepassword123",
    organization=org,
    role="ADMIN"
)
```

### Add Email Support

1. Update `.env`:
```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourcompany.com
```

2. Enable in settings.py if needed

### Run Tests

```bash
python manage.py test api
```

### Database Backup

```bash
# PostgreSQL
pg_dump fs_basic > backup.sql

# Restore
psql fs_basic < backup.sql
```

---

## 📚 Documentation

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Allauth](https://django-allauth.readthedocs.io/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🆘 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'django'"
**Solution**: Activate virtual environment and reinstall dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "CORS error on frontend"
**Solution**: Check CORS_ALLOWED_ORIGINS in `.env`:
```bash
CORS_ALLOWED_ORIGINS=http://localhost:0000,http://localhost:0000
```

### Issue: Database connection error
**Solution**: Verify DATABASE_URL:
```bash
# For PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:0000/fs_basic

# For SQLite (leave empty)
DATABASE_URL=
```

### Issue: "Secret key was not set"
**Solution**: Generate and add to `.env`:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(f'DJANGO_SECRET_KEY={get_random_secret_key()}')" >> backend/.env
```

---

## 📞 Support

- 📧 Email: support@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/haririabd/fs-basic/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/haririabd/fs-basic/discussions)

---

## 🙌 Acknowledgments

Built with ❤️ using Django, Django REST Framework, React, and Vite.

Special thanks to the open-source community.

---

**Last Updated**: April 2026  
**Version**: 1.0.0