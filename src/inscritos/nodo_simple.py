"""Nodo simple para almacenar estudiantes inscritos.

Este módulo define el nodo utilizado por la lista simple del paquete de
inscritos.
"""

from __future__ import annotations

from .estudiante import Estudiante


class NodoSimple:
    """Representa un nodo de una lista simplemente enlazada.

    Attributes:
        valor (Estudiante): Estudiante almacenado en el nodo.
        siguiente (NodoSimple | None): Referencia al siguiente nodo.
    """

    def __init__(self, valor: Estudiante):
        """Inicializa un nodo con un estudiante.

        Args:
            valor (Estudiante): Estudiante que se almacenará en el nodo.
        """

        self.valor: Estudiante = valor
        self.siguiente: NodoSimple | None = None