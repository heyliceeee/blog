# 📝 Notes by Alice

A clean and elegant blog built with **Flask**, featuring a public blog, an authenticated admin panel, full CRUD for posts, and an SMTP‑powered contact form.  
Posts are stored in a JSON file, while user authentication is handled through **Flask‑Login** and **SQLAlchemy**.

---

## ✨ Features

### Public Blog
- Dynamic homepage listing all posts  
- Individual post pages  
- About page  
- Contact form with SMTP email sending  

### Admin Panel (Protected)
- Login with hashed password  
- Logout  
- Fully protected routes using Flask‑Login  
- CRUD operations for posts:
  - Create  
  - Edit  
  - Delete  
  - Manage posts in a responsive table view  

### Storage
- Posts stored in `blog-data.txt` (JSON)  
- Automatic JSON updates after CRUD actions  
- SQLite database for user authentication  

### UI
- Responsive Bootstrap 5 theme  
- Custom “Notes by Alice” styling  
- Clean admin interface  

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
- `/posts` — admin dashboard with table of posts  
- `/create-post` — create a new post  
- `/edit-post/<id>` — edit an existing post  
- `/delete-post/<id>` — delete a post  

All admin routes require authentication via `@login_required`.

---

## 🔐 Security

- Password hashing using `generate_password_hash`  
- Authentication and session management with Flask‑Login  
- Automatic redirect to login when accessing protected routes  
- Prevents logged‑in users from accessing the login page  
- Admin user created automatically on first run  

---

## 🛠 Technologies

- Python (Flask, Flask‑Login, SQLAlchemy, smtplib)  
- Jinja2 templating  
- Bootstrap 5  
- JSON for post storage  
- SQLite for user storage  
