# Excel AI Chatbot (Django)

A Django-based web application for managing student fee records from Excel uploads and answering common queries using a rule-based chatbot.

## Features

- **Authentication & Roles**
  - Custom user model (`CustomUser`) with roles:
    - `teacher`
    - `superadmin`
  - Login / Registration / Logout with user activity logging.
- **Admin Panel (Super Admin)**
  - Dashboard with system statistics.
  - Manage:
    - Excel uploads (list + delete)
    - Users (list / edit / delete)
    - User logs
    - Chatbot logs
  - System settings management (school name, system name, contact details, logo).
- **Student Management**
  - Students stored in the database with fee fields:
    - `roll_no`, `name`, `std`, `fee_status`, `remaining_fee`, `total_paid_fee`.
  - CRUD views for student listing, details, and updates.
- **Excel Import**
  - Upload an Excel file and import/update students.
  - Requires specific columns in the Excel sheet (see **Excel Format**).
- **Chatbot**
  - AJAX endpoint that processes teacher questions and returns responses.
  - Logs every question/answer pair.
  - Supports commands like:
    - Total students
    - Total fee paid / pending fee
    - Pending/paid student lists
    - Highest/lowest remaining fee
    - Last 10 students
    - Search by roll no / std / student name

## Tech Stack

- **Backend:** Django
- **Data Processing:** pandas (Excel parsing)
- **Database:** SQLite (default)
- **Frontend:** Server-rendered templates + static JS/CSS

## Prerequisites

- Python 3.10+ (recommended)
- pip

## Setup & Run (Development)

1. **Create and activate a virtual environment**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. **Install dependencies**

   Install the required Python packages (create your own `requirements.txt` if you don’t already have one):

   ```bash
   pip install django pandas openpyxl
   ```

3. **Apply migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser (for admin panel)**

   ```bash
   python manage.py createsuperuser
   ```

5. **Run the server**

   ```bash
   python manage.py runserver
   ```

6. **Open the application**

   - Main app: `http://127.0.0.1:8000/`
   - Admin panel (superadmin): `http://127.0.0.1:8000/admin-panel/`

> Notes:
> - Media (uploaded Excel + logo) is served via `MEDIA_URL` / `MEDIA_ROOT` in development.
> - `DEBUG=True` by default.

## Excel Format
The Excel upload expects these column headers:

- `Roll No`
- `Name`
- `Std`
- `Fee Status`
- `Remaining Fee`
- `Total Paid Fee`

If any required column is missing, the upload will fail with an error message.

## Project Structure (High Level)

- `Excel_AI_chatbot_project/` — Django project settings and root URL configuration
- `excel_ai_chatbot/` — Main app (custom user, students, Excel import, chatbot, pages)
- `admin_panel/` — Super admin dashboard, logs, user management, settings

## Endpoints (Useful)

- App routes (`excel_ai_chatbot/urls.py`):
  - `/` — Home
  - `/login/` — Login
  - `/register/` — Registration
  - `/logout/` — Logout
  - `/dashboard/` — Teacher dashboard
  - `/excel-upload/` — Upload Excel
  - `/students/` — Student list
  - `/student/<id>/` — Student detail
  - `/student/<id>/edit/` — Student update
  - `/chatbot/` — Chatbot AJAX endpoint (POST)

- Admin panel (`admin_panel/urls.py`):
  - `/admin-panel/` — Admin dashboard
  - `/admin-panel/excel-sheets/` — Excel upload list
  - `/admin-panel/excel-sheets/delete/<excel_id>/` — Delete uploaded Excel
  - `/admin-panel/users/` — User list
  - `/admin-panel/users/edit/<user_id>/` — Edit user
  - `/admin-panel/users/delete/<user_id>/` — Delete user
  - `/admin-panel/user-logs/` — User logs
  - `/admin-panel/chatbot-logs/` — Chatbot logs
  - `/admin-panel/settings/` — System settings

## Security Notes

- Admin panel views are restricted to `superadmin` via a custom decorator.
- Chatbot endpoint is **POST-only** and returns JSON.

## License

Add your project license here (or remove this section).

