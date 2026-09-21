# UniPlacementHub 🎓

A university internship and job placement management portal built with **Django, PostgreSQL, Bootstrap, and SQL**.

UniPlacementHub provides a centralized platform where students can discover and apply for internships and jobs, companies can publish opportunities and manage applicants, and the university placement cell can verify companies, manage placement drives, and analyze placement activity.

---

## 📌 Project Overview

UniPlacementHub is designed as a **DBMS-focused university placement system** with three major user roles:

* **Students** — maintain profiles, browse opportunities, apply, and track application status.
* **Companies / Recruiters** — create company profiles, publish internship/job postings, review applicants, and update application status.
* **Placement Cell / Administrators** — verify companies, manage placement drives, maintain eligibility rules, and monitor placement analytics.

The project emphasizes relational database design, normalization, referential integrity, indexing, constraints, transactions, and SQL-based analytics.

### Technology Stack

| Layer           | Technology                          |
| --------------- | ----------------------------------- |
| Backend         | Python, Django                      |
| Database        | PostgreSQL                          |
| Frontend        | HTML, Bootstrap 5, Django Templates |
| Authentication  | Django Authentication               |
| Database Access | Django ORM + Raw SQL                |
| Version Control | Git / GitHub                        |
| Deployment      | PostgreSQL-compatible hosting       |

---

# ✨ Features

## 👨‍🎓 Student

* Student registration and login
* Student profile management
* Department and graduation year
* CGPA tracking
* Skills management
* Resume URL
* Browse internship and job postings
* Filter opportunities by type, department, skills, and eligibility
* Apply to opportunities
* Prevent duplicate applications
* Track application status:

  * Applied
  * Shortlisted
  * Rejected
  * Selected
* View application history

## 🏢 Company / Recruiter

* Company registration and login
* Company profile
* Admin verification
* Create internship and full-time job postings
* Define:

  * Minimum CGPA
  * Eligible departments
  * Required skills
  * Deadline
  * Number of positions
  * Location
  * Remote / onsite status
  * Salary / stipend
* View applicants
* Shortlist applicants
* Reject applicants
* Select candidates
* Automatic position-limit validation

## 🏫 Placement Cell / Admin

* Django admin dashboard
* Verify company accounts
* Manage students and companies
* Manage departments and skills
* Create placement drives
* Define drive eligibility
* View placement analytics
* Monitor applications and selections

---

# 🗂️ Project Structure

```text
UniPlacementHub/
│
├── manage.py
├── requirements.txt
├── README.md
├── seed_demo.py
├── setup_windows.bat
├── setup.sh
├── .gitignore
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── students/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── companies/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── postings/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── applications/
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── placement/
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── queries/
│   ├── advanced_queries.sql
│   └── company_statistics.sql
│
├── templates/
│   └── ...
│
└── static/
    └── ...
```

---

# 🗃️ Database Design

The application uses a relational database design centered around students, companies, postings, applications, departments, skills, and placement drives.

## ER Diagram

![UniPlacementHub ER Diagram](docs/er-diagram.png)

> Place the downloaded `er-diagram.png` inside the project's `docs/` directory before pushing to GitHub.

The main relationships include:

```text
User
 │
 ├── UserProfile
 │
 ├── Student ─────── Department
 │      │
 │      └──────────── Skill
 │
 └── Company
         │
         └────────── Posting
                       │
                       ├── Department
                       ├── Skill
                       ├── PlacementDrive
                       │
                       └── Application ─── Student
```

---

# 🧩 Normalization Approach

The database follows relational normalization principles, primarily targeting **Third Normal Form (3NF)**.

### 1NF — Atomic Values

Attributes contain atomic values rather than repeating groups.

For example, student skills are not stored as:

```text
"Python, Django, SQL, PostgreSQL"
```

Instead, skills are represented using a separate `Skill` table and a many-to-many relationship.

### 2NF — No Partial Dependencies

Non-key attributes depend on the complete primary key.

For example, the `Application` entity stores application-specific information such as:

