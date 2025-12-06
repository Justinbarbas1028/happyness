# HappyNess Project Overview

This is **HappyNess**, a modern Django-based web application focused on user experience and theming.

### **Project Overview**
-   **Type:** Full-stack Web Application
-   **Backend:** Python (Django 5.2+)
-   **Frontend:** HTML, CSS (Tailwind + Custom Theme System), JavaScript, HTMX
-   **Database:** SQLite (default for development)
-   **Infrastructure:** Docker support included

### **Key Systems**
1.  **Authentication (`AUTHENTICATION.md`)**
    -   Powered by `django-allauth`.
    -   Features modern, asynchronous forms using **HTMX** (no page reloads for validation).
    -   Includes Login, Signup (with real-time username/email checking), and Password Reset.
    -   Styled with Tailwind CSS and glassmorphism effects.

2.  **Theme System (`THEME_SYSTEM.md`)**
    -   A centralized Light/Dark mode system built with CSS variables.
    -   **Light Mode:** Soft pastels (beige/mint/teal).
    -   **Dark Mode:** Deep blue/gray tones.
    -   Persists user preference via `localStorage` to avoid flashing unstyled content.

### **Project Structure**
-   **`app/`**: Main application logic (models, views, URLs, and validation logic).
-   **`happyness/`**: Project configuration (settings, main URL routing).
-   **`templates/`**: HTML files organized by feature (`account/`, `admin/`, `partials/`).
-   **`static/`**: CSS, JavaScript, and images (includes the core `theme.css` and `theme.js`).
-   **`docker/`**: Containerization scripts.

### **Getting Started**
If you haven't already, you can set up the environment by running:
1.  `pip install -r requirements.txt`
2.  `python manage.py migrate`
3.  `python manage.py runserver`

The app will be available at `http://127.0.0.1:8000/`.

### **Usability Principles**
In the development of HappyNess, we adhere to **Jakob Nielsen's 10 Usability Heuristics** to ensure a user-friendly and intuitive experience:

1.  **Visibility of System Status**: Users are always informed about what is going on through appropriate feedback within reasonable time.
2.  **Match Between System and the Real World**: The system speaks the users' language, with words, phrases, and concepts familiar to the user, rather than system-oriented terms. Information appears in a natural and logical order.
3.  **User Control and Freedom**: Users can easily undo or redo actions, providing them with a sense of control and freedom to explore without fear of irreversible mistakes.
4.  **Consistency and Standards**: We maintain consistency in terminology, actions, and situations across the platform, adhering to established conventions.
5.  **Error Prevention**: We design carefully to prevent problems from occurring in the first place, or at least help users recognize errors before they commit to them.
6.  **Recognition Rather Than Recall**: We minimize the user's memory load by making objects, actions, and options visible.
7.  **Flexibility and Efficiency of Use**: The system is efficient for both novice and experienced users, allowing for customization and shortcuts where appropriate.
8.  **Aesthetic and Minimalist Design**: Dialogues do not contain irrelevant or rarely needed information. Every extra unit of information in a dialogue competes with the relevant units of information and diminishes their relative visibility.
9.  **Help Users Recognize, Diagnose, and Recover from Errors**: Error messages are expressed in plain language (no codes), precisely indicate the problem, and constructively suggest a solution.
10. **Help and Documentation**: Although it's better if the system can be used without documentation, it should be available and easy to search, focused on the user's task, list concrete steps to be carried out, and not be too large.
