from .estudiante import Estudiante
from .nodo_simple import NodoSimple


class ListaSimple:
    def __init__(self):
        self.cabeza: NodoSimple | None = None

    def esta_vacia(self) -> bool:
        return self.cabeza is None

    def insertar_final(self, dato: Estudiante) -> Estudiante:
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
        actual = self.cabeza
        while actual is not None:
            valor = actual.valor
            if valor.id_estudiante == str(identificador):
                return valor
            actual = actual.siguiente
        return None

    def buscar_por_ci(self, ci_estudiante: str) -> Estudiante | None:
        actual = self.cabeza
        while actual is not None:
            valor = actual.valor
            if valor.ci_estudiante == str(ci_estudiante):
                return valor
            actual = actual.siguiente
        return None

    def eliminar(self, identificador: str) -> Estudiante | None:
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
        actual = self.cabeza
        recorrido: list[Estudiante] = []
        while actual is not None:
            recorrido.append(actual.valor)
            actual = actual.siguiente
        return recorrido

    def contar(self) -> int:
        total = 0
        actual = self.cabeza
        while actual is not None:
            total += 1
            actual = actual.siguiente
        return total

    def limpiar(self):
        self.cabeza = None

    def exportar_csv(self, ruta):
        from .persistencia_csv import exportar_inscritos_csv

        exportar_inscritos_csv(self, ruta)

    def importar_csv(self, ruta):
        from .persistencia_csv import importar_inscritos_csv

        importar_inscritos_csv(ruta, self)