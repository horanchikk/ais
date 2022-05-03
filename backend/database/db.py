# -*- coding: utf-8 -*-
"""Предоставляет класс Database для работы с базой данных"""
from typing import List, Any
from sqlite3 import connect

from .user import User


class Database:
    """Предоставляет работу с пользователями"""
    def __init__(
            self,
            filename: str = 'database.db'
    ):
        self.connection = connect(filename)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            f'''create table if not exists {User.table} (
                {User.Column.ID.value} integer primary key,
                {User.Column.ROLE.value} text not null,
                {User.Column.LOGIN.value} text not null,
                {User.Column.PASSWORD.value} text not null,
                {User.Column.DISCOUNT.value} real not null
            )'''
        )
        self.connection.commit()
    
    def add_user(
            self,
            login: str,
            password: str,
            role: User.Role = User.Role.CLIENT,
            discount: float = 0.0
    ) -> User:
        self.cursor.execute(
            f'''insert into {User.table} (
                {User.Column.LOGIN.value},
                {User.Column.PASSWORD.value},
                {User.Column.ROLE.value},
                {User.Column.DISCOUNT.value}
            ) values (?, ?, ?, ?)''',
            (login, password, role.value, discount)
        )
        self.connection.commit()
        return self.get_user(self.cursor.lastrowid)
    
    def get_user(
            self,
            user_id: int
    ) -> User:
        return User(self.cursor.execute(
            f'select * from {User.table} where {User.Column.ID.value} = ?', (user_id,)
        ).fetchone())
    
    def get_all_users(
            self,
            limit: int = 0
    ) -> List[User]:
        limit_str = f'limit {limit}' if limit > 0 else ''
        result = self.cursor.execute(
            f'select * from {User.table} {limit_str}'
        ).fetchall()
        return [User(row) for row in result]
    
    def get_user_by(
            self,
            column: User.Column,
            value: Any
    ) -> User:
        return User(self.cursor.execute(
            f'select * from {User.table} where {column.value} = ?', (value,)
        ).fetchone())
    
    def save_user(
            self,
            user: User
    ):
        """Сохранение пользователя в таблице
        
        :param user: объект пользователя"""
        self.cursor.execute(
            f'''update {User.table} set
                {User.Column.LOGIN.value} = ?,
                {User.Column.PASSWORD.value} = ?,
                {User.Column.DISCOUNT.value} = ?,
                {User.Column.ROLE.value} = ?
                where {User.Column.ID.value} = ?''',
            (user.login, user.password, user.discount, user.role.value, user.user_id)
        )
        self.connection.commit()
