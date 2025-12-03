# HappyNess Project - Copilot Instructions

## Architecture Overview
Django 5.2 web application with HTMX-powered interactivity and Tailwind CSS for styling, plus a custom CSS variable-based theming system for light/dark mode.

**Tech Stack:**
- **Backend:** Django 5.2, django-allauth (auth), crispy-tailwind (forms)
- **Frontend:** HTMX (interactivity), Tailwind CSS via CDN (styling), AOS (animations)
- **Theming:** CSS custom properties in `theme.css` for light/dark mode support

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

### UI Development (Critical - Tailwind + HTMX First)
**Always use Tailwind utility classes for layout, spacing, sizing, and non-themed styling.**
**Use inline `style` attributes with CSS variables ONLY for theme-aware colors.**
**Minimize custom CSS in `style.css` - only for states that JS toggles or complex animations.**

```html
<!-- ✓ Correct: Tailwind for layout + CSS vars for theme colors -->
<div class="w-full max-w-[600px] h-[400px] rounded-2xl overflow-hidden shadow-2xl"
     style="background-color: var(--card-bg); border: 1px solid var(--card-border);">
  <p class="text-lg font-semibold px-4 py-2" style="color: var(--text-primary);">
    Content here
  </p>
</div>

<!-- ✗ Wrong: Custom CSS for things Tailwind handles -->
<div class="my-custom-card">...</div>
/* In style.css - AVOID THIS */
.my-custom-card { width: 100%; max-width: 600px; border-radius: 16px; }

<!-- ✗ Wrong: Hardcoded colors that break theming -->
<div class="bg-white text-gray-900">...</div>
```

**Tailwind usage guidelines:**
- Layout: `flex`, `grid`, `items-center`, `justify-between`, `gap-4`
- Sizing: `w-full`, `h-[400px]`, `max-w-[600px]`, `p-4`, `px-8`, `py-2`
- Borders/Radius: `rounded-2xl`, `rounded-full`, `overflow-hidden`
- Shadows: `shadow-md`, `shadow-lg`, `shadow-2xl`
- Transforms: `transform`, `rotate-2`, `scale-110`, `translate-x-full`
- Transitions: `transition-all`, `duration-300`, `ease-out`, `hover:scale-110`
- Responsive: `md:block`, `hidden`, `sm:flex`

**When to use `style.css`:**
- JS-toggled states (e.g., `.slide.active { opacity: 1; transform: translateX(0); }`)
- Complex multi-property transitions not easily done in Tailwind
- Keyframe animations

### Theme System (Colors Only)
Use CSS variables for ALL colors to support light/dark mode:
```html
<div style="background-color: var(--card-bg); color: var(--text-primary);">
```
Available variables: `--text-primary`, `--text-secondary`, `--text-muted`, `--card-bg`, `--card-border`, `--card-shadow`, `--brand-primary`, `--brand-secondary`, `--button-primary`, `--bg-primary`, `--bg-secondary`. See `static/css/theme.css` for full list.

Utility classes `.card`, `.btn-primary`, `.btn-secondary` are pre-styled with theme variables.

### HTMX Patterns
**Use HTMX for all dynamic interactions instead of custom JavaScript.**

Real-time form validation returns HTML snippets:
```python
# app/views.py pattern
@require_POST
def validate_username(request):
    username = request.POST.get('username', '').strip()
    if User.objects.filter(username=username).exists():
        return HttpResponse('<span class="text-red-400">✗ Username taken</span>')
    return HttpResponse('<span class="text-green-400">✓ Username available</span>')
```
```html
<!-- Template pattern -->
<input hx-post="{% url 'validate_username' %}" 
       hx-trigger="blur changed delay:500ms"
       hx-target="#username-feedback"
       class="w-full px-4 py-2 rounded-lg"
       style="background-color: var(--input-bg); border: 1px solid var(--input-border); color: var(--text-primary);">
<div id="username-feedback" class="mt-1 text-sm"></div>
```

**HTMX partials:** Store reusable HTML fragments in `templates/partials/` for `hx-get`/`hx-post` responses.

**Common HTMX attributes:**
- `hx-get`, `hx-post` - HTTP requests
- `hx-trigger` - Event triggers (`click`, `blur`, `change`, `load`, `delay:500ms`)
- `hx-target` - Where to put the response (`#id`, `this`, `closest .class`)
- `hx-swap` - How to swap (`innerHTML`, `outerHTML`, `beforeend`, `afterbegin`)
- `hx-boost="true"` - On `<body>` for SPA-like navigation

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
