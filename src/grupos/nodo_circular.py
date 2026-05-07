"""Nodo circular para almacenar grupos de exposición.

Este módulo define el nodo utilizado por la lista circular del paquete de
grupos.
"""

from __future__ import annotations

from .grupo import Grupo


class NodoCircular:
    """Representa un nodo de una lista circular.

    Attributes:
        valor (Grupo): Grupo almacenado en el nodo.
        siguiente (NodoCircular | None): Referencia al siguiente nodo.
    """

    def __init__(self, valor: Grupo):
        """Inicializa un nodo con un grupo.

        Args:
            valor (Grupo): Grupo que se almacenará en el nodo.
        """

        self.valor: Grupo = valor
        self.siguiente: NodoCircular | None = None