# Requirements

- Docker
- Or Python 3.8+

# Description

This project was built using the Django, Celery, and Redis (backend) and HTML, CSS, JavaScript (frontend). The data is pulled from pokeapi.co every 30 minutes - based on the type of data, this didn't need to happen often but is more for demonstrative purposes - via a Celery task that populates the database with the first 151 Pokemon and relevant attributes e.g. type. This allows for retrieving and filtering data very quickly as it's done locally and can also be done if pokeapi.co is down. Pokemon can be filtered using the left-hand form and selected for export by clicking on the relevant row in the right hand table.

# Set up

## Docker

```
# Clone the repo
$ git clone https://github.com/Qirky/pokedex.git

# Build and run the docker container
$ cd pokedex
$ docker-compose up --build

# Run the initial command to populate the database (runs automatically every 30 minutes)
$ docker-compose exec web python manage.py populate
```

## Python 3.8

```
# Clone th repo
$ git clone https://github.com/Qirky/pokedex.git

# Source a virtual environment
$ cd pokedex/django
$ python3 -m venv env

# Activate environment (Unix)
$ . env/bin/activate

# Activate environment (Windows)
$ .\env\Scripts\activate

# Install requirements
$ pip install -r requirements.txt

# Build the database schema
$ python manage.py migrate

# Populate the database from pokeapi.co - does not run periodically
$ python manage.py populate

# Run server
$ python manage.py runserver
```

Access the server at http://localhost:8000/
