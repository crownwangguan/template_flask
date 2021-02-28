# Flask

This repo can be used to create a flask online store app.

## Prerequisite:
Have PostgreSQL installed on your system. Or run a docker container of PostgreSQL.

Create a new folder: `postgres-data` to mount the volume.

```sh
docker run -d --name dev-postgres -e POSTGRES_PASSWORD={password} -v postgres-data:/var/lib/postgresql/data -p 5432:5432 postgres
```

Once docker container is spawned, enter the container to create new database and systemic user:
```sh
docker exec -it dev-postgres bash
# (Inside docker container)
psql -h localhost -U postgres
postgres=\# create database flask_store;
postgres=\# create user {db_user} with encrypted password '{db_password}';
postgres=\# grant all privileges on database flask_store to {db_user};
```

### To run the app:

Create a file `.env.dev` with content:
```
FLASK_APP={}
MAIL_USERNAME={}
MAIL_PASSWORD={}
FLASKY_ADMIN={}
PYTHONDONTWRITEBYTECODE=1
PYTHONUNBUFFERED=1
DEV_DATABASE_URL=postgresql://{}:{}@db:5432/{}
```
Create a file `.env.dev.db` with content:
```
POSTGRES_USER={}
POSTGRES_PASSWORD={}
POSTGRES_DB={}
```
``` 
docker-compose build && docker-compose up
```

Then go to url: `http://127.0.0.1:5000/`

## DataBase Architecture:
```sh

There are mainly four schemas 

* Users - details about the users
* Store - details about the store
* Items - details about the items
* Order - which is for ordering stuff

### DataBase Architecture

- store and item: one to many 
- item and order: many to many 

```

## Todo:

- [x] Create user model
- [x] User login page
- [x] User signup page
- [x] Connect db
- [x] Hash password
- [x] Add entry point shell script
- [x] Confirmation Email
- [x] Add JWT integration for api routes
- [x] Modify Store, Item, Order model
- [x] Add resource for model
- [x] Switch to postgresql
- [x] Add JWT authentication for resources
- [x] Dockerize app
- [x] Add Swagger
- [x] Authentication refactoring 401 (flask restplus break jwt)
- [ ] Add shopping cart logic