```text
posting_id
student_id
status
applied_at
updated_at
```

### 3NF — No Transitive Dependencies

Independent entities are separated into their own tables.

For example:

```text
Department
Skill
Company
Student
Posting
Application
PlacementDrive
```

are maintained separately rather than storing duplicated department, company, or skill information inside every posting/application record.

### Many-to-Many Relationships

The database uses junction tables for many-to-many relationships.

Examples:

```text
Student ↔ Skill
Posting ↔ Skill
Posting ↔ Department
PlacementDrive ↔ Department
```

This reduces duplication and improves data integrity.

---

# ⚡ Database Constraints

The system uses database constraints to maintain data integrity.

Examples include:

### Primary Keys

Every major entity has a primary key.

```text
Student.id
Company.id
Posting.id
Application.id
Skill.id
Department.id
```

### Foreign Keys

Examples:

```text
Student.department_id → Department.id

Posting.company_id → Company.id

Application.posting_id → Posting.id

Application.student_id → Student.id
```

### Unique Constraint

A student cannot apply to the same posting more than once:

```text
UNIQUE(posting_id, student_id)
```

### Check Constraints / Validation

CGPA is restricted to the valid range:

```text
0.0 <= CGPA <= 4.0
```

Posting positions and other eligibility values are validated as well.

---

# 🚀 Indexes

Indexes are added to frequently searched or joined columns to improve query performance.

Important indexes include:

```text
Student.cgpa
Student.department_id

Posting.company_id
Posting.type
Posting.status
Posting.deadline

Application.student_id
Application.posting_id
Application.status
```

These indexes support common operations such as:

* Finding eligible students
* Finding postings by company
* Finding open internships
* Searching applications by status
* Finding applications belonging to a student
* Finding applicants for a posting

---

# 🔎 Complex SQL Queries

The project includes SQL examples in:

```text
queries/
├── advanced_queries.sql
└── company_statistics.sql
```

## Query 1 — Eligible CSE Students Applying to Recent Remote Internships

```sql
SELECT DISTINCT
    s.id,
    s.full_name,
    s.cgpa,
    p.title,
    p.deadline
FROM students_student s
JOIN students_department d
    ON s.department_id = d.id
JOIN applications_application a
    ON a.student_id = s.id
JOIN postings_posting p
    ON a.posting_id = p.id
WHERE d.name = 'CSE'
  AND s.cgpa >= 3.5
  AND p.is_remote = TRUE
  AND p.type = 'internship'
  AND a.applied_at >= CURRENT_TIMESTAMP - INTERVAL '7 days'
ORDER BY s.cgpa DESC;
```

### Explanation

This query combines multiple normalized tables to identify students who:

* Belong to CSE
* Have CGPA ≥ 3.5
* Applied during the last seven days
* Applied for remote internships

It demonstrates the use of:

* Multiple joins
* Filtering
* Date arithmetic
* Sorting
* Relational foreign keys

---

## Query 2 — Company Application Statistics

```sql
SELECT
    c.company_name,
    COUNT(a.id) AS total_applications,
    COUNT(*) FILTER (WHERE a.status = 'selected') AS selected_students,
    COUNT(*) FILTER (WHERE a.status = 'shortlisted') AS shortlisted_students,
    COUNT(*) FILTER (WHERE a.status = 'rejected') AS rejected_students
FROM companies_company c
JOIN postings_posting p
    ON p.company_id = c.id
LEFT JOIN applications_application a
    ON a.posting_id = p.id
GROUP BY c.id, c.company_name
ORDER BY total_applications DESC;
```

### Explanation

This query generates company-level placement statistics.

It calculates:

* Total applications
* Selected students
* Shortlisted students
* Rejected students

It demonstrates:

* `JOIN`
* `LEFT JOIN`
* `COUNT`
* Conditional aggregation
* `GROUP BY`
* Sorting

---

## Query 3 — Oversubscribed Job Postings

