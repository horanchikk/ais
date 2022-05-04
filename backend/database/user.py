# -*- coding: utf-8 -*-
from typing import List, Any
from enum import Enum


class User:
    """Предоставляет удобный интерфейс
    для работы с таблицей пользователей
    """
    table: str = 'user'

    class Column(Enum):
        """Названия колонок в таблице"""
        ID = 'id'
        ROLE = 'role'
        LOGIN = 'login'
        PASSWORD = 'password'
        DISCOUNT = 'discount'

    class Role(Enum):
        """Роли пользователей
        клиент и кассир соответственно"""
        CLIENT = 'client'
        CASHIER = 'cashier'

        @staticmethod
        def has(item):
            return item in [i.value for i in User.Role.__members__.values()]

    def __init__(
            self,
            args: List[Any]
    ):
        self.user_id: int = args[0]
        self.role = User.Role(args[1])
        self.login = args[2]
        self.password = args[3]
        self.discount = args[4]
    
    def __str__(self) -> str:
        """Преобразует объект пользователя в строку"""
        return f'[{self.user_id}] {self.login}, {self.role}'
    
    def json(self):
        """Преобразует объект пользователя в JSON, скрывая при этом пароль"""
        return {
            'id': self.user_id,
            'role': self.role.value,
            'login': self.login,
            'discount': self.discount
        }
