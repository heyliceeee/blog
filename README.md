# 📝 Notes by Alice

A clean and elegant blog built with **Flask**, featuring an authenticated admin panel, **full CRUD for posts**, a rich‑text editor powered by **CKEditor**, user authentication with **Flask‑Login**, and an SMTP‑based contact form.

Posts are stored in a **SQLite** database using **SQLAlchemy**, including title, subtitle, image, HTML content, publication date, reading time, and comments.

---

## ✨ Features

### 🌐 Public Blog
- Dynamic homepage listing all posts  
- Individual post pages  
- Fully formatted HTML content (CKEditor)  
- About page  
- Contact form with SMTP email sending  

### 🔐 Admin Panel (Protected)
- Login with hashed password  
- Logout  
- Fully protected routes using `@login_required`  
- Complete post management:
  - Create posts with CKEditor  
  - Edit posts with CKEditor  
  - Delete posts  
  - Manage posts in a responsive table view  

### 🗄 Storage
- **SQLite + SQLAlchemy** for posts and users  
- Full post model:
  - `title`  
  - `subtitle`  
  - `image`  
  - `published`  
  - `body` (HTML from CKEditor)  
  - `reading_time`  
  - `comments_count`  
  - `comments` (JSON string)  
- Automatic database updates after CRUD operations  

### 🎨 UI
- Responsive Bootstrap 5 theme  
- Modern layout inspired by the “Notes by Alice” design  
- CKEditor 4 integrated for rich‑text editing  
- Clean and intuitive admin interface  

---

## 🚀 How It Works

### Public Routes
- `/` — homepage with all posts  
- `/post/<id>` — single post page  
- `/about` — static About page  
- `/contact` — contact form (GET/POST)  

### Authentication Routes
- `/login` — login page  
- `/logout` — logout  

### Admin Routes (Protected)
- `/posts` — admin dashboard with post table  
- `/new-post` — create a new post  
- `/edit-post/<id>` — edit an existing post  
- `/delete-post/<id>` — delete a post  

All admin routes require authentication.

---

## 🔐 Security

- Password hashing using `generate_password_hash`  
- Authentication and session management with **Flask‑Login**  
- Secure sessions  
- Automatic redirect to login when accessing protected routes  
- Admin user created automatically on first run  
- CSRF protection via Flask‑WTF  

---

## 🛠 Technologies

- Python (Flask, Flask‑Login, SQLAlchemy, smtplib)  
- Flask‑WTF + WTForms  
- CKEditor 4 (rich‑text editor)  
- Jinja2 templating  
- Bootstrap 5  
- SQLite (posts + users)  
- JSON for comments