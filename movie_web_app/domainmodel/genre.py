from datetime import date, datetime
from typing import List, Iterable
import pytest

class Genre:
    pass

    def __init__(
            self, gname: str,
    ):
        self._gname: str = gname

    @property
    def genre_name(self) -> str:
        return self._gname

    def __repr__(self):
        if not self._gname:
            return f'<Genre None>'
        else:
            return f'<Genre {self._gname}>'

    def __eq__(self, other):
        if not isinstance(other, Genre):
            return False
        return (
                other._gname == self._gname
        )

    def __lt__(self, other):
        return self._gname < other._gname

    def __hash__(self):
        return hash(self._gname)
