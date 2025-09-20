# Clash_up

## Basic assumptions
+ Python >= 3.13
+ PostgreSQL >= 17.0
+ Max line length - 100 characters
+ Ruff for formatting and linting
+ Pytest for testing
+ uv for virtual environment management

## To run the project locally
```
uvicorn api.app:app
```

## To set up the database
```
inv run-postgres
```

## To load initial data
```
inv load-initial-data
```

## Swagger
```
http://localhost:8000/api/docs
```
