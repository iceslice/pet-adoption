# Pet Adoption & Rescue Platform

A Django web application where users can browse pets available for adoption and submit adoption requests. It includes a template-based website and a REST API built with Django REST Framework. Administration is done through Django Admin.

## Features

**Website**
- Register, login, logout, and a profile page
- Browse pets as cards, with pagination
- Search and filter by name, animal type, breed, gender, location, and adoption status
- Pet details page (the Apply button is hidden for adopted pets)
- Adoption application form
- "My Adoption Requests" dashboard showing Pending / Approved / Rejected
- Favorite pets (bonus)
- Bootstrap 5 responsive layout, navigation bar, and success/error messages

**Admin**
- Add, edit, delete pets, change status, upload images
- View and manage adoption requests (approve / reject)

**Business rules**
1. Only available pets can be adopted.
2. A user cannot submit another request for a pet while they already have a pending one (checked in code and enforced by a database constraint).
3. When a request is approved, the pet becomes `Adopted`, so no further applications are accepted for it.

**REST API**
- Pets: full CRUD, search, filtering, pagination
- Adoption requests: list, create, retrieve, update (own requests only)
- Token authentication

## Tech stack
Python 3, Django, Django REST Framework, django-filter, Pillow, Bootstrap 5, SQLite.

## Setup (Windows / VS Code)

```powershell
git clone https://github.com/iceslice/pet-adoption.git pet_adoption
cd pet_adoption
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

If PowerShell blocks activation, run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

Open:
- Website: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
- API root: http://127.0.0.1:8000/api/

Add some pets (with images) in the admin panel to see them on the site.

## Website pages

| URL | Page |
|---|---|
| `/` | Home |
| `/pets/` | Pet list with search/filter |
| `/pets/<id>/` | Pet details |
| `/pets/<id>/apply/` | Adoption form (login required) |
| `/dashboard/` | My adoption requests |
| `/favorites/` | My favorite pets |
| `/profile/` | Profile |
| `/login/`, `/register/`, `/logout/` | Authentication |

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/pets/` | List pets (paginated) |
| GET | `/api/pets/<id>/` | Pet detail |
| POST | `/api/pets/` | Create pet (auth required) |
| PUT | `/api/pets/<id>/` | Update pet (auth required) |
| DELETE | `/api/pets/<id>/` | Delete pet (auth required) |
| GET | `/api/adoptions/` | List my adoption requests |
| POST | `/api/adoptions/` | Submit a request |
| GET | `/api/adoptions/<id>/` | My request detail |
| PUT | `/api/adoptions/<id>/` | Update my request |
| POST | `/api/token/` | Get an auth token |

Search and filters:
```
GET /api/pets/?search=golden
GET /api/pets/?animal_type=Dog
GET /api/pets/?gender=Male
GET /api/pets/?page=2
```

Authentication:
```powershell
curl.exe -X POST http://127.0.0.1:8000/api/token/ -d "username=USER&password=PASS"
curl.exe http://127.0.0.1:8000/api/adoptions/ -H "Authorization: Token <your-token>"
```

Note: the status of a request can only be changed by an admin (it is read-only in the API).

## Models

- **Pet**: name, animal_type, breed, age, gender, location, description, image, status, created_at
- **AdoptionRequest**: user, pet, phone, address, reason, previous_pet_experience, message, status, created_at
- **Favorite**: user, pet, created_at

One user can have many adoption requests; one pet can receive many adoption requests.

## Project structure
```
config/        project settings and root urls
pets/          models, views, forms, services (business rules), api, admin
pets/templates/  base layout, pet pages, registration pages
```
