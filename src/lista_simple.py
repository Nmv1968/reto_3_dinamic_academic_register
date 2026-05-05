
from nodo_simple import NodoSimple


class ListaSimple:
    def __init__(self):
        self.cabeza = None

    def esta_vacia(self):
        return self.cabeza is None

    def insertar_final(self, dato):
        nuevo = NodoSimple(dato)
        if self.cabeza is None:
            self.cabeza = nuevo
            return dato

        actual = self.cabeza
        while actual.siguiente is not None:
            actual = actual.siguiente
        actual.siguiente = nuevo
        return dato

    def buscar(self, identificador):
        actual = self.cabeza
        while actual is not None:
            valor = actual.valor
            if valor.id_estudiante == str(identificador):
                return valor
            actual = actual.siguiente
        return None

    def eliminar(self, identificador):
        actual = self.cabeza
        anterior = None

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

    def recorrer(self):
        actual = self.cabeza
        recorrido = []
        while actual is not None:
            recorrido.append(actual.valor)
            actual = actual.siguiente
        return recorrido

    def contar(self):
        total = 0
        actual = self.cabeza
        while actual is not None:
            total += 1
            actual = actual.siguiente
        return total

    def limpiar(self):
        self.cabeza = None

    def exportar_csv(self, ruta):
        from persistencia_csv import exportar_inscritos_csv

        exportar_inscritos_csv(self, ruta)

    def importar_csv(self, ruta):
        from persistencia_csv import importar_inscritos_csv

        importar_inscritos_csv(ruta, self)