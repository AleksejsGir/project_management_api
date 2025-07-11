# 🚀 Project Management API

[![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)](https://djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14.0-blue.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://postgresql.org/)
[![Railway](https://img.shields.io/badge/Deployed%20on-Railway-purple.svg)](https://railway.app/)
[![API Status](https://img.shields.io/badge/API%20Status-Live-brightgreen.svg)](https://web-production-339a1.up.railway.app/)

A robust REST API for project and job vacancy management, built with Django REST Framework and deployed on Railway with PostgreSQL.

## 📋 Table of Contents

- [🌐 Live Demo](#-live-demo)
- [🏗️ Tech Stack](#️-tech-stack)
- [📖 API Documentation](#-api-documentation)
- [🔐 Authentication](#-authentication)
- [👤 Test Data](#-test-data)
- [🚀 API Endpoints](#-api-endpoints)
- [💡 Request Examples](#-request-examples)
- [⚙️ Local Setup](#local-setup)
- [🐳 Docker Setup](#-docker-setup)
- [🚀 Deployment](#-deployment)

## 🌐 Live Demo

**🔗 Production API:** https://web-production-339a1.up.railway.app

**📊 Server Status:** ✅ Active and running stable

## 🏗️ Tech Stack

### 🐍 Backend
- **Python 3.11+** - Core language
- **Django 4.2.7** - Web framework
- **Django REST Framework 3.14.0** - API framework
- **PostgreSQL** - Primary database
- **Gunicorn** - WSGI server for production

### 📦 Additional Libraries
- **drf-spectacular** - OpenAPI documentation generation
- **django-cors-headers** - CORS configuration
- **python-decouple** - Environment variables management
- **dj-database-url** - Database configuration via URL
- **whitenoise** - Static files serving

### 🌐 Infrastructure
- **Railway** - Hosting and auto-deployment
- **PostgreSQL (Railway)** - Managed database
- **GitHub** - Version control and CI/CD

### 🏛️ Architecture Features
- ✅ **Token Authentication** for API security
- ✅ **Permission Classes** for access control
- ✅ **Model Validators** for data validation
- ✅ **Serializer Validation** with cross-field checks
- ✅ **ViewSet Architecture** with custom actions
- ✅ **Swagger Documentation** with detailed schemas
- ✅ **Production-ready Settings** with security configuration

## 📖 API Documentation

| Resource | URL | Description |
|----------|-----|-------------|
| **Swagger UI** | [/api/docs/](https://web-production-339a1.up.railway.app/api/docs/) | Interactive API documentation |
| **ReDoc** | [/api/redoc/](https://web-production-339a1.up.railway.app/api/redoc/) | Alternative API documentation |
| **OpenAPI Schema** | [/api/schema/](https://web-production-339a1.up.railway.app/api/schema/) | Raw OpenAPI specification |
| **Django Admin** | [/admin/](https://web-production-339a1.up.railway.app/admin/) | Admin interface |

## 🔐 Authentication

The API uses **Token Authentication**. To access protected endpoints:

1. Register a new account or login
2. Obtain an authentication token
3. Include token in request headers: `Authorization: Token your_token_here`

### 🔑 Admin Access
- **Username:** `******`
- **Password:** `********`

## 👤 Test Data

### 🧑‍💻 Test Users
```
Username: testuser1  |  Password: testpass123
Username: testuser2  |  Password: testpass123  
Username: testuser3  |  Password: testpass123
```

### 📂 Sample Projects
1. **E-commerce Platform** (testuser1)
   - Technologies: Python, Django, React, PostgreSQL, Redis
   - Budget: $150,000
   - Deadline: 90 days from now

2. **Food Delivery Mobile App** (testuser2)
   - Technologies: React Native, Node.js, MongoDB, Socket.io
   - Budget: $80,000
   - Deadline: 60 days from now

3. **Data Analytics System** (testuser3)
   - Technologies: Python, Apache Spark, Kafka, Elasticsearch
   - Budget: $200,000
   - Deadline: 120 days from now

### 💼 Sample Job Vacancies
- Senior Python Developer ($120k-$180k, full-time)
- React Native Developer ($100k-$150k, full-time)
- Data Engineer ($140k-$200k, full-time)
- Frontend Developer Intern ($40k-$60k, internship)

## 🚀 API Endpoints

### 🔐 Authentication
```http
POST /auth/register/          # Register new user
POST /auth/login/             # User login
POST /auth/logout/            # User logout
GET  /auth/profile/           # Get user profile
PUT  /auth/profile/           # Update user profile
POST /auth/change-password/   # Change password
GET  /auth/verify-token/      # Verify token validity
```

### 📂 Projects
```http
GET    /api/projects/              # List user's projects
POST   /api/projects/              # Create new project
GET    /api/projects/{id}/         # Get project details
PUT    /api/projects/{id}/         # Update project (full)
PATCH  /api/projects/{id}/         # Update project (partial)
DELETE /api/projects/{id}/         # Delete project
GET    /api/projects/{id}/stats/   # Get project statistics
```

### 💼 Project Vacancies
```http
GET  /api/projects/{id}/vacancies/    # Get project vacancies
POST /api/projects/{id}/vacancies/    # Create vacancy for project
```

### 💼 Vacancies (General)
```http
GET    /api/vacancies/                # List all user vacancies
GET    /api/vacancies/{id}/           # Get vacancy details
PUT    /api/vacancies/{id}/           # Update vacancy (full)
PATCH  /api/vacancies/{id}/           # Update vacancy (partial)
DELETE /api/vacancies/{id}/           # Delete vacancy
```

### 🔍 Vacancy Filters
```http
GET /api/vacancies/?project=1                    # Filter by project
GET /api/vacancies/?employment_type=full-time    # Filter by employment type
GET /api/vacancies/?is_active=true               # Filter active vacancies
```

## 💡 Request Examples

### 1. 📝 User Registration

```bash
curl -X POST https://web-production-339a1.up.railway.app/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "secure_password123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 5,
    "username": "newuser",
    "email": "newuser@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "token": "YOUR_TOKEN_HERE"
}
```

### 2. 📂 Create Project

```bash
curl -X POST https://web-production-339a1.up.railway.app/api/projects/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Awesome Project",
    "description": "Revolutionary web application",
    "technologies": ["Python", "Django", "Vue.js"],
    "budget": 75000.00,
    "deadline": "2025-12-31"
  }'
```

**Response:**
```json
{
  "id": 4,
  "title": "My Awesome Project",
  "description": "Revolutionary web application",
  "technologies": ["Python", "Django", "Vue.js"],
  "budget": "75000.00",
  "deadline": "2025-12-31",
  "owner": "newuser",
  "owner_id": 5,
  "technologies_count": 3,
  "is_overdue": false,
  "vacancies_count": 0,
  "metadata": {},
  "created_at": "2025-07-02T12:00:00Z",
  "updated_at": "2025-07-02T12:00:00Z"
}
```

### 3. 💼 Create Job Vacancy

```bash
curl -X POST https://web-production-339a1.up.railway.app/api/projects/4/vacancies/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Full Stack Developer",
    "description": "Looking for experienced full stack developer",
    "requirements": "Python, Django, Vue.js, 2+ years experience",
    "salary_min": 80000.00,
    "salary_max": 120000.00,
    "employment_type": "full-time"
  }'
```

### 4. 📊 Get Project Statistics

```bash
curl -X GET https://web-production-339a1.up.railway.app/api/projects/4/stats/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

**Response:**
```json
{
  "total_technologies": 3,
  "total_vacancies": 1,
  "active_vacancies": 1,
  "is_overdue": false,
  "days_until_deadline": 182
}
```

### 5. 🔍 Search Vacancies

```bash
curl -X GET "https://web-production-339a1.up.railway.app/api/vacancies/?employment_type=full-time" \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## ⚙️ Local Setup

### 🐳 Docker Setup (RECOMMENDED)

The easiest way to run the project locally:

1. **Clone the repository:**
```bash
git clone https://github.com/AleksejsGir/project_management_api.git
cd project_management_api
```

2. **Create environment file:**
```bash
cp .env.example .env
# Edit .env file as needed
```

3. **Run with Docker Compose:**
```bash
docker-compose up --build
```

**That's it!** API will be available at: http://localhost:8000/

**What happens automatically:**
- ✅ PostgreSQL database starts
- ✅ Migrations are applied
- ✅ Static files are collected
- ✅ Test data is created
- ✅ Django server starts

### 📋 Useful Docker Commands

```bash
# Stop containers
docker-compose down

# Restart with rebuild
docker-compose up --build

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access container shell
docker-compose exec web bash

# View logs
docker-compose logs web
```

### 🐍 Manual Setup (Without Docker)

**Requirements:** Python 3.11+, PostgreSQL 13+

1. **Installation:**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configuration:**
```bash
# Copy and configure .env
cp .env.example .env

# Create PostgreSQL database
createdb project_management
```

3. **Run the application:**
```bash
python manage.py migrate
python manage.py create_test_data
python manage.py createsuperuser
python manage.py runserver
```

## 🚀 Deployment

### 🚂 Railway Deployment

#### Automatic deployment via GitHub:

1. **Fork this repository** on GitHub
2. **Create a Railway project** at railway.app
3. **Connect your GitHub repository**
4. **Add PostgreSQL** from Railway Marketplace
5. **Configure environment variables:**

```env
RAILWAY_ENVIRONMENT=production
SECRET_KEY=<your-production-secret-key>
DEBUG=False
PORT=8000
```

6. **Deployment happens automatically!**

#### Manual deployment via Railway CLI:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add PostgreSQL
railway add postgresql

# Deploy
railway up
```

#### Post-deployment setup:

```bash
# Create superuser
railway run python manage.py createsuperuser

# Create test data
railway run python manage.py create_test_data
```



---

## 📞 Support

If you encounter any issues or have questions about the API:

1. Check the [Swagger Documentation](https://web-production-339a1.up.railway.app/api/docs/)
2. Review the API examples above
3. Test with the provided sample data
4. Contact the development team: https://github.com/AleksejsGir

## 📝 About This Project
This REST API was developed as a technical demonstration showcasing Django REST Framework, PostgreSQL integration, and production deployment capabilities. The project serves as a portfolio piece demonstrating full-stack development skills.

---

**⭐ If you find this project helpful, please give it a star!**