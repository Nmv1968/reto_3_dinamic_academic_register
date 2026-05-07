from __future__ import annotations

from .estudiante import Estudiante


class NodoSimple:
    def __init__(self, valor: Estudiante):
        self.valor: Estudiante = valor
        self.siguiente: NodoSimple | None = None