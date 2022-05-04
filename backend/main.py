# -*- coding: utf-8 -*-
from fastapi import FastAPI

from database import Database, User
from errors import Error
from config import ADMIN_TOKEN


db = Database('test.db')
app = FastAPI()
users_router = FastAPI()
films_router = FastAPI()
app.mount('/users', users_router)
app.mount('/films', films_router)
SUCCESS = {'response': 'success'}


@users_router.get('/login')
async def users_get(
        login: str,
        password: str
):
    """Проверяет правильность логина и пароля"""
    user = db.get_user_by(User.Column.LOGIN, login)
    if not user:
        return Error.INVALID_PASS_LOGIN
    if user.password != password:
        return Error.INVALID_PASS_LOGIN
    return {'response': user.json()}


@users_router.get('/get')
async def users_get(
        user_id: int
):
    """Возвращает объект пользователя по его ID"""
    user = db.get_user(user_id)
    if not user:
        return Error.USER_IS_NOT_EXISTS
    return {'response': user.json()}


@users_router.get('/getall')
async def users_get(limit: int = 0):
    """Возвращает список всех пользователей"""
    users = db.get_all_users(limit)
    return {'response': [user.json() for user in users]}


@users_router.get('/register')
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


# ---=== Films ===--- #


@films_router.get('/get')
async def films_get_all(
        film_id: int
):
    """Возвращает фильм по его ID."""


@films_router.get('/getall')
async def films_get_all(
        limit: int = 0
):
    """Возвращает список всех фильмов
    
    :param limit: Количество возвращаемых пользователей"""
    films = db.get_all_films(limit)
    return {'response': [film.json() for film in films]}
