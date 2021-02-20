# Flask

This repo can be used to create a flask online store app.

To run the app:

``` 
chmod +x entry_point.sh
./entry_point.sh {your email address} {email password}
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
- [ ] Add JWT authentication for resources
