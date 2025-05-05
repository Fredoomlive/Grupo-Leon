from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import os
from flask_migrate import Migrate


db = SQLAlchemy()
csrf = CSRFProtect()
migrate = Migrate()


def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    templates_dir = os.path.join(base_dir, '..', 'templates')

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    app.config['SECRET_KEY'] = 'B3t012**'  # Usa una clave fuerte y secreta
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///citas.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        from .models import Cita

    return app
