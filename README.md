# 📝 Notes by Alice — Flask Blog

A simple and elegant blog application built with **Flask**, using **Jinja templates** and a JSON file as the data source. The project renders a homepage with all posts, individual post pages, and an About page.

---

## 🚀 Features

- **Homepage listing all blog posts**  
  Posts are loaded from a JSON file and displayed dynamically using Jinja loops.

- **Individual post pages**  
  Each post includes title, date, reading time, image, subtitle, body text, and comments.

- **About page**  
  A static page describing the author, professional background, education, and portfolio.

- **Responsive UI**  
  Built with Bootstrap and a developer‑friendly theme.

- **Comment section per post**  
  Comments are rendered from the JSON structure using Jinja loops.

---

## 🧱 Project Structure

- **app.py** — Flask application with three routes:  
  - `/` → homepage  
  - `/post/<index>` → individual post  
  - `/about` → about page

- **templates/**  
  - `index.html` — blog list  
  - `blog-post.html` — single post  
  - `about.html` — author profile

- **static/**  
  - Images, CSS, JS, and theme assets

- **blog-data.txt**  
  JSON file containing all posts, metadata, and comments.

---

## 🛠️ How It Works

1. The app loads all posts from a JSON file at startup.  
2. Flask routes pass the data to Jinja templates.  
3. Templates render posts, metadata, images, and comments.  
4. The UI uses Bootstrap components and a custom theme.

---

## 📌 Technologies Used

- **Python** (Flask, JSON handling)  
- **HTML5 / Jinja2** templating  
- **Bootstrap** for layout and styling  
- **Static assets** (images, icons, theme)

---

## 🎯 Purpose

This project serves as a clean, minimal example of a **Flask‑based blog**, ideal for learning:

- Routing  
- Template rendering  
- Dynamic content loading  
- Structuring small Flask applications
- **A version with badges, screenshots, or installation steps**

Just tell me what direction you want next.
