from .nodo_doble import NodoDoble
from .semestre import Semestre


class ListaDoble:
    def __init__(self):
        self.cabeza: NodoDoble | None = None
        self.cola: NodoDoble | None = None

    def esta_vacia(self) -> bool:
        return self.cabeza is None

    def insertar_ordenado(self, dato: Semestre) -> Semestre:
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
        actual = self.cabeza
        historial: list[Semestre] = []
        while actual is not None:
            if actual.valor.estudiante_id == str(estudiante_id):
                historial.append(actual.valor)
            actual = actual.siguiente
        return historial

    def buscar_semestre(self, estudiante_id: str, anio: int, term: int) -> Semestre | None:
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
        actual = self.cabeza
        while actual is not None:
            valor = actual.valor
            if valor.anio == anio and valor.term == term:
                return valor
            actual = actual.siguiente
        return None

    def existe_estudiante(self, estudiante_id: str) -> bool:
        actual = self.cabeza
        while actual is not None:
            if actual.valor.estudiante_id == str(estudiante_id):
                return True
            actual = actual.siguiente
        return False

    def existe_anio(self, anio: int) -> bool:
        actual = self.cabeza
        while actual is not None:
            if actual.valor.anio == anio:
                return True
            actual = actual.siguiente
        return False

    def obtener_terminos_por_anio(self, anio: int) -> list[int]:
        actual = self.cabeza
        terminos: list[int] = []
        while actual is not None:
            if actual.valor.anio == anio and actual.valor.term not in terminos:
                terminos.append(actual.valor.term)
            actual = actual.siguiente
        return terminos

    def existe_anio_de_estudiante(self, estudiante_id: str, anio: int) -> bool:
        actual = self.cabeza
        while actual is not None:
            if actual.valor.estudiante_id == str(estudiante_id) and actual.valor.anio == anio:
                return True
            actual = actual.siguiente
        return False

    def obtener_terminos_por_estudiante_y_anio(self, estudiante_id: str, anio: int) -> list[int]:
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
        recorrido: list[Semestre] = []
        actual = self.cabeza
        while actual is not None:
            recorrido.append(actual.valor)
            actual = actual.siguiente
        return recorrido

    def recorrer_atras(self) -> list[Semestre]:
        recorrido: list[Semestre] = []
        actual = self.cola
        while actual is not None:
            recorrido.append(actual.valor)
            actual = actual.anterior
        return recorrido

    def limpiar(self):
        self.cabeza = None
        self.cola = None

    def exportar_json(self, ruta):
        from .persistencia_json import exportar_historial_json

        exportar_historial_json(self, ruta)

    def importar_json(self, ruta):
        from .persistencia_json import importar_historial_json

        importar_historial_json(ruta, self)

    def _comparar(self, dato1: Semestre, dato2: Semestre) -> int:
        if dato1.anio < dato2.anio:
            return -1
        if dato1.anio > dato2.anio:
            return 1
        if dato1.term < dato2.term:
            return -1
        if dato1.term > dato2.term:
            return 1
        return 0