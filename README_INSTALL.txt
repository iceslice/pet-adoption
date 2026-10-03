Copy these files into your project (overwrite when asked):
  config/urls.py          -> pet_adoption/config/urls.py
  pets/*.py               -> pet_adoption/pets/
  pets/templates/         -> pet_adoption/pets/templates/

Then in the VS Code terminal (venv active):
  python manage.py makemigrations pets
  python manage.py migrate
  python manage.py createsuperuser
  python manage.py runserver

Add pets and set a pet image through http://127.0.0.1:8000/admin/

Favorites added: run `python manage.py makemigrations pets` then `migrate` again
(a new Favorite model was added). README.md and .gitignore go in the project root.
