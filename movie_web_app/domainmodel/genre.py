from datetime import date, datetime
from typing import List, Iterable
import pytest

class Genre:
    def __init__(
            self, genre_name: str,
    ):
        self._genre_name: str = genre_name

    @property
    def genre_name(self) -> str:
        return self._genre_name

    def __repr__(self):
        if not self._genre_name:
            return f'<Genre None>'
        else:
            return f'<Genre {self._genre_name}>'

    def __eq__(self, other):
        if not isinstance(other, Genre):
            return False
        return (
                other._genre_name == self._genre_name
        )

    def __lt__(self, other):
        return self._genre_name < other._genre_name

    def __hash__(self):
        return hash(self._genre_name)
