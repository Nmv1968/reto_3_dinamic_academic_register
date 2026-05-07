from __future__ import annotations

from .grupo import Grupo


class NodoCircular:
    def __init__(self, valor: Grupo):
        self.valor: Grupo = valor
        self.siguiente: NodoCircular | None = None