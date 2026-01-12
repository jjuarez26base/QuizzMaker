# Quizzma

A simple, dark-themed quiz management platform to help students create, edit, and take custom quizzes — fast.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](#) [![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen)](#) [![Django](https://img.shields.io/badge/django-4.x-4B8BBE)](#)

---

## Table of Contents
- Features
- Tech Stack
- Database Structure
- Project Milestones
- Installation
- Usage
- Credits
- License

---

## Features
- ✅ Unlimited quiz creation
- ✅ Full CRUD for quizzes, questions, and choices
- ✅ Gamified user profiles (points & bio)
- ✅ Admin dashboard: site stats, manage quizzes & user activation
- ✅ Mobile-responsive with sidebar navigation
- ✅ Dark-mode friendly UI

---

## Tech Stack
- Backend: Python, Django
- Data: Django Models (Quizzes, Questions, Choices, Tags, UserProfile)
- Frontend: HTML5, CSS3 (dark theme), JavaScript for interactivity
- Tools: VS Code, Canva, Coolors, Gemini, GitHub Copilot

---

## Database Structure (high level)
- UserProfile — extends Django User: points, bio, avatar
- Quiz — title, cover image, owner, tags, is_active
- Question — belongs to Quiz, text, ordering
- Choice — belongs to Question, text, is_correct
- Tag — many-to-many with Quiz

---

## Project Milestones
1. Planning — UX and data model definition  
2. Design — dark-mode UI and responsive layout  
3. Development — models, views, authentication, and admin tools  
4. Testing — manual QA, iterative bug fixes

---

## Installation & Setup

Open a terminal (macOS):

```bash
# Clone
git clone https://github.com/yourusername/quizzma.git
cd quizzma

# Virtualenv
python -m venv venv
source venv/bin/activate

# Dependencies
pip install -r requirements.txt
# or at minimum:
pip install django

# Migrate & admin
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Run server
python manage.py runserver

# Visit:
# http://127.0.0.1:8000/
```

---

## Usage
- Admins: use the Django admin or the built-in dashboard to manage users and quizzes.
- Users: sign up, create quizzes, add questions/choices, take quizzes and earn points.

---

## Credits
- Jason & Jesuse — Backend architecture  
- Angel — Backend support & logic  
- Design & Frontend — Quizzma team

Created: Dec 29th, 2025 — Jan 12th, 2026

---

## License
MIT — see LICENSE file for details

