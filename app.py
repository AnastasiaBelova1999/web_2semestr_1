import json

import mysql
from flask import Flask, render_template, request, abort, redirect, flash, url_for
from flask_login import login_required
from collections import namedtuple

from mysql_db import MySQL
import mysql.connector
import flask_login
import hashlib

app = Flask(__name__)
app.secret_key = 'asjdfbajSLDFBhjasbfd'
app.config.from_pyfile('config.py')
db = MySQL(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    pass

#Ищем_в_бд_чтобы_логин_и_пароль_совпадали_правильно
@login_manager.user_loader
def user_loader(login):
    cursor = db.db.cursor(named_tuple=True)
    cursor.execute('select id, login, name from users where id = %s', (login,))
    user_db = cursor.fetchone()
    if user_db:
        user = User()
        user.id = user_db.id
        user.login = user_db.login
        user.name = user_db.name
        return user
    return None


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template("index.html", authorization=False, login="anonimus", login_false=False)

#[get]-получить_у_сервева,_[post] - отдать_серверу
#формочка, где вход пользователя
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
                    "SELECT id,name,login FROM users WHERE `login` = '%s' and `password_hash` = '%s'" % (
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
                flask_user.name = user.name
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


@app.route('/main', methods=['POST', 'GET'])
def main():
    user = flask_login.current_user
    if not user.is_anonymous:
        return user.name
    else:
        return "Залогинтесь"


@app.route('/logout', methods=['GET'])
def logout():
    flask_login.logout_user()
    return render_template("index.html", authorization=not flask_login.current_user.is_anonymous, login="anonimus",
                           login_false=False)


@app.route('/town', methods=['GET'])
@login_required
def town():
    towns = db.select(None, "towns")
    login = flask_login.current_user.login
    return render_template("town.html", towns=towns, login=login)


@app.route('/tariff', methods=['GET'])
@login_required
def tariff():
    tariffs = db.select(None, "tariffs")
    login = flask_login.current_user.login
    return render_template("tariff.html", tariffs=tariffs, login=login)


@app.route('/tariff/new', methods=['GET', 'POST'])
@login_required
def tariff_new():
    if request.method == 'GET':
        return render_template("tarrif_new.html", login=flask_login.current_user.login)
    elif request.method == 'POST':
        id = request.form.get("id")
        title = request.form.get("title")
        price = request.form.get("price")
        description = request.form.get("description")
        review = request.form.get("review")
        if id and title and price and description:
            cursor = db.db.cursor(named_tuple=True)
            try:
                cursor.execute(
                    "INSERT INTO `tariffs` (`id`, `title`, `price`, `description`, `review`) VALUES ('%s', '%s', '%s', '%s','%s')" % (
                        id, title, price, description, review))
                db.db.commit()
                cursor.close()
                return redirect("/tariff")
            except Exception:
                return render_template("tarrif_new.html", login=flask_login.current_user.login, insert_false=True)


@app.route('/tariff/edit', methods=['POST'])
@login_required
def tariff_edit():
    try:
        tariff_id = request.form.get("tariff_id")
        title = request.form.get("title")
        price = request.form.get("price")
        description = request.form.get("description")
        review = request.form.get("review")
        tariff = {
            'id': tariff_id,
            'title': title,
            'price': price,
            'description': description,
            'review': review
        }
        return render_template("tariff_edit.html", tariff=tariff)
    except Exception:
        return redirect("/tariff")


@app.route('/tariff/edit/submit', methods=['POST'])
@login_required
def tariff_edit_submit():
    older_id = request.form.get("older_id")
    id = request.form.get("id")
    title = request.form.get("title")
    price = request.form.get("price")
    description = request.form.get("description")
    review = request.form.get("review")
    if id and title and price and description:
        cursor = db.db.cursor(named_tuple=True)
        try:
            cursor.execute(
                "UPDATE `tariffs` SET `id` = '%s', `title` = '%s', `price` = '%s', `description` = '%s', `review` = '%s' WHERE `tariffs`.`id` = %s" % (
                    id, title, price, description, review, older_id))
            db.db.commit()
            cursor.close()
            return redirect("/tariff")
        except Exception:
            return render_template("tarrif_new.html", login=flask_login.current_user.login, insert_false=True)


@app.route('/sub', methods=['GET'])
@login_required
def sub():
    subs = db.select(None, "subscribers")
    towns = dict(db.select(None, "towns"))
    tariffs = dict(db.select(["id", "title"], "tariffs"))

    view_subs = []
    for sub in subs:
        view_subs.append({"id": sub.id,
                          "full_name": sub.full_name,
                          "town": towns[sub.town_id],
                          "tariff": tariffs[sub.tariff_id],
                          "town_id": sub.town_id,
                          "tariff_id": sub.tariff_id
                          })
    return render_template("sub.html", login=flask_login.current_user.login, subs=view_subs)


@app.route('/sub/delete', methods=['POST'])
@login_required
def sub_delete():
    id = request.form.get("id")
    cursor = db.db.cursor()
    cursor.execute("DELETE FROM `subscribers` WHERE `subscribers`.`id` = '%s'" % id)
    cursor.close()
    return redirect("/sub")


@app.route('/sub/new', methods=['POST', 'GET'])
@login_required
def sub_new():
    if request.method == 'GET':
        towns = db.select(["id", "title"], "towns")
        tariffs = db.select(["id", "title"], "tariffs")
        return render_template("sub_new.html", towns=towns, tariffs=tariffs)
    elif request.method == 'POST':
        id = request.form.get("id")
        full_name = request.form.get("full_name")
        town_id = request.form.get("town")
        tariff_id = request.form.get("tariff")
        if id and full_name and town_id and tariff_id:
            cursor = db.db.cursor(named_tuple=True)
            try:
                cursor.execute(
                    "INSERT INTO `subscribers` (`id`, `full_name`, `town_id`, `tariff_id`) VALUES ('%s', '%s', '%s', '%s')" % (
                        id, full_name, town_id, tariff_id))
                db.db.commit()
                cursor.close()
                return redirect("/sub")
            except Exception:
                return render_template("sub_new.html", login=flask_login.current_user.login, insert_false=True)
        else:
            return render_template("sub_new.html", login=flask_login.current_user.login, insert_false=True)


@app.route('/sub/edit', methods=['POST'])
@login_required
def sub_edit():
    try:
        sub_id = request.form.get("id")
        full_name = request.form.get("full_name")
        town_id = request.form.get("town_id")
        tariff_id = request.form.get("tariff_id")
        towns = db.select(["id", "title"], "towns")
        tariffs = db.select(["id", "title"], "tariffs")
        sub = {
            'id': sub_id,
            'full_name': full_name,
            'town_id': town_id,
            'tariff_id': tariff_id
        }
        return render_template("sub_edit.html", sub=sub, towns=towns, tariffs=tariffs,
                               login=flask_login.current_user.login)
    except Exception:
        return redirect("/sub")

@app.route('/sub/edit/submit', methods=['POST'])
@login_required
def sub_edit_submit():
    older_id = request.form.get("older_id")
    sub_id = request.form.get("id")
    full_name = request.form.get("full_name")
    town_id = request.form.get("town_id")
    tariff_id = request.form.get("tariff_id")
    if sub_id and full_name and town_id and tariff_id:
        cursor = db.db.cursor(named_tuple=True)
        try:
            cursor.execute(
                "UPDATE `subscribers` SET `id` = '%s', `full_name` = '%s', `town_id` = '%s', `tariff_id` = '%s' WHERE `subscribers`.`id` = %s" % (
                    sub_id, full_name, town_id, tariff_id, older_id))
            db.db.commit()
            cursor.close()
            return redirect("/sub")
        except Exception:
            return redirect("/sub")
    else:
        return redirect("/sub")



if __name__ == '__main__':
    app.run()
