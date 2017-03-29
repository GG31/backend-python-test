from flask import Blueprint, render_template
from flask import (
    g,
    redirect,
    render_template,
    request,
    session,
    jsonify
    )
from alayatodo.models import Todo

todo = Blueprint('todo', __name__)


@todo.route('/todo/<id>/json', methods=['GET'])
@todo.route('/todo/<id>/json/', methods=['GET'])
def todo_json(id):
    if not session.get('logged_in'):
        return redirect('/login')
    myTodo = Todo.query.filter_by(id=id).first()
    if myTodo:
        return jsonify(dict(myTodo))
    else:
        return redirect('/todo')


@todo.route('/todo/<id>', methods=['GET'])
def todo(id):
    todo = Todo.query.filter_by(id=id).first()
    return render_template('todo.html', todo=todo)


def getTodos(page):
    todos = Todo.query.limit(todosPerPage).offset(todosPerPage * int(page))
    return todos

@todo.route('/todo', methods=['GET'])
@todo.route('/todo/page/<page>', methods=['GET'])
def todos(page=0):
    if not session.get('logged_in'):
        return redirect('/login')
    todos = getTodos(page)
    return render_template('todos.html', todos=todos, page=page)


@todo.route('/todo', methods=['POST'])
@todo.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')
    if request.form.get('description', '') == '':
        return redirect('/todo')
    result = 'Todo added'
    try:
        todo = Todo(session['user']['id'], request.form.get('description', ''))
        db.sessions.add(todo)
        db.sessions.commit()
    except:
        result = 'Error'
    page = 0
    return render_template('todos.html', todos=getTodos(page), result=result, page=page)

@todo.route('/todo/complete/<id>', methods=['POST'])
def todos_complete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    stmt = update(Todo).where(id=id).values(is_complete=1)
    db.execute(stmt).fetchall()
    return redirect('/todo')

@todo.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    result = 'Todo ' + id + ' deleted'
    try:
        Todo.query.filter_by(id=id).delete()
    except:
        result = 'Error'
    page = 0
    return render_template('todos.html', todos=getTodos(page), result=result, page=page)
