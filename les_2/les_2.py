# Урок 2. Погружение во Flask
# Задание
#
# Создать страницу, на которой будет форма для ввода имени и электронной почты, при отправке которой будет создан
# cookie-файл с данными пользователя, а также будет произведено перенаправление на страницу приветствия,
# где будет отображаться имя пользователя. На странице приветствия должна быть кнопка «Выйти», при нажатии на которую
# будет удалён cookie-файл с данными пользователя и произведено перенаправление на страницу ввода имени и электронной
# почты.

import secrets
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = secrets.token_hex()


@app.route("/")
@app.route("/index/")
def index():
    return render_template("index.html")


@app.route("/log/", methods=["GET", "POST"])
def log():
    if request.method == "POST":
        session["username"] = request.form.get("username")
        return redirect(url_for("index"))
    return render_template("log.html")


@app.route("/logout/")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
