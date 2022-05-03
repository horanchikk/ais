# -*- coding: utf-8 -*-
from fastapi import FastAPI

from database import Database, User
from errors import Error


db = Database('test.db')
app = FastAPI()
SUCCESS = {'response': 'success'}


@app.get('/users/get')
async def users_get(login: str, password: str):
    user = db.get_user_by(User.Column.LOGIN, login)
    if not user:
        return Error.INVALID_PASS_LOGIN.value
    if user.password != password:
        return Error.INVALID_PASS_LOGIN.value
    
    return SUCCESS


@app.get('/users/new')
async def asd():
    pass