```sql
SELECT
    p.id,
    p.title,
    p.positions,
    COUNT(a.id) AS total_applications
FROM postings_posting p
LEFT JOIN applications_application a
    ON a.posting_id = p.id
GROUP BY p.id, p.title, p.positions
HAVING COUNT(a.id) > p.positions
ORDER BY total_applications DESC;
```

### Explanation

This query identifies postings where the number of applications exceeds the number of available positions.

For example:

```text
Positions:     5
Applications:  87
```

This can be useful for placement-cell analytics and recruiter dashboards.

---

# 👁️ Views

The application provides analytics through Django views backed by relational queries.

Examples include:

* Placement statistics
* Company statistics
* Application status summaries
* Drive-level analytics

The SQL query files can also be adapted into PostgreSQL database views for production deployments.

---

# 🔄 Transactions

Transactions are used for operations where multiple database changes must remain consistent.

One important example is candidate selection.

When a recruiter selects a candidate, the application uses a database transaction with row-level locking:

```python
with transaction.atomic():
    application = (
        Application.objects
        .select_for_update()
        .get(pk=application_id)
    )

    posting = (
        Posting.objects
        .select_for_update()
        .get(pk=application.posting_id)
    )

    # Validate available positions
    # Update application status
```

This helps prevent race conditions when multiple users attempt to select candidates for the same limited number of positions.

---

# 🔐 Application Integrity

The application process validates:

1. Student authentication
2. Student profile availability
3. Posting status
4. Application deadline
5. CGPA eligibility
6. Department eligibility
7. Duplicate application prevention

The database-level unique constraint provides an additional layer of protection:

```text
(posting_id, student_id)
```


## 5. Create Admin Account

```powershell
python manage.py createsuperuser
```

Enter:

```text
Username
Email
Password
```

---

## 6. Load Demo Data

```powershell
python seed_demo.py
```

This creates sample:

* Departments
* Skills
* Demo database records

---

## 7. Start the Development Server

```powershell
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Admin dashboard:

```text
http://127.0.0.1:8000/admin/
```

---

# 🧪 Example Demo Flow

### Student

```text
Register
   ↓
Complete Profile
   ↓
Add Skills
   ↓
Browse Jobs
   ↓
Apply
   ↓
Track Application
```

### Company

```text
Register
   ↓
Complete Company Profile
   ↓
Admin Verification
   ↓
Create Job/Internship
   ↓
View Applicants
   ↓
Shortlist
   ↓
Select / Reject
```

### Placement Cell

```text
Admin Login
   ↓
Verify Companies
   ↓
Create Placement Drive
   ↓
Monitor Applications
   ↓
View Analytics
```

---

# 📊 DBMS Concepts Demonstrated

This project demonstrates practical implementation of:

* Relational database design
* Entity Relationship modeling
* Primary keys
* Foreign keys
* Candidate/unique constraints
* Check constraints
* Normalization
* 1NF
* 2NF
* 3NF
* Many-to-many relationships
* Junction tables
* Database indexes
* Complex joins
* Aggregation
* Filtering
* Transactions
* Row-level locking
* Referential integrity
* SQL analytics
* Django ORM
* Raw SQL
* PostgreSQL

---

# 🔮 Future Improvements

Possible extensions include:

* Email notifications
* Resume file uploads
* Advanced recommendation engine
* Student skill-gap analysis
* Company dashboards
* Placement-drive registration
* Interview scheduling
* Automated eligibility matching
* PostgreSQL database views
* Stored procedures
* REST API
* Docker deployment
* Cloud deployment
* CI/CD with GitHub Actions

---

# 🌐 Live Demo

**Live link:** Not deployed yet.

Once deployed, replace this section with:

```text
Live Demo: https://your-domain.com
```

For example:

```markdown
## 🌐 Live Demo

[Visit UniPlacementHub][(http://127.0.0.1:8000/)]
```

---



# 👨‍💻 Author

**Mumnur Jannat Riha**

University DBMS / Software Engineering Project

**Project:** UniPlacementHub
**Technology:** Django + PostgreSQL + Bootstrap

