# Requirements

- Docker
- Or Python 3.8+

# Description

This project was built using the Django, Celery, and Redis (backend) and HTML, CSS, JavaScript (frontend). The data is pulled from pokeapi.co every 30 minutes - based on the type of data, this didn't need to happen often but is more for demonstrative purposes - via a Celery task that populates the database with the first 151 Pokemon and relevant attributes e.g. type. This allows for retrieving and filtering data very quickly as it's done locally and can also be done if pokeapi.co is down. Pokemon can be filtered using the left-hand form and selected for export by clicking on the relevant row in the right hand table.

![image](https://user-images.githubusercontent.com/1469662/142439059-6fdf1bba-6587-4bba-bddb-1e0d1b9d4bb3.png)

# Set up

## Docker

```
# Clone the repo
$ git clone https://github.com/Qirky/pokedex.git
$ cd pokedex

# Build the docker container (only needs to be done once)
$ docker-compose build

# Start the container
$ docker-compose up
```

## Python 3.8

```
# Clone the repo
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

# Build the database schema & cache table
$ python manage.py migrate
$ python manage.py createcachetable cache_table

# Populate the database from pokeapi.co - does not run periodically
$ python manage.py populate

# Run server
$ python manage.py runserver
```

Access the server at http://localhost:8000/
