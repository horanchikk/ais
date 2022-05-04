# -*- coding: utf-8 -*-
from typing import List, Any
from enum import Enum


class Film:
    """Предоставляет удобный интерфейс
    для работы с таблицей фильмов
    """
    table: str = 'film'

    class Column(Enum):
        """Названия колонок в таблице"""
        ID = 'id'
        NAME = 'name'
        DATE = 'film_date'
        TIME = 'film_time'
        PRICE = 'price'
        DESCRIPTION = 'description'
        PLACES = 'places'
        IMAGE = 'image'
        GENRES = 'genres'

    def __init__(
            self,
            args: List[Any]
    ):
        self.film_id: int = args[0]
        self.name: str = args[1]
        self.date: str = args[2]
        self.time: str = args[3]
        self.price: float = args[4]
        self.description: str = args[5]
        self.places: int = args[6]
        self.image: str = args[7]
        self.genres: str = args[8]
    
    def __str__(self) -> str:
        """Преобразует объект пользователя в строку"""
        return f'[{self.film_id}] {self.name}, {self.role}, {self.places} places'
    
    def json(self):
        """Преобразует объект пользователя в JSON, скрывая при этом пароль"""
        return {
            'id': self.user_id,
            'name': self.name,
            'date': self.date,
            'title': self.title,
            'description': self.description,
            'places': self.places,
            'price': self.price,
            'image': self.image,
            'genres': self.genres
        }
