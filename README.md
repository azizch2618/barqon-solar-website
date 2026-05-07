# BARQON Solar Energy Platform

A modern full-stack solar company platform built with Django for lead generation, quotation management, customer interaction, and solar engineering workflows.

---

## 🚀 Features

### 🌞 Solar Company Website

* Premium responsive landing page
* Dark/light theme support
* Modern solar business UI
* Mobile responsive design

### 📋 Smart Quote System

* Quick quote form
* Detailed solar assessment form
* Load-based calculation system
* Customer lead generation

### 📄 Proposal & Quotation System

* Multi-page solar proposal PDF
* Technical breakdown
* Cost estimation
* Terms & conditions
* Signature page

### 👨‍💼 Admin Dashboard

* Lead management system
* Customer details tracking
* Engineering tools
* Staff management modules
* Project management

### ⚡ Engineering Features

* Solar sizing calculations
* ROI estimation
* Load calculations
* Battery backup calculations
* Cable and protection recommendations

---

# 🛠 Tech Stack

### Backend

* Python
* Django

### Frontend

* HTML5
* CSS3
* JavaScript

### Database

* SQLite (Development)

### PDF Generation

* WeasyPrint / ReportLab

---

# 📦 Installation Guide

## 1️⃣ Clone Project

```bash
git clone <repository-url>
cd barqon_project
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv env
```

### Activate Environment

#### Windows

```bash
env\Scripts\activate
```

#### Mac/Linux

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 5️⃣ Run Development Server

```bash
python manage.py runserver
```

Open browser:

```text
http://127.0.0.1:8000/
```

---

# 🔐 Admin Access

### Django Admin Panel

```text
http://127.0.0.1:8000/admin/
```

### Frontend Admin Dashboard

```text
http://127.0.0.1:8000/admin-dashboard/
```

---

# 📁 Project Structure

```text
barqon_project/
│
├── manage.py
├── requirements.txt
├── README.md
│
├── templates/
├── static/
├── media/
├── apps/
│
├── barqon_project/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
└── db.sqlite3
```

---

# ⚙️ Core Functionalities

* Customer lead capture
* Dynamic solar calculation
* Proposal generation
* Mobile responsive UI
* CRM-style lead management
* Admin engineering tools

---

# 📱 Responsive Design

The platform is optimized for:

* Desktop
* Tablet
* Mobile devices

---

# 🚀 Deployment

Recommended Hosting:

* Render
* Railway
* DigitalOcean

Recommended Domain Providers:

* Namecheap
* GoDaddy

---

# 🔧 Production Setup

Before deployment:

```bash
python manage.py collectstatic
```

Ensure:

* DEBUG = False
* ALLOWED_HOSTS configured
* Static files configured properly

---

# 📞 Support

For setup assistance or project support, contact the developer.

---

# © BARQON Solar Energy

Built for modern solar business operations and customer management.
