from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g
from werkzeug.utils import redirect

from flyskys import db
from flyskys.forms import CommentForm
from flyskys.models import Question, Answer, Comment
from .auth_views import login_required

bp = Blueprint('comment', __name__, url_prefix='/comment')

# QUESTION


@bp.route('/create/question/<int:question_id>', methods=('GET', 'POST'))
@login_required
def create_question(question_id):
    form = CommentForm()
    question = Question.query.get_or_404(question_id)

    if request.method == 'POST' and form.validate_on_submit():
        comment = Comment(user=g.user, content=form.content.data,
                          create_date=datetime.now(), question=question)
        db.session.add(comment)
        db.session.commit()
        return redirect('{}#comment_{}'.format(url_for('question.detail', question_id=question_id), commnet.id))

    return render_template('comment/comment_form.html', form=form)


@bp.route('/modify/question/<int:comment_id>', methods=('GET', 'POST'))
@login_required
def modify_question(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    if g.user != comment.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=comment.question.id))

    if request.method == 'POST':
        form = CommentForm()
        if form.validate_on_submit():
            form.populate_obj(comment)
            comment.modify_date = datetime.now()
            db.session.commit()
            return redirect('{}#comment_{}'.format(url_for('question.detail', question_id=comment.question.id), comment.id))

    else:
        form = CommentForm(obj=comment)

    return render_template('comment/comment_form.html', form=form)


@bp.route('/delete/question/<int:comment_id>')
@login_required
def delete_question(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    question_id = comment.question.id

    if g.user != comment.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))

    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for('question.detail', question_id=question_id))


# ANSWER

@bp.route('/create/answer/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def create_answer(answer_id):
    form = CommentForm()
    answer = Answer.query.get_or_404(answer_id)

    if request.method == 'POST' and form.validate_on_submit():
        comment = Comment(user=g.user, content=form.content.data,
                          create_date=datetime.now(), answer=answer)
        db.session.add(comment)
        db.session.commit()
        return redirect('{}#comment_{}'.format(url_for('question.detail', question_id=answer.question.id), comment.id))

    return render_template('comment/comment_form.html', form=form)


@ bp.route('/modify/answer/<int:comment_id>', methods=('GET', 'POST'))
@ login_required
def modify_answer(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    if g.user != comment.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=comment.answer.id))

    if request.method == 'POST':
        form = CommentForm()
        if form.validate_on_submit():
            form.populate_obj(comment)
            comment.modify_date = datetime.now()
            db.session.commit()
            return redirect('{}#comment{}'.format(url_for('question.detail', question_id=comment.answer.question.id), commnet.id))

    else:
        form = CommentForm(obj=comment)

    return render_template('comment/comment_form.html', form=form)


@ bp.route('/delete/answer/<int:comment_id>')
@ login_required
def delete_answer(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    question_id = comment.answer.question.id

    if g.user != comment.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))

    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for('question.detail', question_id=question_id))
