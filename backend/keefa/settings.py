"""
Django settings for KEEFA project.
"""

import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

# Application definition
DJANGO_APPS = [
    'jazzmin', # MUST be before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_ckeditor_5',
]

LOCAL_APPS = [
    'core',
    'programs',
    'donations',
    'news',
    'contact',
    'users',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'keefa.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'keefa.wsgi.application'

# Database

USE_SQLITE = config('USE_SQLITE', default=True, cast=bool)

if USE_SQLITE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT'),
        }
    }


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

    # Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
        BASE_DIR / 'static',
    ]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:4321",
    "http://127.0.0.1:4321",
]

CORS_ALLOW_CREDENTIALS = True

# CKEditor settings
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading', '|',
            'bold', 'italic', 'underline', 'strikethrough', '|',
            'link', 'bulletedList', 'numberedList', 'blockQuote', '|',
            'insertTable', 'imageUpload', 'mediaEmbed', '|',
            'undo', 'redo', 'codeBlock', 'horizontalLine'
        ],
        'language': 'en',
        'image': {
            'toolbar': ['imageTextAlternative', 'imageStyle:full', 'imageStyle:side']
        },
        'table': {
            'contentToolbar': ['tableColumn', 'tableRow', 'mergeTableCells']
        },
        'height': '300px',
        'width': '100%',
    }
}


# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@cbongo.org')

# Stripe settings
STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY', default='')
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default='')
STRIPE_WEBHOOK_SECRET = config('STRIPE_WEBHOOK_SECRET', default='')

# Celery settings
CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Create logs directory if it doesn't exist
os.makedirs(BASE_DIR / 'logs', exist_ok=True)


#Customized Grouped admin Panel
# settings.py

JAZZMIN_SETTINGS = {
    # ... (Brand settings remain the same) ...
    "site_header": "KEEFA Admin Panel",
    "site_brand": "KEEFA CMS",
    "welcome_sign": "Welcome to the KEEFA Administration Dashboard",
    "search_url": "admin:users_customuser_changelist",
    "show_sidebar": True,
    "navigation_expanded": True,
    "changeform_format": "horizontal_tabs",
    
    # ⚙️ Global App Ordering (Sets the relative order of sections)
    "order_with_respect_to": [
        "programs", "donations", "news", "core", "contact", "users", "auth", "authtoken",
    ],

    # 🔗 Custom Sidebar Menu (Icons added to every model for visual clarity)
    "sidebar_links": [

        # 1. Custom Link/Separator
        {"name": "Website Home", "url": "/", "icon": "fas fa-globe"},

        # 2. Program & Project Management 🚀 (Kept High Priority)
        {
            "name": "Programs & Projects",
            "icon": "fas fa-hands-helping",
            "models": [
                {"model": "programs.programs", "icon": "fas fa-tasks"},                   # Program List
                {"model": "programs.projectlocations", "icon": "fas fa-map-marker-alt"}, # Locations
                {"model": "programs.successstories", "icon": "fas fa-trophy"},           # Success Stories
                {"model": "programs.scholarshipapplications", "icon": "fas fa-user-graduate"}, # Scholarships
                {"model": "programs.workshopregistrations", "icon": "fas fa-clipboard-list"}, # Registrations
            ]
        },

        # 3. Financial & Donation Management 💵 (Kept High Priority)
        {
            "name": "Donations & Partnerships",
            "icon": "fas fa-hand-holding-usd",
            "models": [
                {"model": "donations.donations", "icon": "fas fa-money-bill-wave"},       # Donations Records
                {"model": "donations.donationcampaigns", "icon": "fas fa-bullseye"},     # Campaigns
                {"model": "donations.donationimpacts", "icon": "fas fa-chart-line"},     # Impacts
                {"model": "donations.partnerships", "icon": "fas fa-handshake"},         # Partnerships
                {"model": "donations.volunteers", "icon": "fas fa-users-cog"},           # Volunteers
            ]
        },

        # 4. News & Events 📰 (Kept High Priority)
        {
            "name": "News & Events",
            "icon": "fas fa-bullhorn",
            "models": [
                {"model": "news.newsarticles", "icon": "fas fa-newspaper"},               # Articles
                {"model": "news.newscategories", "icon": "fas fa-tags"},                 # Categories
                {"model": "news.events", "icon": "fas fa-calendar-alt"},                 # Events
                {"model": "news.eventregistrations", "icon": "fas fa-user-check"},       # Event Registrations
                {"model": "news.newslettersubscriptions", "icon": "fas fa-at"},          # Subscriptions
            ]
        },
        
        # 5. SITE ADMINISTRATION & UTILITIES 🛠️ 
        {
            "name": "Site Admin & Utilities",
            "icon": "fas fa-cogs",
            "models": [
                # CORE App Models
                {"label": "Site Settings", "model": "core.sitesettings", "icon": "fas fa-tools"},
                {"model": "core.organizationinformation", "icon": "fas fa-building"},     # Organization Info
                {"model": "core.faqs", "icon": "fas fa-question-circle"},                # FAQs
                {"model": "core.impactstatistics", "icon": "fas fa-calculator"},         # Impact Stats
                {"model": "core.partners", "icon": "fas fa-address-book"},               # Partners
                {"model": "core.testimonials", "icon": "fas fa-quote-right"},            # Testimonials
                {"model": "core.teammembers", "icon": "fas fa-users"},                   # Team Members
                # CONTACT App Models
                {"label": "Contact Inquiries", "model": "contact.contactinquiries", "icon": "fas fa-inbox"},
                {"model": "contact.contactpersons", "icon": "fas fa-id-card"},           # Contact Persons
                {"model": "contact.officelocations", "icon": "fas fa-map-pin"},          # Office Locations
                {"model": "contact.socialmediaaccounts", "icon": "fas fa-share-alt"},    # Social Media
                # USER & AUTH Models
                {"label": "Manage Users", "model": "users.customuser", "icon": "fas fa-user-shield"},
                {"model": "auth.group", "icon": "fas fa-user-tag"},                      # Groups
                {"model": "authtoken.token", "icon": "fas fa-key"},                      # Tokens
            ]
        },
    ],
    
    # ⚙️ USER MENU LINKS (Provides quick access to top-level site links)
    "usermenu_links": [
        {"name": "Website Home", "url": "/", "icon": "fas fa-globe"},
    ],
}