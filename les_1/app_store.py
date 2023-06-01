'''
1) Задача 8.
Создать базовый шаблон для всего сайта, содержащий общие элементы дизайна (шапка, меню, подвал), и дочерние шаблоны для каждой отдельной страницы.
Например, создать страницу "О нас" и "Контакты", используя базовый шаблон.

2) Задача 9
Создать базовый шаблон для интернет-магазина, содержащий общие элементы дизайна (шапка, меню, подвал), и дочерние шаблоны для страниц категорий товаров и отдельных товаров.
Например, создать страницы "Одежда", "Обувь" и "Куртка", используя базовый шаблон.
'''


from flask import Flask, render_template

app = Flask(__name__)

category = [
    {"title": "Одежда", "f_name": "cloth"},
    {"title": "Обувь", "f_name": "shoes"},
    {"title": "Куртка", "f_name": "jacket"}
]


@app.route("/")
def index():
    return render_template("base_shop.html", category=category)


@app.route("/info/")
def info():
    return render_template("info.html")


@app.route("/contacts/")
def contacts():
    return render_template("contacts.html")


@app.route("/cloth/")
def cloth():
    return render_template("cloth_shop.html")


@app.route("/shoes/")
def shoes():
    return render_template("shoes_shop.html")


@app.route("/jacket/")
def jacket():
    return render_template("jacket_snop.html")


if __name__ == "__main__":
    app.run()
