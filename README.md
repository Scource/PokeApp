# PokeApp

Simple Pokedex application.

## Prerequisites

- docker compose

## Setup

Clone git repository

```
git clone https://github.com/Scource/PokeApp
cd PokeApp
```

- From root application folder run `docker compose up`

- Migrate tables to new DB
  `docker compose exec pokeapp python manage.py migrate`

- For admin site access create superuser
  `docker-compose exec api python manage.py createsuperuser`

- Application should be up and running at `http://localhost:8000`

Now application is ready to use by logged user.
