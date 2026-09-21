# UniPlacementHub

A DBMS-focused university internship and job placement portal built with Django and PostgreSQL.

## Features

- Student/company registration and profiles
- Admin/company verification
- Company internship/job postings
- Eligibility by CGPA and department
- Skill requirements
- Student applications with duplicate protection
- Application status: Applied, Shortlisted, Rejected, Selected
- Placement drives
- Placement analytics
- PostgreSQL-ready schema with constraints and indexes
- Transactional candidate selection
- Raw SQL analytics in `queries/`

## Run locally

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Database

The project defaults to SQLite so it runs immediately. For PostgreSQL, set:

```bash
export DB_ENGINE=postgresql
export DB_NAME=uniplacementhub
export DB_USER=postgres
export DB_PASSWORD=your_password
export DB_HOST=localhost
export DB_PORT=5432
```

On Windows PowerShell use `$env:NAME="value"`.

### 4. Migrate and create admin

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Main URLs

- `/` dashboard/home
- `/register/`
- `/login/`
- `/student/profile/`
- `/company/profile/`
- `/postings/`
- `/company/postings/`
- `/company/postings/create/`
- `/my-applications/`
- `/admin/`
- `/placement/analytics/`

## PostgreSQL / DBMS highlights

- Foreign keys and one-to-one profile relationships
- Unique `(posting, student)` application constraint
- CGPA and positive-position validation
- Many-to-many skills and departments
- Indexes on common filtering/join columns
- `transaction.atomic()` + `select_for_update()` for candidate selection
- Raw SQL analytics in `queries/`

## Demo flow

1. Create an admin with `createsuperuser`.
2. Register a company.
3. In Django admin, mark the company as verified.
4. Register a student and fill their profile.
5. Create a posting as the verified company.
6. Apply as the student.
7. Manage the application from the company dashboard.
8. Open Placement Analytics.

## Note

Django's built-in auth stores passwords securely using Django's password hashing system. Do not store plaintext passwords.
