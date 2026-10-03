# 🐾 PawCare — Pet Adoption & Rescue Platform

A complete assignment-ready Django project for a Pet Adoption & Rescue Platform. It includes a Django Template website, Django REST Framework API, authentication, admin management, adoption workflow, business rules, and optional bonus features.

## Assignment coverage

### Required
- User registration, login, logout, profile/dashboard
- Pet browsing with image, type, breed, age, gender, location, description, status
- Search/filter by pet name, animal type, breed, gender, location, adoption status
- Pet details page
- Adoption application form
- My Adoption Requests dashboard
- Django Admin for pets and adoption requests
- Business rules:
  - only available pets can be adopted
  - one user cannot create more than one pending request for the same pet
  - approving a request marks the pet as Adopted and rejects other pending requests
- REST API endpoints for pets and adoption requests
- API search and filter

### Bonus features
- ❤️ Favorites
- 🌐 Website pagination
- 📄 API pagination
- 🔑 DRF Token Authentication
- 🐶 Pet categories via `animal_type`: Dog, Cat, Bird, Rabbit, Other
- Automated business-logic tests
- GitHub Codespaces-ready development container

## Project structure

```text
pet_adoption_platform/
├── .devcontainer/
│   └── devcontainer.json
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── pets/
│   ├── management/commands/seed_data.py
│   ├── migrations/0001_initial.py
│   ├── admin.py
│   ├── api_urls.py
│   ├── api_views.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── pagination.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── services.py
│   ├── urls.py
│   └── views.py
├── static/css/style.css
├── templates/
│   ├── base.html
│   ├── partials/
│   ├── pets/
│   └── registration/
├── tests/test_business_logic.py
├── media/
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── requirements.txt
└── README.md
```

## 1. GitHub Codespaces — easiest method

You do NOT need Django installed on your own computer first.

1. Create a GitHub repository.
2. Upload this entire project folder.
3. Open the repository in **GitHub Codespaces**.
4. The included `.devcontainer/devcontainer.json` automatically installs packages and runs migrations.
5. In the Codespaces terminal run:

```bash
python manage.py createsuperuser
python manage.py seed_data
python manage.py runserver 0.0.0.0:8000
```

6. Open the forwarded port **8000**.

## 2. Normal local setup

Use Python 3.12, 3.13, or 3.14.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_data
python manage.py runserver
```

## 3. Admin

Open:

`/admin/`

Use the superuser created with:

```bash
python manage.py createsuperuser
```

### Admin workflow

- Add/edit/delete pets.
- Upload pet images.
- Change a pet between Available and Adopted.
- Review adoption requests.
- Set a request to Rejected.
- Set a request to Approved. The project then atomically marks that pet as Adopted and rejects all other pending requests for that pet.

## 4. Website pages

- `/` — Home
- `/pets/` — Pet list + search/filter + pagination
- `/pets/<id>/` — Pet details
- `/pets/<id>/adopt/` — Adoption form
- `/dashboard/` — My adoption requests
- `/profile/` — User profile
- `/favorites/` — Favorite pets (bonus)
- `/register/` — Register
- `/login/` — Login
- `/logout/` — Logout
- `/admin/` — Django Admin

## 5. REST API

### Pets

```text
GET    /api/pets/
GET    /api/pets/<id>/
POST   /api/pets/
PUT    /api/pets/<id>/
PATCH  /api/pets/<id>/
DELETE /api/pets/<id>/
```

Public users can read pets. Only staff/admin users can create, edit, or delete pets.

### Adoption requests

```text
GET    /api/adoptions/
POST   /api/adoptions/
GET    /api/adoptions/<id>/
PUT    /api/adoptions/<id>/
PATCH  /api/adoptions/<id>/
DELETE /api/adoptions/<id>/
```

A logged-in API user can only see and manage their own requests. The `status` field is controlled by the admin workflow.

### Search and filtering

```text
GET /api/pets/?search=golden
GET /api/pets/?animal_type=Dog
GET /api/pets/?gender=Male
GET /api/pets/?location=Dhaka
GET /api/pets/?status=available
```

The API also supports pagination:

```text
GET /api/pets/?page=2
GET /api/pets/?page=2&page_size=12
```

### Token authentication (bonus)

Get a token:

```text
POST /api/token/
```

Send `username` and `password` and receive a token.

Then authenticate requests with:

```http
Authorization: Token YOUR_TOKEN_HERE
```

This is the built-in DRF TokenAuthentication flow.

## 6. Test business logic

```bash
python manage.py test tests
```

The tests cover the key rules from the assignment.

## 7. GitHub submission checklist

Before submitting:

```bash
git status
git add .
git commit -m "Complete pet adoption platform assignment"
git push origin main
```

Submit the GitHub repository URL together with this repository's `README.md`, `requirements.txt`, and database migration files.

## 8. Important security note

The development project uses a fallback development `SECRET_KEY` and `DEBUG=1`. For a real deployment, set environment variables and use `DEBUG=0`.

## 9. Technology versions

This project is pinned to Django 6.1.1, Django REST Framework 3.18.1, and Pillow 12.3.0 in `requirements.txt`.
