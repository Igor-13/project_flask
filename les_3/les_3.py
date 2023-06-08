from flask import Flask, render_template, request, flash, redirect, url_for
from models import db, Books, Authors, User
from random import choice
from form import RegistrationForm
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SECRET_KEY'] = 'mysecretkey'
csrf = CSRFProtect(app)
db.init_app(app)

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')

@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')

# Задание №2
# Создать базу данных для хранения информации о книгах в библиотеке.
# База данных должна содержать две таблицы: "Книги" и "Авторы".
# В таблице "Книги" должны быть следующие поля: id, название, год издания,
# количество экземпляров и id автора.
# В таблице "Авторы" должны быть следующие поля: id, имя и фамилия.
# Необходимо создать связь между таблицами "Книги" и "Авторы".
# Написать функцию-обработчик, которая будет выводить список всех книг с
# указанием их авторов.


@app.cli.command("fill-books")
def fill_tables():
    count = 5
    # Добавляем авторов
    for author in range(1, count + 1):
        new_author = Authors(name=f'Author{author}', surname=f'Surname{author}')
        db.session.add(new_author)
    db.session.commit()
    # Добавляем книги
    for book in range(1, count ** 2):
        author = choice(range(1, 6))
        new_book = Books(name=f'Title{book}', year=choice(range(1990, 2010)), instances=choice(range(1, 1000)),
                        author=author)
        db.session.add(new_book)
    db.session.commit()

@app.route('/all_books/')
def get_all_books():
    books = Books.query.all()
    context = {'books': books}
    return render_template('all_books.html', **context)

# Задание №5
# Создать форму регистрации для пользователя.
# Форма должна содержать поля: имя, электронная почта,
# пароль (с подтверждением), дата рождения, согласие на
# обработку персональных данных.
# Валидация должна проверять, что все поля заполнены
# корректно (например, дата рождения должна быть в
# формате дд.мм.гггг).
# При успешной регистрации пользователь должен быть
# перенаправлен на страницу подтверждения регистрации.


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data.lower()
        email = form.email.data
        user = User(username=username, email=email)
        if User.query.filter(User.username == username).first() or User.query.filter(User.email == email).first():
            flash(f'Пользователь с username {username} или e-mail {email} уже существует')
            return redirect(url_for('registration'))
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Вы успешно зарегистрировались!')
        return redirect(url_for('registration'))
    return render_template('registration.html', form=form)



if __name__ == "__main__":
    app.run()