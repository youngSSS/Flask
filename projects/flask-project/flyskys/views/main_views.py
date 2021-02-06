from flask import Blueprint, url_for
from werkzeug.utils import redirect

# Blueprint 객체 생성
bp = Blueprint("main", __name__, url_prefix="/")


@bp.route("/hello")
def hello_flyskys():
    return "Hello, FlySkys!"


@bp.route("/")
def index():
    # redirect 함수는 입력 받은 URL으로 redirect 하고,
    # url_for 함수는 라우트가 설정된 함수명으로 URL을 역으로 찾아 준다
    # url_for의 question은 등록된 Blueprint 이름,
    # _list는 Blueprint에 등록된 함수명이라고 생각하자
    return redirect(url_for("question._list"))
