from __future__ import annotations


class NodoDoble:
    def __init__(self, valor):
        self.valor = valor
        self.anterior: NodoDoble | None = None
        self.siguiente: NodoDoble | None = None