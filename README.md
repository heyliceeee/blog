# 📝 Notes by Alice

A clean and elegant blog built with **Flask**, now featuring a **complete user system**, **three permission levels**, **full CRUD for posts**, rich‑text editing with **CKEditor**, authentication with **Flask‑Login**, and an SMTP‑based contact form.

The project has evolved from **SQLite** to a fully relational **PostgreSQL** database, supporting users, posts, and comments with proper foreign keys and role‑based access control.

---

## ✨ Features

### 🌐 Public Blog
- Dynamic homepage listing all posts  
- Individual post pages  
- Fully formatted HTML content (CKEditor)  
- About page  
- Contact page with SMTP email sending  
- Public viewing of comments  

### 👥 User System
- Full **user registration** page  
- Login / Logout  
- Password **hashing + salting** using `werkzeug.security`  
- **Dynamic sidebar** based on user role  
- **Protected routes** using Flask‑Login  

### 🔐 User Roles

#### **Unauthenticated User**
- Can view posts, comments, About, and Contact pages  

#### **Authenticated User**
- Everything an unauthenticated user can do  
- Can **write, edit, and delete their own comments**  

#### **Admin**
- Everything an authenticated user can do  
- Can **create, edit, and delete posts**  
- Can **delete any comment**  
- Can **edit the About page**  
- Can **edit the Contact page**  

---

## 🗄 Database — PostgreSQL + SQLAlchemy

The application now uses **PostgreSQL** with SQLAlchemy ORM models for:

- Users  
- Posts  
- Comments  

### Example Model Structure

**User**
- `id`  
- `username`  
- `email`  
- `password_hash`  
- `role` (guest / user / admin)

**Post**
- `id`  
- `title`  
- `subtitle`  
- `image`  
- `body` (HTML)  
- `published`  
- `reading_time`  

**Comment**
- `id`  
- `content`  
- `created_at`  
- `user_id` (FK)  
- `post_id` (FK)  

---

## 🎨 UI & Experience
- Responsive Bootstrap 5 layout  
- Dynamic sidebar based on user role  
- CKEditor 4 for rich‑text editing  
- Clean and intuitive admin interface  

---

## 🚀 Application Routes

### Public Routes
- `/` — homepage  
- `/post/<id>` — single post page  
- `/about` — About page  
- `/contact` — Contact form  

### Authentication Routes
- `/register` — user registration  
- `/login` — login  
- `/logout` — logout  

### User Routes (Authenticated)
- `/comment/<post_id>/new` — create comment  
- `/comment/<id>/edit` — edit own comment  
- `/comment/<id>/delete` — delete own comment  

### Admin Routes (Protected)
- `/posts` — admin dashboard  
- `/new-post` — create post  
- `/edit-post/<id>` — edit post  
- `/delete-post/<id>` — delete post  
- `/admin/edit-about` — edit About page  
- `/admin/edit-contact` — edit Contact page  

---

## 🔐 Security
- Password hashing + salting with `generate_password_hash`  
- Password verification with `check_password_hash`  
- Role‑based access control  
- Protected routes using Flask‑Login  
- CSRF protection via Flask‑WTF  

---

## 🛠 Technologies
- Python (Flask, Flask‑Login, SQLAlchemy, smtplib)  
- PostgreSQL  
- Flask‑WTF + WTForms  
- CKEditor 4  
- Jinja2 templating  
- Bootstrap 5  
