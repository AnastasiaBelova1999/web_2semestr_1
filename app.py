import hashlib

import mysql
import flask_login
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import login_required
import mysql.connector

from mysql_db import MySQL

app = Flask(__name__)
app.secret_key = 'asjdfbajSLDFBhjasbfd'
app.debug = True
app.config.from_pyfile('config.py')
db = MySQL(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(login):
    cursor = db.db.cursor(named_tuple=True)
    cursor.execute('select id, login from users_exam where id = %s', (login,))
    user_db = cursor.fetchone()
    if user_db:
        user = User()
        user.id = user_db.id
        user.login = user_db.login
        return user
    return None


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template("index.html", authorization=False, login="anonimus", login_false=False)


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    if request.method == 'GET':
        login: str
        if flask_login.current_user.is_anonymous:
            login = "anonymus"
        else:
            login = flask_login.current_user.login
        return render_template("index.html", authorization=not flask_login.current_user.is_anonymous, login=login)
    elif request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        password_hash = hashlib.sha224(password.encode()).hexdigest()
        if username and password:
            cursor = db.db.cursor(named_tuple=True, buffered=True)
            try:
                cursor.execute(
                    "SELECT id,login FROM users_exam WHERE `login` = '%s' and `password_hash` = '%s'" % (
                        username, password_hash))
                user = cursor.fetchone()
            except Exception:
                cursor.close()
                return render_template("index.html", authorization=False,
                                       login="anonimus", login_false=True)
            cursor.close()
            if user is not None:
                flask_user = User()
                flask_user.id = user.id
                flask_user.login = user.login
                flask_login.login_user(flask_user, remember=True)
                return render_template("index.html", authorization=not flask_login.current_user.is_anonymous,
                                       login=user.login, login_false=False)
            else:
                flash("Не правильный логин или пароль")
                return render_template("index.html", authorization=False,
                                       login="anonimus", login_false=True)
        else:
            flash("Не правильный логин или пароль")
            return render_template("index.html", authorization=False,
                                   login="anonimus", login_false=True)


@app.route('/logout', methods=['GET'])
def logout():
    flask_login.logout_user()
    return render_template("index.html", authorization=not flask_login.current_user.is_anonymous, login="anonimus",
                           login_false=False)


@app.route('/list', methods=['GET'])
@login_required
def list():
    lists = db.select(None, "lists")
    login = flask_login.current_user.login
    types = dict(db.select(None, "types"))
    status = dict(db.select(["id", "title"], "status"))
    return render_template("call-list.html", login=login, lists=lists, types=types, status=status)


@app.route('/list/delete', methods=['POST'])
@login_required
def list_delete():
    id = request.form.get("id")
    cursor = db.db.cursor()
    cursor.execute("DELETE FROM `lists` WHERE `lists`.`id` = '%s'" % id)
    db.db.commit()
    cursor.close()
    return redirect("/list")


@app.route('/list/edit', methods=['POST'])
@login_required
def list_edit():
    try:
        list_id = request.form.get("list_id")
        date = request.form.get("data")
        login = request.form.get("login_users")
        type_id = request.form.get("type_id")
        status_id = request.form.get("status_id")
        message = request.form.get("message")
        statuss = db.select(None, "status")
        types = db.select(None, "types")
        sub = {
            'list_id': list_id,
            'date': date,
            'login_users': login,
            'type_id': type_id,
            'status_id': status_id,
            'message': message
        }
        return render_template("list_edit.html", sub=sub, types=types, statuss=statuss,
                               login=flask_login.current_user.login, user_id=flask_login.current_user.id
                               , user_role=1, list_id=list_id)

    except Exception:
        return redirect(url_for("list"))


@app.route('/list/edit/submit', methods=['POST'])
@login_required
def sub_edit_submit():
    list_id = request.form.get("id")
    date = request.form.get("data")
    type_id = request.form.get("type_id")
    status_id = request.form.get("status_id")
    message = request.form.get("message")

    if date and status_id and type_id:
        cursor = db.db.cursor(named_tuple=True)
        try:
            cursor.execute(
                "UPDATE `lists` SET  `data` = '%s', `status_id` = '%s', `type_id` = '%s',`message` = '%s' WHERE `lists`.`id` = '%s'" % (
                    date, status_id, type_id, message, list_id))
            db.db.commit()
            cursor.close()
            return redirect("/list")
        except Exception:
            return redirect("/list")
    else:
        return redirect("/list")


@app.route('/list/new', methods=['POST', 'GET'])
@login_required
def sub_new():
    if request.method == 'GET':
        types = db.select(["id", "title"], "types")
        status = db.select(["id", "title"], "status")
        return render_template("new.html", types=types, status=status)
    elif request.method == 'POST':
        data = request.form.get("data")
        login_users = request.form.get("login_users")
        type_id = request.form.get("type_id")
        status_id = request.form.get("status_id")
        message = request.form.get("message")
        if data and login_users and type_id and status_id and message:
            cursor = db.db.cursor(named_tuple=True)
            try:
                cursor.execute(
                    "INSERT INTO `lists` (`data`, `login_users`, `type_id`,`status_id`, `message`) VALUES ( '%s', '%s', '%s','%s','%s')" % (
                        data, login_users, type_id, status_id, message))
                cursor.close()
                return redirect("/list")
            except Exception:
                types = db.select(["id", "title"], "types")
                status = db.select(["id", "title"], "status")
                return render_template("new.html", login=flask_login.current_user.login, insert_false=True, types=types,
                                       status=status)
        else:
            types = db.select(["id", "title"], "types")
            status = db.select(["id", "title"], "status")
            return render_template("new.html", login=flask_login.current_user.login, insert_false=True, types=types,
                                   status=status)


if __name__ == '__main__':
    app.run()
