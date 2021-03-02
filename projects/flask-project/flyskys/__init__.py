from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flaskext.markdown import Markdown

import config


naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
# 다른 모듈에서 db 객체를 호출하기 위해 global 선언
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    from . import models

    # Blueprint
    from .views import main_views, question_views, answer_views, auth_views, comment_views, vote_views

    # Register Blueprint
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(comment_views.bp)
    app.register_blueprint(vote_views.bp)

    # Filter
    from .filter import format_datetime
    # datetime이라는 이름으로 필터 등록
    app.jinja_env.filters['datetime'] = format_datetime

    Markdown(app, extensions=['nl2br', 'fenced_code'])

    return app
