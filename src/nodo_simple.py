from __future__ import annotations


class NodoSimple:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente: NodoSimple | None = None