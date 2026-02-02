# Django URL Shortener Project

## Overview
A Django-based URL shortening application that allows users to create short links, track clicks, and manage link expiration. Includes user authentication, QR code generation, and dashboard management.

## Features
- User authentication with login/logout.
- Create, edit, delete short URLs.
- Custom short keys or auto-generated Base62 keys.
- URL expiration (date/time) with dashboard status.
- Click tracking for each URL.
- QR code generation for each short URL.
- Dashboard with active/expired link status.
- Base62 key generation to avoid collisions.

## Setup Instructions

1. Clone the repository
git clone <repository-url>
cd <project-directory>

2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Apply migrations
py manage.py makemigrations
python manage.py migrate

5. Run Server
python manage.py runserver