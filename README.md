# Happyness

Basic Django setup with templates and static files (HTML/CSS/JS/images).

## Quickstart

1. Install dependencies (optionally in a virtualenv):

```cmd
py -m pip install -r requirements.txt
```

2. Run migrations and start the server:

```cmd
py manage.py migrate
py manage.py runserver
```

3. Open http://127.0.0.1:8000/ and you should see the home page with working CSS/JS and a logo.

## Project layout

- `templates/` — base and home templates
- `static/css/style.css` — site styles
- `static/js/app.js` — small interactivity
- `static/images/happyness-logo.jpeg` — favicon/logo

## Notes

- Static files are served automatically by Django in DEBUG. In production, collect with `py manage.py collectstatic` and serve via a web server.
# happyness
