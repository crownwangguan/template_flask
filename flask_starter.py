import os
from app import create_app, db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

jwt = JWTManager(app)


@app.before_first_request
def create_tables():
    db.create_all()
