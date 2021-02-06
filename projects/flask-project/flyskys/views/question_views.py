from flask import Blueprint, render_template
from flyskys.models import Question

# Blueprint 객체 생성
bp = Blueprint("question", __name__, url_prefix="/question")


@bp.route("/list/")
def _list():
    question_list = Question.query.order_by(Question.create_date.desc())
    return render_template("question/question_list.html", question_list=question_list)


@bp.route("/detail/<int:question_id>/")
def detail(question_id):
    # get_or_404는 해당 데이터를 찾을 수 없는 경우 404 페이지를 출력해 준다.
    question = Question.query.get_or_404(question_id)
    return render_template("question/question_detail.html", question=question)
