import os
from app import create_app, db, swagger_api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

jwt = JWTManager(app)
jwt._set_error_handler_callbacks(swagger_api)


@app.before_first_request
def create_tables():
    db.create_all()
