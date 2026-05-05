from nodo_doble import NodoDoble


class ListaDoble:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def esta_vacia(self):
        return self.cabeza is None

    def insertar_ordenado(self, dato):
        nuevo = NodoDoble(dato)

        if self.cabeza is None:
            self.cabeza = nuevo
            self.cola = nuevo
            return dato

        actual = self.cabeza
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

    def buscar(self, anio, term):
        actual = self.cabeza
        while actual is not None:
            valor = actual.valor
            if valor.get("anio") == anio and valor.get("term") == term:
                return valor
            actual = actual.siguiente
        return None

    def eliminar(self, anio, term):
        actual = self.cabeza

        while actual is not None:
            valor = actual.valor
            if valor.get("anio") == anio and valor.get("term") == term:
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

    def recorrer_adelante(self):
        recorrido = []
        actual = self.cabeza
        while actual is not None:
            recorrido.append(actual.valor)
            actual = actual.siguiente
        return recorrido

    def recorrer_atras(self):
        recorrido = []
        actual = self.cola
        while actual is not None:
            recorrido.append(actual.valor)
            actual = actual.anterior
        return recorrido

    def limpiar(self):
        self.cabeza = None
        self.cola = None

    def exportar_json(self, ruta):
        from persistencia_json import exportar_historial_json

        exportar_historial_json(self, ruta)

    def importar_json(self, ruta):
        from persistencia_json import importar_historial_json

        importar_historial_json(ruta, self)

    def _comparar(self, dato1, dato2):
        if dato1["anio"] < dato2["anio"]:
            return -1
        if dato1["anio"] > dato2["anio"]:
            return 1
        if dato1["term"] < dato2["term"]:
            return -1
        if dato1["term"] > dato2["term"]:
            return 1
        return 0