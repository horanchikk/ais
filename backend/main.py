# -*- coding: utf-8 -*-
from fastapi import FastAPI

from database import Database, User
from errors import Error
from config import ADMIN_TOKEN


db = Database('test.db')
app = FastAPI()
SUCCESS = {'response': 'success'}


@app.get('/users/login')
async def users_get(
        login: str,
        password: str
):
    user = db.get_user_by(User.Column.LOGIN, login)
    if not user:
        return Error.INVALID_PASS_LOGIN
    if user.password != password:
        return Error.INVALID_PASS_LOGIN
    return user.json()


@app.get('/users/get')
async def users_get(
        user_id: int
):
    user = db.get_user(user_id)
    if not user:
        return Error.USER_IS_NOT_EXISTS
    return user.json()


@app.get('/users/register')
async def asd(
        login: str,
        password: str,
        role: str = User.Role.CLIENT.value,
        discount: int = 0.0,
        access_key: str = ''
):
    """Регистрирует нового пользователя

    :param login: Логин для регистрации
    :param password: Пароль для регистрации
    :param role: Роль регистрируемого пользователя
    :param discount: Скидка регистрируемого пользователя
    :param access_key: Ключ доступа (для параметров роли и скидки"""
    user = db.get_user_by(User.Column.LOGIN, login)
    if user:
        return Error.LOGIN_IS_EXISTS
    if access_key != ADMIN_TOKEN and (role != User.Role.CLIENT.value or discount != 0.0):
        return Error.NO_ACCESS
    user = db.add_user(
        login, password, role, discount
    )
    return {'response': user.json()}
