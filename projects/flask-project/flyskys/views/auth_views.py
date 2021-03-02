from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from sqlalchemy.exc import IntegrityError

from flyskys import db
from flyskys.forms import UserCreateForm, UserLoginForm
from flyskys.models import User

import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()

    # Case: 최종 회원가입
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            try:
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('main.index'))

            except IntegrityError:
                db.session.rollback()
                flash('이미 등록된 이메일입니다')

        else:
            flash('이미 존재하는 사용자입니다')

    # Case: 회원가입 bnt를 눌러 회원가입 창으로 이동하는 경우
    return render_template('auth/signup.html', form=form)


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()

    # POST 요청에 대해서는 로그인 수행
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = '존재하지 않는 사용자입니다.'
        elif not check_password_hash(user.password, form.password.data):
            error = '비밀번호가 올바르지 않습니다.'
        if error is None:
            # CASE: 사용자 존재 && 비밀번호 존재
            # session에 키와 키값을 저장
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        flash(error)

    # GET 요청에 대해서는 로인인 템플릿 렌더링
    return render_template('auth/login.html', form=form)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))


# decorator function
# 아래와 같이 decorator 함수를 생성하여 @login_required 애터테이션을 사요할 수 있다
# @login_required 애너테이션을 사용하면 데코레이터 함수가 먼저 실행되고
# 해당 데코레이터 함수는 g.user 유무를 조사하여 없으면 로그인 URL로 redirect 있으면 원래 함수를 그대로 실행한다
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
