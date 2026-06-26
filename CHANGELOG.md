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


## Phase 1.4 - 2026-06-26

### Added in models.py
- Implemented a custom authentication manager `SchoolManager` by inheriting from `BaseUserManager`.
- Added a `create_user()` method to centralize user creation logic.
- Added email validation to ensure every user has a valid email before creation.
- Implemented email normalization using `normalize_email()` for consistent email storage.
- Used `self.create()` to instantiate a new `School` model object through the manager.
- Secured user passwords using `set_password()` instead of storing plain text passwords.
- Configured staff permissions using the `is_staff` attribute.
- Saved users to the configured database using `user.save(using=self._db)`.
- Returned the newly created `School` object after successful creation.

### Learned
- `BaseUserManager` acts as a factory responsible for creating user objects.
- `create_user()` defines how regular users are created.
- `normalize_email()` standardizes email addresses before saving them.
- `set_password()` hashes passwords securely using Django's built-in password hashing system.
- `save(using=self._db)` ensures the object is saved using the manager's configured database connection.
- `return user` provides the created object back to the caller for further use.

### Workflow Mastered

```text
User Registration
       │
       ▼
Validate Email
       │
       ▼
Normalize Email
       │
       ▼
Create School Object
       │
       ▼
Hash Password
       │
       ▼
Assign Permissions
       │
       ▼
Save to Database
       │
       ▼
Return User Object
```

### Memory Mnemonic

**NCHSR**

- **N** → Normalize Email
- **C** → Create User
- **H** → Hash Password
- **S** → Save User
- **R** → Return User

