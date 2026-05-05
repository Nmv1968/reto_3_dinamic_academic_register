from __future__ import annotations


class NodoCircular:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente: NodoCircular | None = None