from __future__ import annotations

from .semestre import Semestre


class NodoDoble:
    def __init__(self, valor: Semestre):
        self.valor: Semestre = valor
        self.anterior: NodoDoble | None = None
        self.siguiente: NodoDoble | None = None