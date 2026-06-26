## Phase 1.2 — 2026-06-26
- Installed Django, DRF, cors-headers, python-dotenv, drf-spectacular
- Frozen dependencies to requirements.txt
- Initialized git repository
- Learned: virtual environments isolate project packages; requirements.txt
  allows the project to be recreated on any machine

## Phase 1.3 — 2026-06-26
- Created Django project with django-admin startproject
- Studied: manage.py, settings.py, urls.py, wsgi.py
- Dev server runs at http://127.0.0.1:8000/
- Learned: Django project = config folder + manage.py. Apps are 
  separate from the project config.

## Phase 1.4 — 2026-06-26
- Moved SECRET_KEY to .env using python-dotenv
- Registered rest_framework, corsheaders, drf_spectacular in INSTALLED_APPS
- Added CorsMiddleware as first middleware
- Configured REST_FRAMEWORK, CORS_ALLOWED_ORIGINS, MEDIA_ROOT settings
- Learned: settings.py is loaded once at startup — every app and middleware
  must be registered here before Django knows it exists