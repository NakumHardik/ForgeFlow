# ForgeFlow

A Material Inventory Management API built using FastAPI,
SQLite, SQLAlchemy, and Docker.

## Features

- Create, view, update, and delete materials
- Update material stock quantities
- Filter materials by minimum stock
- Calculate total inventory value
- Store data persistently using SQLite
- Run the API using Docker Compose
- Interactive API documentation with Swagger

## Tech Stack

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- Docker
- Docker Compose

## Run with Docker

Build and start the application:

    docker compose up --build

Open the API documentation:

    http://127.0.0.1:8000/docs

Stop the application using Ctrl + C.

## Run Locally

Install dependencies:

    python -m pip install -r requirements.txt

Start the API:

    python -m uvicorn main:app --reload

## Database

ForgeFlow uses SQLite to store material records.
Docker Compose mounts the database file so data
persists when the container is restarted.