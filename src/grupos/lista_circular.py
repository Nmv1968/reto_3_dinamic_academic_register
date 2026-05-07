from .grupo import Grupo
from .nodo_circular import NodoCircular


class ListaCircular:
    def __init__(self):
        self.actual: NodoCircular | None = None

    def esta_vacia(self) -> bool:
        return self.actual is None

    def insertar(self, dato: Grupo) -> Grupo:
        nuevo = NodoCircular(dato)

        if self.actual is None:
            self.actual = nuevo
            nuevo.siguiente = nuevo
            return dato

        ultimo = self._ultimo()
        nuevo.siguiente = self.actual
        if ultimo is not None:
            ultimo.siguiente = nuevo
        return dato

    def buscar_recursivo(
        self,
        nombre_grupo: str,
        nodo: NodoCircular | None = None,
        inicio: NodoCircular | None = None,
    ) -> Grupo | None:
        if self.actual is None:
            return None

        if nodo is None:
            nodo = self.actual
            inicio = self.actual

        if nodo is None:
            return None

        if nodo.valor.nombre_grupo == nombre_grupo:
            return nodo.valor

        if nodo.siguiente == inicio:
            return None

        return self.buscar_recursivo(nombre_grupo, nodo.siguiente, inicio)

    def buscar_por_estudiante_id(self, estudiante_id: str) -> Grupo | None:
        if self.actual is None:
            return None

        actual: NodoCircular | None = self.actual
        while True:
            if actual is None:
                return None
            if str(estudiante_id) in actual.valor.integrantes_ids:
                return actual.valor
            actual = actual.siguiente
            if actual == self.actual:
                break
        return None

    def eliminar(self, nombre_grupo: str) -> Grupo | None:
        if self.actual is None:
            return None

        actual: NodoCircular | None = self.actual
        anterior: NodoCircular | None = None

        while True:
            if actual is None:
                return None

            if actual.valor.nombre_grupo == nombre_grupo:
                if actual.siguiente == actual:
                    eliminado = actual.valor
                    self.actual = None
                    return eliminado

                if anterior is None:
                    ultimo = self._ultimo()
                    eliminado = actual.valor
                    self.actual = actual.siguiente
                    if ultimo is not None:
                        ultimo.siguiente = self.actual
                    return eliminado

                eliminado = actual.valor
                anterior.siguiente = actual.siguiente
                if actual == self.actual:
                    self.actual = actual.siguiente
                return eliminado

            anterior = actual
            actual = actual.siguiente
            if actual == self.actual:
                break
        return None

    def rotar(self, k: int) -> Grupo | None:
        if self.actual is None:
            return None

        pasos = 0
        while pasos < k:
            if self.actual.siguiente is not None:
                self.actual = self.actual.siguiente
            pasos += 1
        return self.actual.valor

    def recorrer(self) -> list[Grupo]:
        recorrido: list[Grupo] = []
        if self.actual is None:
            return recorrido

        recorrido.append(self.actual.valor)
        nodo: NodoCircular | None = self.actual.siguiente
        while nodo != self.actual:
            if nodo is None:
                break
            recorrido.append(nodo.valor)
            nodo = nodo.siguiente
        return recorrido

    def limpiar(self):
        self.actual = None

    def exportar_json(self, ruta):
        from .persistencia_json import exportar_grupos_json

        exportar_grupos_json(self, ruta)

    def importar_json(self, ruta):
        from .persistencia_json import importar_grupos_json

        importar_grupos_json(ruta, self)

    def _ultimo(self) -> NodoCircular | None:
        ultimo = self.actual
        while ultimo is not None and ultimo.siguiente != self.actual:
            ultimo = ultimo.siguiente
        return ultimo