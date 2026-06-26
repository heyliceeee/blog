# 📝 Notes by Alice — Flask Blog

A minimal and elegant blog built with **Flask**, using **Jinja2 templates**, a JSON file for post data, and an SMTP‑powered contact form. The project includes a homepage with all posts, individual post pages, an About page, and a fully functional contact form.

---

## ✨ Features

- **Dynamic blog posts** loaded from a JSON file  
- **Individual post pages** rendered via Jinja2  
- **About page** with author information  
- **Contact form with SMTP email sending**  
- **Responsive UI** using Bootstrap and a custom theme  
- **Simple, lightweight, and easy to extend**

## 🚀 How It Works

### Routes

- `/` — homepage with all posts  
- `/post/<id>` — single post page  
- `/about` — static About page  
- `/contact` — GET/POST form with email sending
  
## 🛠 Technologies

- Python (Flask, smtplib, EmailMessage)
- Jinja2 templating
- Bootstrap 5
- JSON for post storage
