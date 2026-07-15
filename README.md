# AuthSystem

A simple registration and login system built with Django REST Framework, using Token Authentication and MySQL.

## Features

- User registration with hashed passwords
- Login with Token generation
- Protected profile endpoint (requires valid Token)

## Tech Stack

- Python / Django
- Django REST Framework
- MySQL

## Endpoints

### Register
```
POST /api/register/
```
```json
{
    "username": "testuser",
    "email": "test@test.com",
    "password": "test12345"
}
```

### Login
```
POST /api/login/
```
```json
{
    "username": "testuser",
    "password": "test12345"
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
