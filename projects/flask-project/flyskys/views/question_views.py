from datetime import datetime
from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect
from .. import db
from ..models import Question
from ..forms import QuestionForm, AnswerForm
from .auth_views import login_required

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
@login_required
def create():
    form = QuestionForm()
    # CASE: 질문 최종 등록 (최종 등록은 POST 형식으로 전송된다)
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data,
                            content=form.content.data, create_date=datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    # CASE: 질문 리스트에서 질문 등록 버튼 클릭
    return render_template('question/question_form.html', form=form)


@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))

    # CASE: 질문수정을 마치고 저장을 누른 경우
    # validate_on_submit에서 QuestionForm을 검증한 뒤 이상이 없으면 변경된 데이터를 저장
    # 변경된 데이터를 적용하기 위해 form.populate_obj(question)을 이용해 form 변수에 들어 있는
    # 데이터를 question 객체에 적용한다
    if request.method == 'POST':
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:
        form = QuestionForm(obj=question)

    # CASE: 질문수정 버튼을 누른 경우
    # QuestionForm(obj=question)과 같이 조회한 데이터를 obj 매개변수에 전달하여
    # question_form을 띄우면 해당 질문의 기존 내용을 포함한 상태로 질문등록에 들어갈 수 있다
    return render_template('question/question_form.html', form=form)


@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))
