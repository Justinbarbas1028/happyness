# HappyNess Project - Copilot Instructions

## Architecture Overview
Django 5.2 web application with HTMX-powered interactivity and a custom CSS variable-based theming system.

**Key structural decisions:**
- Single `app/` module handles all views; URL routing split between `happyness/urls.py` (root) and `app/urls.py`
- Templates at project root (`templates/`) with partials in `templates/partials/` for HTMX fragments
- Authentication via **django-allauth** (not custom auth); templates override at `templates/account/`
- Theme system uses CSS custom properties in `static/css/theme.css` with JS toggle in `static/js/theme.js`

## Developer Workflow

### Quick Start
```cmd
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py runserver
```
Or use VS Code task: "Run Django dev server"

### Running Tests
```cmd
py manage.py test app.tests
```
Tests use Django's test client; auth tests are in `app/tests/test_auth_views.py`.

### Docker (Production-like)
```cmd
docker build -t happyness .
docker run -p 8000:8000 -e SECRET_KEY=your-key happyness
```
`docker/entrypoint.sh` handles Postgres wait, migrations, and gunicorn startup.

## Project-Specific Patterns

### Theme System (Critical Pattern)
**Do NOT use hardcoded Tailwind color classes for theming.** Use CSS variables:
```html
<!-- ✗ Wrong -->
<div class="bg-white text-gray-900">

<!-- ✓ Correct -->
<div style="background-color: var(--card-bg); color: var(--text-primary);">
```
Available variables: `--text-primary`, `--text-secondary`, `--card-bg`, `--card-border`, `--brand-primary`, `--brand-secondary`, `--button-primary`, etc. See `static/css/theme.css` for full list.

Use utility classes `.card`, `.btn-primary`, `.btn-secondary` for components.

### HTMX Validation Pattern
Real-time form validation returns HTML snippets:
```python
# app/views.py pattern
@require_POST
def validate_username(request):
    username = request.POST.get('username', '').strip()
    if User.objects.filter(username=username).exists():
        return HttpResponse('This username is already taken')
    return HttpResponse('<span class="text-green-400">✓ Username available</span>')
```
```html
<!-- Template pattern -->
<input hx-post="{% url 'validate_username' %}" 
       hx-trigger="blur changed delay:500ms"
       hx-target="#username-feedback">
```

### View Decorators
- Public pages: no decorator needed
- Authenticated pages: use `@login_required` (redirects to `/accounts/login/`)
- POST-only endpoints: use `@require_POST`

### Template Inheritance
All pages extend `templates/base.html`. Override `{% block title %}` and `{% block content %}`.
```django
{% extends 'base.html' %}
{% block title %}Page Title - Happyness{% endblock %}
{% block content %}
  <!-- Your content -->
{% endblock %}
```

## Key Configuration

### Environment Variables (Production)
- `SECRET_KEY` - Required for production
- `DEBUG` - Set to `0` for production  
- `ALLOWED_HOSTS` - Comma-separated hostnames
- `POSTGRES_HOST/DB/USER/PASSWORD/PORT` - Database config (defaults to SQLite if not set)

### django-allauth Settings
```python
# Login accepts username OR email
ACCOUNT_LOGIN_METHODS = {'username', 'email'}
# Redirects after login/logout
LOGIN_REDIRECT_URL = '/home/'
LOGOUT_REDIRECT_URL = '/'
```

### Crispy Forms + Tailwind
Forms use `crispy_tailwind` template pack. In templates:
```django
{% load crispy_forms_tags %}
{{ form|crispy }}
```

## File Locations Quick Reference
| Purpose | Location |
|---------|----------|
| Django settings | `happyness/settings.py` |
| URL routing | `happyness/urls.py`, `app/urls.py` |
| Views | `app/views.py` |
| Models | `app/models.py` (currently empty) |
| Base template | `templates/base.html` |
| Auth templates | `templates/account/` |
| HTMX partials | `templates/partials/` |
| Theme CSS | `static/css/theme.css` |
| Theme JS | `static/js/theme.js` |
| Tests | `app/tests/` |
