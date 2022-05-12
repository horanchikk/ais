# -*- coding: utf-8 -*-
"""Предоставляет класс Database для работы с базой данных"""
from json import dumps
from typing import List, Any, Optional
from sqlite3 import connect

from .user import User
from .film import Film


class Database:
    """Предоставляет работу с пользователями"""
    user_table: str = 'user'
    film_table: str = 'film'

    def __init__(
            self,
            filename: str = 'database.db'
    ):
        self.connection = connect(filename)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            f'''create table if not exists {self.user_table} (
                {User.Column.ID.value} integer primary key,
                {User.Column.ROLE.value} text not null,
                {User.Column.LOGIN.value} text not null,
                {User.Column.PASSWORD.value} text not null,
                {User.Column.DISCOUNT.value} real not null,
                {User.Column.TICKETS.value} text not null
            )'''
        )
        self.cursor.execute(
            f'''create table if not exists {self.film_table} (
                {Film.Column.ID.value} integer primary key,
                {Film.Column.NAME.value} text not null,
                {Film.Column.DATE.value} text not null,
                {Film.Column.TIME.value} text not null,
                {Film.Column.PRICE.value} real not null,
                {Film.Column.DESCRIPTION.value} text not null,
                {Film.Column.PLACES.value} integer not null,
                {Film.Column.IMAGE.value} text not null,
                {Film.Column.GENRES.value} text not null
            )'''
        )
        self.connection.commit()
    
    def add_film(
            self,
            name: str,
            description: str,
            date: str,
            time: str,
            price: float,
            places: int,
            image: str,
            genres: List[str]
    ) -> Optional[Film]:
        """Создает объект фильма
        
        :param name: название фильма
        :param description: описание фильма
        :param date: дата премьеры
        :param time: время премьеры
        :param price: цена билета
        :param places: количество свободных мест
        :param image: URL постера фильма
        :param genres: жанры фильма через запятую"""
        self.cursor.execute(
            f'''insert into {self.film_table} (
                {Film.Column.NAME.value},
                {Film.Column.DESCRIPTION.value},
                {Film.Column.DATE.value},
                {Film.Column.TIME.value},
                {Film.Column.PRICE.value},
                {Film.Column.PLACES.value},
                {Film.Column.IMAGE.value},
                {Film.Column.GENRES.value}
            ) values (?, ?, ?, ?, ?, ?, ?, ?)''',
            (name, description, date, time, price, places, image, ' '.join(genres))
        )
        self.connection.commit()
        return self.get_film(self.cursor.lastrowid)
    
    def add_user(
            self,
            login: str,
            password: str,
            role: str = User.Role.CLIENT.value,
            discount: float = 0.0
    ) -> Optional[User]:
        if not User.Role.has(role):
            return None
        self.cursor.execute(
            f'''insert into {self.user_table} (
                {User.Column.LOGIN.value},
                {User.Column.PASSWORD.value},
                {User.Column.ROLE.value},
                {User.Column.DISCOUNT.value},
                {User.Column.TICKETS.value}
            ) values (?, ?, ?, ?, ?)''',
            (login, password, role, discount, '[]')
        )
        self.connection.commit()
        return self.get_user(self.cursor.lastrowid)
    
    def get_film(
            self,
            film_id: int
    ) -> Optional[Film]:
        result = self.cursor.execute(
            f'select * from {self.film_table} where {Film.Column.ID.value} = ?', (film_id,)
        ).fetchone()
        if result:
            return Film(*result)
        return None
    
    def get_user(
            self,
            user_id: int
    ) -> Optional[User]:
        result = self.cursor.execute(
            f'select * from {self.user_table} where {User.Column.ID.value} = ?', (user_id,)
        ).fetchone()
        if result:
            return User(*result)
        return None
    
    def get_all_films(
            self,
            limit: int = 0
    ) -> List[Film]:
        limit_str = f'limit {limit}' if limit > 0 else ''
        result = self.cursor.execute(
            f'select * from {self.film_table} {limit_str}'
        ).fetchall()
        return [Film(*row) for row in result]
    
    def get_all_users(
            self,
            limit: int = 0
    ) -> List[User]:
        limit_str = f'limit {limit}' if limit > 0 else ''
        result = self.cursor.execute(
            f'select * from {self.user_table} {limit_str}'
        ).fetchall()
        return [User(*row) for row in result]
    
    def get_user_by(
            self,
            column: User.Column,
            value: Any
    ) -> Optional[User]:
        result = self.cursor.execute(
            f'select * from {self.user_table} where {column.value} = ?', (value,)
        ).fetchone()
        if result:
            return User(*result)
        return None
    
    def save_film(
            self,
            film: Film
    ):
        """Сохранение фильма в таблице
        
        :param film: объект фильма"""
        self.cursor.execute(
            f'''update {self.film_table} set
                {Film.Column.NAME.value} = ?,
                {Film.Column.DESCRIPTION.value} = ?,
                {Film.Column.PLACES.value} = ?,
                {Film.Column.PRICE.value} = ?,
                {Film.Column.IMAGE.value} = ?,
                {Film.Column.GENRES.value} = ?,
                {Film.Column.DATE.value} = ?,
                {Film.Column.TIME.value} = ?
                where {Film.Column.ID.value} = ?''',
            (
                film.name, film.description, film.places, film.price,
                film.image, ' '.join(film.genres), film.date, film.time, film.film_id
            )
        )
        self.connection.commit()

    def save_user(
            self,
            user: User
    ):
        """Сохранение пользователя в таблице

        :param user: объект пользователя"""
        self.cursor.execute(
            f'''update {self.user_table} set
                {User.Column.LOGIN.value} = ?,
                {User.Column.PASSWORD.value} = ?,
                {User.Column.DISCOUNT.value} = ?,
                {User.Column.ROLE.value} = ?,
                {User.Column.TICKETS.value} = ?
                where {User.Column.ID.value} = ?''',
            (
                user.login, user.password, user.discount,
                user.role.value, dumps(user.tickets), user.user_id
            )
        )
        self.connection.commit()
