# -*- coding: utf-8 -*-
from pydantic import BaseModel


class RegisterModel(BaseModel):
    login: str
    password: str
    role: str = 'client'
    access_key: str = ''
    discount: float = 0


class LoginModel(BaseModel):
    login: str
    password: str
