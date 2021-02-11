from datetime import datetime
from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect
from .. import db
from ..models import Question
from ..forms import QuestionForm, AnswerForm

# Blueprint 객체 생성
bp = Blueprint("question", __name__, url_prefix="/question")


@bp.route("/list/")
def _list():
    # GET 방식으로 요청한 아래와 같은 URL에서 page 값 5를 가져올 때 사용
    # localhost:5000/question/list/?page=5
    page = request.args.get('page', type=int, default=1)
    question_list = Question.query.order_by(Question.create_date.desc())
    question_list = question_list.paginate(page, per_page=10)
    return render_template("question/question_list.html", question_list=question_list)


@bp.route("/detail/<int:question_id>/")
def detail(question_id):
    form = AnswerForm()
    # get_or_404는 해당 데이터를 찾을 수 없는 경우 404 페이지를 출력해 준다.
    question = Question.query.get_or_404(question_id)
    return render_template("question/question_detail.html", question=question, form=form)


@bp.route('/create/', methods=('GET', 'POST'))
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data,
                            content=form.content.data, create_date=datetime.now())
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)
