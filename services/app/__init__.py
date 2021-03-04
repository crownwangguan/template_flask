from flask import Flask
from config import config
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restplus import Api
from flask_marshmallow import Marshmallow


login_manager = LoginManager()
login_manager.login_view = 'auth.login'

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}

mail = Mail()
bootstrap = Bootstrap()
db = SQLAlchemy()
ma = Marshmallow()
swagger_api = Api(version='1.0',
                  title='Flask Store',
                  doc='/doc',
                  description='A flask store template',
                  security='Bearer Auth',
                  authorizations=authorizations)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from app.item.resource import api as item_ns
    swagger_api.add_namespace(item_ns)

    from app.store.resource import api as store_ns
    swagger_api.add_namespace(store_ns)
    
    from app.api.resource import api as auth_ns
    swagger_api.add_namespace(auth_ns)
    
    from app.order.resource import api as order_ns
    swagger_api.add_namespace(order_ns)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    ma.init_app(app)
    swagger_api.init_app(app)

    return app
