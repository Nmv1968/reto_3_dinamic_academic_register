"""Lista simple para gestionar estudiantes inscritos.

Este módulo implementa las operaciones básicas de inserción, búsqueda,
eliminación, recorrido y persistencia para la estructura enlazada de
estudiantes inscritos.
"""

from .estudiante import Estudiante
from .nodo_simple import NodoSimple


class ListaSimple:
    """Representa una lista simplemente enlazada de estudiantes.

    Attributes:
        cabeza (NodoSimple | None): Primer nodo de la lista.
    """

    def __init__(self):
        """Inicializa una lista simple vacía."""

        self.cabeza: NodoSimple | None = None

    def esta_vacia(self) -> bool:
        """Indica si la lista no contiene elementos.

        Returns:
            bool: True si la lista está vacía.
        """

        return self.cabeza is None

    def insertar_final(self, dato: Estudiante) -> Estudiante:
        """Inserta un estudiante al final de la lista.

        Args:
            dato (Estudiante): Estudiante que se desea insertar.

        Returns:
            Estudiante: El mismo estudiante insertado.
        """

        nuevo = NodoSimple(dato)
        if self.cabeza is None:
            self.cabeza = nuevo
            return dato

        actual = self.cabeza
        while actual.siguiente is not None:
            actual = actual.siguiente
        actual.siguiente = nuevo
        return dato

    def buscar(self, identificador: str) -> Estudiante | None:
        """Busca un estudiante por su identificador interno.

        Args:
            identificador (str): ID del estudiante.

        Returns:
            Estudiante | None: Estudiante encontrado o None si no existe.
        """

        actual = self.cabeza
        while actual is not None:
            valor = actual.valor
            if valor.id_estudiante == str(identificador):
                return valor
            actual = actual.siguiente
        return None

    def buscar_por_ci(self, ci_estudiante: str) -> Estudiante | None:
        """Busca un estudiante por su cédula.

        Args:
            ci_estudiante (str): Cédula del estudiante.

        Returns:
            Estudiante | None: Estudiante encontrado o None si no existe.
        """

        actual = self.cabeza
        while actual is not None:
            valor = actual.valor
            if valor.ci_estudiante == str(ci_estudiante):
                return valor
            actual = actual.siguiente
        return None

    def eliminar(self, identificador: str) -> Estudiante | None:
        """Elimina un estudiante según su identificador interno.

        Args:
            identificador (str): ID del estudiante a eliminar.

        Returns:
            Estudiante | None: Estudiante eliminado o None si no existe.
        """

        actual = self.cabeza
        anterior: NodoSimple | None = None

        while actual is not None:
            valor = actual.valor
            if valor.id_estudiante == str(identificador):
                if anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                return valor
            anterior = actual
            actual = actual.siguiente
        return None

    def recorrer(self) -> list[Estudiante]:
        """Recorre la lista y devuelve sus estudiantes.

        Returns:
            list[Estudiante]: Estudiantes almacenados en orden de inserción.
        """

        actual = self.cabeza
        recorrido: list[Estudiante] = []
        while actual is not None:
            recorrido.append(actual.valor)
            actual = actual.siguiente
        return recorrido

    def contar(self) -> int:
        """Cuenta la cantidad de estudiantes presentes en la lista.

        Returns:
            int: Número total de estudiantes inscritos.
        """

        total = 0
        actual = self.cabeza
        while actual is not None:
            total += 1
            actual = actual.siguiente
        return total

    def limpiar(self):
        """Elimina todas las referencias de la lista."""

        self.cabeza = None

    def exportar_csv(self, ruta):
        """Exporta la lista actual de inscritos a un archivo CSV.

        Args:
            ruta (str): Ruta del archivo de salida.
        """

        from .persistencia_csv import exportar_inscritos_csv

        exportar_inscritos_csv(self, ruta)

    def importar_csv(self, ruta):
        """Importa estudiantes desde un archivo CSV.

        Args:
            ruta (str): Ruta del archivo de entrada.
        """

        from .persistencia_csv import importar_inscritos_csv

        importar_inscritos_csv(ruta, self)