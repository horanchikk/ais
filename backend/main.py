# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Database, User
from models import RegisterModel, LoginModel, FilmEditModel
from errors import Error
from config import ADMIN_TOKEN


db = Database('test.db')
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
users_router = FastAPI()
films_router = FastAPI()
app.mount('/users', users_router)
app.mount('/films', films_router)
SUCCESS = {'response': 'success'}


@users_router.post('/login')
async def users_get(
        model: LoginModel
):
    """Проверяет правильность логина и пароля

    :param model: Модель авторизации"""
    user = db.get_user_by(User.Column.LOGIN, model.login)
    if not user:
        return Error.INVALID_PASS_LOGIN
    if user.password != model.password:
        return Error.INVALID_PASS_LOGIN
    return {'response': user.json()}


@users_router.get('/get')
async def users_get(
        user_id: int
):
    """Возвращает объект пользователя по его ID"""
    user = db.get_user(user_id)
    if not user:
        return Error.USER_NOT_EXISTS
    return {'response': user.json()}


@users_router.get('/getall')
async def users_get(limit: int = 0):
    """Возвращает список всех пользователей"""
    users = db.get_all_users(limit)
    return {'response': [user.json() for user in users]}


@users_router.post('/reg')
async def asd(
        model: RegisterModel
):
    """Регистрирует нового пользователя

    :param model: Модель регистрации"""
    user = db.get_user_by(User.Column.LOGIN, model.login)
    if user:
        return Error.LOGIN_IS_EXISTS
    if model.access_key != ADMIN_TOKEN and (model.role != User.Role.CLIENT.value or model.discount != 0.0):
        return Error.NO_ACCESS
    user = db.add_user(
        model.login, model.password, model.role, model.discount
    )
    return {'response': user.json()}


# ---=== Films ===--- #


@films_router.get('/get')
async def films_get(
        film_id: int
):
    """Возвращает фильм по его ID."""
    film = db.get_film(film_id)
    if not film:
        return Error.FILM_NOT_EXISTS
    return {'response': film.json()}


@films_router.get('/buy')
async def film_buy(
        film_id: int,
        user_id: int,
        date: str
):
    """Покупает билет на фильм, если есть свободное место"""
    print(date)
    return {'detail': {
        'message': 'Вадим лох(',
        'code': '1448'
    }}
    film = db.get_film(film_id)
    if not film:
        return Error.FILM_NOT_EXISTS
    user = db.get_user(user_id)
    if not user:
        return Error.USER_NOT_EXISTS
    if film.places > 0:
        film.places -= 1
        user.tickets.append(film_id)
        db.save_film(film)
        db.save_user(film)
        return {'response': {
            'user_id': user_id,
            'film_id': film_id
        }}
    return Error.FILM_HASNOT_PLACES


@films_router.get('/getall')
async def films_get_all(
        limit: int = 0
):
    """Возвращает список всех фильмов
    
    :param limit: Количество возвращаемых пользователей"""
    films = db.get_all_films(limit)
    return {'response': [film.json() for film in films]}


@films_router.post('/new')
async def films_new(
        model: FilmEditModel
):
    """Создает новый фильм

    :param model: модель фильма"""
    if model.access_key != ADMIN_TOKEN:
        return Error.NO_ACCESS
    film = db.add_film(
        model.name, model.description, model.date,
        model.time, model.price, model.places, model.image,
        model.genres
    )
    return {'response': film.json()}
