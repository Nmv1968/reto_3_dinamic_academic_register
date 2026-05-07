"""Lista doble para gestionar el historial académico.

Este módulo implementa la estructura doblemente enlazada utilizada para
almacenar semestres ordenados por año y término.
"""

from .nodo_doble import NodoDoble
from .semestre import Semestre


class ListaDoble:
    """Representa una lista doblemente enlazada de semestres.

    Attributes:
        cabeza (NodoDoble | None): Primer nodo de la lista.
        cola (NodoDoble | None): Último nodo de la lista.
    """

    def __init__(self):
        """Inicializa una lista doble vacía."""

        self.cabeza: NodoDoble | None = None
        self.cola: NodoDoble | None = None

    def esta_vacia(self) -> bool:
        """Indica si la lista no contiene semestres.

        Returns:
            bool: True si la lista está vacía.
        """

        return self.cabeza is None

    def insertar_ordenado(self, dato: Semestre) -> Semestre:
        """Inserta un semestre respetando el orden por año y término.

        Args:
            dato (Semestre): Semestre que se desea insertar.

        Returns:
            Semestre: El mismo semestre insertado.
        """

        nuevo = NodoDoble(dato)

        if self.cabeza is None:
            self.cabeza = nuevo
            self.cola = nuevo
            return dato

        actual: NodoDoble | None = self.cabeza
        while actual is not None and self._comparar(actual.valor, dato) <= 0:
            actual = actual.siguiente

        if actual == self.cabeza:
            nuevo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo
            self.cabeza = nuevo
            return dato

        if actual is None:
            nuevo.anterior = self.cola
            if self.cola is not None:
                self.cola.siguiente = nuevo
            self.cola = nuevo
            return dato

        anterior = actual.anterior
        nuevo.anterior = anterior
        nuevo.siguiente = actual
        if anterior is not None:
            anterior.siguiente = nuevo
        actual.anterior = nuevo
        return dato

    def buscar_por_estudiante(self, estudiante_id: str) -> list[Semestre]:
        """Obtiene todos los semestres asociados a un estudiante.

        Args:
            estudiante_id (str): ID del estudiante.

        Returns:
            list[Semestre]: Semestres encontrados para el estudiante.
        """

        actual = self.cabeza
        historial: list[Semestre] = []
        while actual is not None:
            if actual.valor.estudiante_id == str(estudiante_id):
                historial.append(actual.valor)
            actual = actual.siguiente
        return historial

    def buscar_semestre(self, estudiante_id: str, anio: int, term: int) -> Semestre | None:
        """Busca un semestre específico de un estudiante.

        Args:
            estudiante_id (str): ID del estudiante.
            anio (int): Año del semestre.
            term (int): Término del semestre.

        Returns:
            Semestre | None: Semestre encontrado o None si no existe.
        """

        actual = self.cabeza
        while actual is not None:
            valor = actual.valor
            if (
                valor.estudiante_id == str(estudiante_id)
                and valor.anio == anio
                and valor.term == term
            ):
                return valor
            actual = actual.siguiente
        return None

    def buscar(self, anio: int, term: int) -> Semestre | None:
        """Busca el primer semestre que coincida por año y término.

        Args:
            anio (int): Año del semestre.
            term (int): Término del semestre.

        Returns:
            Semestre | None: Semestre encontrado o None si no existe.
        """

        actual = self.cabeza
        while actual is not None:
            valor = actual.valor
            if valor.anio == anio and valor.term == term:
                return valor
            actual = actual.siguiente
        return None

    def existe_estudiante(self, estudiante_id: str) -> bool:
        """Verifica si existe historial para un estudiante.

        Args:
            estudiante_id (str): ID del estudiante.

        Returns:
            bool: True si el estudiante tiene al menos un semestre.
        """

        actual = self.cabeza
        while actual is not None:
            if actual.valor.estudiante_id == str(estudiante_id):
                return True
            actual = actual.siguiente
        return False

    def existe_anio(self, anio: int) -> bool:
        """Verifica si existe al menos un semestre en un año dado.

        Args:
            anio (int): Año a consultar.

        Returns:
            bool: True si existe un semestre registrado en ese año.
        """

        actual = self.cabeza
        while actual is not None:
            if actual.valor.anio == anio:
                return True
            actual = actual.siguiente
        return False

    def obtener_terminos_por_anio(self, anio: int) -> list[int]:
        """Obtiene los términos registrados para un año dado.

        Args:
            anio (int): Año a consultar.

        Returns:
            list[int]: Términos encontrados sin repetir.
        """

        actual = self.cabeza
        terminos: list[int] = []
        while actual is not None:
            if actual.valor.anio == anio and actual.valor.term not in terminos:
                terminos.append(actual.valor.term)
            actual = actual.siguiente
        return terminos

    def existe_anio_de_estudiante(self, estudiante_id: str, anio: int) -> bool:
        """Verifica si un estudiante tiene registros en un año específico.

        Args:
            estudiante_id (str): ID del estudiante.
            anio (int): Año a consultar.

        Returns:
            bool: True si existe al menos un semestre del estudiante en ese año.
        """

        actual = self.cabeza
        while actual is not None:
            if actual.valor.estudiante_id == str(estudiante_id) and actual.valor.anio == anio:
                return True
            actual = actual.siguiente
        return False

    def obtener_terminos_por_estudiante_y_anio(self, estudiante_id: str, anio: int) -> list[int]:
        """Obtiene los términos de un estudiante dentro de un año específico.

        Args:
            estudiante_id (str): ID del estudiante.
            anio (int): Año a consultar.

        Returns:
            list[int]: Términos encontrados para el estudiante en ese año.
        """

        actual = self.cabeza
        terminos: list[int] = []
        while actual is not None:
            if (
                actual.valor.estudiante_id == str(estudiante_id)
                and actual.valor.anio == anio
                and actual.valor.term not in terminos
            ):
                terminos.append(actual.valor.term)
            actual = actual.siguiente
        return terminos

    def eliminar(self, estudiante_id: str, anio: int, term: int) -> Semestre | None:
        """Elimina un semestre específico de un estudiante.

        Args:
            estudiante_id (str): ID del estudiante.
            anio (int): Año del semestre.
            term (int): Término del semestre.

        Returns:
            Semestre | None: Semestre eliminado o None si no existe.
        """

        actual = self.cabeza

        while actual is not None:
            valor = actual.valor
            if (
                valor.estudiante_id == str(estudiante_id)
                and valor.anio == anio
                and valor.term == term
            ):
                if actual.anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    actual.anterior.siguiente = actual.siguiente

                if actual.siguiente is None:
                    self.cola = actual.anterior
                else:
                    actual.siguiente.anterior = actual.anterior

                return valor
            actual = actual.siguiente
        return None

    def recorrer_adelante(self) -> list[Semestre]:
        """Recorre la lista desde la cabeza hasta la cola.

        Returns:
            list[Semestre]: Semestres en orden ascendente.
        """

        recorrido: list[Semestre] = []
        actual = self.cabeza
        while actual is not None:
            recorrido.append(actual.valor)
            actual = actual.siguiente
        return recorrido

    def recorrer_atras(self) -> list[Semestre]:
        """Recorre la lista desde la cola hasta la cabeza.

        Returns:
            list[Semestre]: Semestres en orden descendente.
        """

        recorrido: list[Semestre] = []
        actual = self.cola
        while actual is not None:
            recorrido.append(actual.valor)
            actual = actual.anterior
        return recorrido

    def limpiar(self):
        """Elimina todas las referencias almacenadas en la lista."""

        self.cabeza = None
        self.cola = None

    def exportar_json(self, ruta):
        """Exporta el historial académico a un archivo JSON.

        Args:
            ruta (str): Ruta del archivo de salida.
        """

        from .persistencia_json import exportar_historial_json

        exportar_historial_json(self, ruta)

    def importar_json(self, ruta):
        """Importa el historial académico desde un archivo JSON.

        Args:
            ruta (str): Ruta del archivo de entrada.
        """

        from .persistencia_json import importar_historial_json

        importar_historial_json(ruta, self)

    def _comparar(self, dato1: Semestre, dato2: Semestre) -> int:
        """Compara dos semestres por año y término.

        Args:
            dato1 (Semestre): Primer semestre a comparar.
            dato2 (Semestre): Segundo semestre a comparar.

        Returns:
            int: -1 si dato1 es menor, 1 si es mayor y 0 si son iguales.
        """

        if dato1.anio < dato2.anio:
            return -1
        if dato1.anio > dato2.anio:
            return 1
        if dato1.term < dato2.term:
            return -1
        if dato1.term > dato2.term:
            return 1
        return 0