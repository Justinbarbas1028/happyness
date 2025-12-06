# Happyness Project Context

## Project Overview
**Happyness** is a modern Django-based web application designed with a focus on user experience and robustness. It features a secure authentication system powered by `django-allauth` and `HTMX`, and a polished, centralized theming system supporting light and dark modes.

## Tech Stack
- **Backend:** Python 3.11+, Django 5.2
- **Database:** SQLite (Development), PostgreSQL (Production ready via `psycopg`)
- **Frontend:** Django Templates, Tailwind CSS, HTMX, Vanilla JavaScript
- **Infrastructure:** Docker, Gunicorn
- **Key Libraries:** `django-allauth`, `django-crispy-forms`, `crispy-tailwind`

## Architecture & Structure
- **Project Root:** `happyness/` (Settings, WSGI/ASGI)
- **Main Application:** `app/` (Models, Views, URLs, Tests)
- **Templates:** `templates/` (Global and specific app templates)
- **Static Files:** `static/` (CSS, JS, Images)
    - `static/css/theme.css`: Core theming variables.
    - `static/js/theme.js`: Theme toggle logic.

## Key Features

### 1. Authentication System
- **Implementation:** Built on `django-allauth` with custom templates.
- **Async Validation:** Uses **HTMX** for real-time username and email availability checks on signup.
- **UI/UX:** Modern, glassmorphism-inspired design using Tailwind CSS.
- **Endpoints:**
    - `/accounts/login/`
    - `/accounts/signup/`
    - `/accounts/password/reset/`

### 2. Centralized Theme System
- **Modes:** Light (Default) and Dark.
- **Mechanism:** CSS Custom Properties (variables) managed via `static/css/theme.css`.
- **Persistence:** Uses `localStorage` to remember user preference across sessions.
- **Usage:** Use CSS variables (e.g., `var(--bg-primary)`, `var(--text-primary)`) instead of hardcoded colors.

## Building and Running

### Local Development
1.  **Environment Setup:**
    ```bash
    python -m venv myvenv
    source myvenv/bin/activate  # or myvenv\Scripts\activate on Windows
    pip install -r requirements.txt
    ```
2.  **Database Setup:**
    ```bash
    python manage.py migrate
    ```
3.  **Run Server:**
    ```bash
    python manage.py runserver
    ```
    Access at: `http://127.0.0.1:8000/`

### Docker (Production/Dev)
1.  **Build Image:**
    ```bash
    docker build -t happyness .
    ```
2.  **Run Container:**
    ```bash
    docker run -p 8000:8000 --env-file .env.example happyness
    ```
    *Note: Ensure `.env` variables are set appropriately for production.*

## Development Conventions
- **Configuration:** Use environment variables for sensitive data (`SECRET_KEY`, `DB` configs). See `settings.py`.
- **Styling:** Prefer Tailwind utility classes. For custom colors, strictly use the variables defined in `theme.css` to ensure dark mode compatibility.
- **Testing:** Run standard Django tests:
    ```bash
    python manage.py test
    ```
- **Dependencies:** Keep `requirements.txt` updated when adding new packages.

## Git Practices
The project strictly follows [Conventional Commits](https://www.conventionalcommits.org/) and a structured GitHub workflow.

### Commit Messages
Format: `<type>(<scope>): <subject>`

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting (whitespace, etc.)
- `refactor`: Code restructuring without behavior change
- `perf`: Performance improvement
- `test`: Adding/fixing tests
- `chore`: Maintenance (deps, etc.)

**Example:** `feat(auth): add google oauth support`

### Workflow
1.  **Branches:** Use dedicated branches for features/fixes (e.g., `feature/new-ui`, `bugfix/login-error`).
2.  **Pull Requests:** Open PRs against `main`.
3.  **Merge Strategy:** Squash and Merge to maintain a clean history.
