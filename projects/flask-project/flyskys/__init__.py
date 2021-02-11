from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config


# 다른 모듈에서 db 객체를 호출하기 위해 global 선언
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

    # Blueprint
    from .views import main_views, question_views, answer_views

    # Register Blueprint
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)

    # Filter
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    return app
