from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db

bp = Blueprint('task', __name__)


def get_task(id, check_author=True):
    task = get_db().execute(
        'SELECT p.id, title, body, finish, author_id, email'
        ' FROM task p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if task is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and task['author_id'] != g.user['id']:
        abort(403)

    return task


@bp.route('/<int:id>', methods=['POST', 'GET'])
def task_detail(id):
    task = get_task(id)
    return render_template('task/task_detail.html', task=task)


@bp.route('/', methods=['POST', 'GET'])
def index():
    db = get_db()
    tasks = db.execute(
        'SELECT p.id, title, body, finish, author_id, email'
        ' FROM task p JOIN user u ON p.author_id = u.id'
        ' ORDER BY finish DESC'
    ).fetchall()
    return render_template('task/index.html', tasks=tasks)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        finish = request.form['finish']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO task (title, body, author_id, finish)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, g.user['id'], finish)
            )
            db.commit()
            return redirect(url_for('task.index'))

    return render_template('task/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    task = get_task(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        finish = request.form['finish']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE task SET title = ?, body = ?, finish = ? WHERE id = ?',
                (title, body, finish, id)
            )
            db.commit()
            return redirect(url_for('task.index'))

    return render_template('task/update.html', task=task)


@bp.route('/<int:id>/delete', methods=('POST', 'GET'))
@login_required
def delete(id):
    get_task(id)
    db = get_db()
    db.execute('DELETE FROM task WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('task.index'))
