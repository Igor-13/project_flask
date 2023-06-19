# Задание
#
# Объедините студентов в команды по 2-5 человек в сессионных залах.
#
# Необходимо создать базу данных для интернет-магазина. База данных должна состоять из трёх таблиц: товары,
# заказы и пользователи. — Таблица «Товары» должна содержать информацию о доступных товарах, их описаниях и ценах. —
# Таблица «Заказы» должна содержать информацию о заказах, сделанных пользователями. — Таблица «Пользователи» должна
# содержать информацию о зарегистрированных пользователях магазина. • Таблица пользователей должна содержать
# следующие поля: id (PRIMARY KEY), имя, фамилия, адрес электронной почты и пароль. • Таблица заказов должна
# содержать следующие поля: id (PRIMARY KEY), id пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и
# статус заказа. • Таблица товаров должна содержать следующие поля: id (PRIMARY KEY), название, описание и цена.
#
# Создайте модели pydantic для получения новых данных и возврата существующих в БД для каждой из трёх таблиц.
# Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API.


import datetime
from fastapi import FastAPI
import database as db
import models
from typing import List
from random import randint

app = FastAPI()


@app.get("/")
def root():
    return {"Message": "Hello"}


''' Добавляем информацию о пользователях, продуктах и заказах '''


@app.get("/fake_products/{count}")
async def create_note(count: int):
    for i in range(count):
        query = db.products.insert().values(title=f'product {i}', description=f'all about product {i}',
                                            price=randint(1, 100))
        await db.database.execute(query)
    return {'message': f'создано продуктов: {count}!'}


@app.get("/fake_orders/{count}")
async def create_note(count: int):
    for i in range(count):
        query = db.orders.insert().values(user_id=randint(1, 10), prod_id=randint(1, 10), status="created",
                                          date=datetime.datetime.now())
        await db.database.execute(query)
    return {'message': f'создано заказов: {count}!'}


@app.get("/fake_users/{count}")
async def create_note(count: int):
    for i in range(count):
        query = db.users.insert().values(name=f'user{i}', surname=f'surname{i}', email=f'mail{i}@mail.ru',
                                         password=f'qwerty{i}')
        await db.database.execute(query)
    return {'message': f'создано пользователей:{count}!'}


''' Получаем информацию о пользователях, продуктах и заказах '''


@app.get("/products/", response_model=List[models.ProductRead])
async def read_products():
    query = db.products.select()
    return await db.database.fetch_all(query)


@app.get("/orders/", response_model=List[models.OrderRead])
async def read_orders():
    query = db.orders.select()
    return await db.database.fetch_all(query)


@app.get("/users/", response_model=List[models.UserRead])
async def read_users():
    query = db.users.select()
    return await db.database.fetch_all(query)


''' Обновляем информацию о пользователях, продуктах и заказах '''


@app.put("/products/{product_id}", response_model=models.ProductRead)
async def update_product(product_id: int, new_product: models.ProductCreate):
    query = db.products.update().where(db.products.c.id == product_id).values(**new_product.dict())
    await db.database.execute(query)
    return {**new_product.dict(), "id": product_id}


@app.put("/orders/{order_id}", response_model=models.OrderRead)
async def update_order(order_id: int, new_order: models.OrderCreate):
    query = db.orders.update().where(db.orders.c.id == order_id).values(**new_order.dict())
    await db.database.execute(query)
    return {**new_order.dict(), "id": order_id}


@app.put("/users/{user_id}", response_model=models.UserRead)
async def update_user(user_id: int, new_user: models.UserCreate):
    query = db.users.update().where(db.users.c.id == user_id).values(**new_user.dict())
    await db.database.execute(query)
    return {**new_user.dict(), "id": user_id}


''' Удаляем информацию о пользователях, продуктах и заказах '''


@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    query = db.products.delete().where(db.products.c.id == product_id)
    await db.database.execute(query)
    return {'message': 'Продукт удалён!'}


@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = db.orders.delete().where(db.orders.c.id == order_id)
    await db.database.execute(query)
    return {'message': 'Заказ удалён!'}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = db.users.delete().where(db.users.c.id == user_id)
    await db.database.execute(query)
    return {'message': 'Пользователь удалён!'}
