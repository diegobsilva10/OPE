# import app
from flask import Flask

from .config import db, login_manager, migrate

from .blueprints.home.routes import home
from .blueprints.register.routes import register
from .blueprints.login.routes import login
from .blueprints.admin.routes import admin


def create_app(config):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost/TCC"
    app.config['SECRET_KEY'] = "f1S\xbd\xb4cK/\xf4\x11\x0f\xc7f\xda7@"

    db.init_app(app)

    # Blueprints
    app.register_blueprint(home)
    app.register_blueprint(login)
    app.register_blueprint(register)
    app.register_blueprint(admin)

    login_manager.init_app(app)

    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    return app
