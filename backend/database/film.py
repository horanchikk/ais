# -*- coding: utf-8 -*-
from enum import Enum
from typing import Dict, Any


class Film:
    """Предоставляет удобный интерфейс
    для работы с таблицей фильмов"""

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
            *args: Any
    ):
        self.film_id: int = args[0]
        self.name: str = args[1]
        self.date: str = args[2]
        self.time: str = args[3]
        self.price: float = args[4]
        self.description: str = args[5]
        self.places: int = args[6]
        self.image: str = args[7]
        self.genres: str = args[8].split()

    def __str__(self) -> str:
        """Преобразует объект пользователя в строку"""
        return f'[{self.film_id}] {self.name} {self.places} places'

    def json(self) -> Dict[str, Any]:
        """Переводит объект в JSON"""
        return {
            'id': self.film_id,
            'name': self.name,
            'description': self.description,
            'date': self.date,
            'time': self.time,
            'price': self.price,
            'places': self.places,
            'image': self.image,
            'genres': self.genres
        }
