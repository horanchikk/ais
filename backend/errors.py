# -*- coding: utf-8 -*-
from enum import Enum
from fastapi.responses import JSONResponse
from fastapi import status


def gen_error(
        message: str,
        code: int
) -> JSONResponse:
    return JSONResponse(
        content={
            'detail': {
                'message': message,
                'code': code
            }
        }, status_code=status.HTTP_400_BAD_REQUEST
    )


class Error:
    INVALID_PASS_LOGIN = gen_error('Неправильный логин или пароль', 1)
    USER_IS_NOT_EXISTS = gen_error('Пользователь не существует', 2)
    LOGIN_IS_EXISTS = gen_error('Этот логин уже занят', 3)
    NO_ACCESS = gen_error('Нет доступа на выполнение запроса', 4)
