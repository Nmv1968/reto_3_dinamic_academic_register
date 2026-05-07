"""Nodo doble para almacenar semestres académicos.

Este módulo define el nodo utilizado por la lista doble del historial
académico.
"""

from __future__ import annotations

from .semestre import Semestre


class NodoDoble:
    """Representa un nodo de una lista doblemente enlazada.

    Attributes:
        valor (Semestre): Semestre almacenado en el nodo.
        anterior (NodoDoble | None): Referencia al nodo previo.
        siguiente (NodoDoble | None): Referencia al nodo siguiente.
    """

    def __init__(self, valor: Semestre):
        """Inicializa un nodo con un semestre.

        Args:
            valor (Semestre): Semestre que se almacenará en el nodo.
        """

        self.valor: Semestre = valor
        self.anterior: NodoDoble | None = None
        self.siguiente: NodoDoble | None = None