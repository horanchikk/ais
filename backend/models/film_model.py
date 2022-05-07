# -*- coding: utf-8 -*-
from typing import List

from pydantic import BaseModel


class FilmEditModel(BaseModel):
    name: str
    description: str = ''
    price: float = 200.0
    image: str = ''
    genres: List[str] = []
    time: str = '00:00'
    date: str = '01.01.0001'
    places: int = 100
    access_key: str = ''
