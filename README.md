# Scrapie

## Distributed scraping warehouse

### Project Structure

- Poetry is used to maintain virtual envs
- Python 3.7
- SQLAlchemy
- Postgresql
- Alembic
- asyncio

## Setup Project

```
$ poetry install
```

```
$ poetry run python main.py
```

## Migrations

Migrations are run using Alembic

```
$ alembic upgrade head
```

Create new migrations
```
$ alembic revision -m 'create users table'
```

Downgrade migrations
```
$ alembic downgrade -1
```

## API Docs

Access API docs at `host:port/docs`

For localhost `localhost:8000/docs`