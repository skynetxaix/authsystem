# AuthSystem

A registration and login system built with Django REST Framework, using Token Authentication (with expiration) and MySQL.

## Features

- User registration with hashed passwords
- Password strength validation
- Duplicate username/email prevention
- Login with Token generation
- Token expiration (24 hours)
- Logout (token invalidation)
- Protected profile endpoint

## Tech Stack

- Python / Django
- Django REST Framework
- MySQL

## Getting Started

```bash
git clone https://github.com/skynetxaix/authsystem.git
cd authsystem
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
DB_NAME=authsystem_db
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=your-secret-key
```

Create the database in MySQL:

```sql
CREATE DATABASE authsystem_db CHARACTER SET utf8mb4;
```

Run migrations and start the server:

```bash
python manage.py migrate
python manage.py runserver
```

The API will be available at `http://localhost:8000/`.

## Endpoints

### Register
```
POST /api/register/
```
```json
{
    "username": "testuser",
    "email": "test@test.com",
    "password": "StrongPass@123"
}
```

### Login
```
POST /api/login/
```
```json
{
    "username": "testuser",
    "password": "StrongPass@123"
}
```
Response:
```json
{
    "token": "8b3fd6cae75bbf261194869d0194e7efbb6fe41c"
}
```

### Profile (requires Token)
```
GET /api/profile/
```
Header:
```
Authorization: Token 8b3fd6cae75bbf261194869d0194e7efbb6fe41c
```

### Logout (requires Token)
```
POST /api/logout/
```
Header:
```
Authorization: Token 8b3fd6cae75bbf261194869d0194e7efbb6fe41c
```

## Notes

- Tokens expire after 24 hours. Expired tokens are rejected on protected endpoints (except logout).
- Passwords are validated against Django's built-in password strength rules.
