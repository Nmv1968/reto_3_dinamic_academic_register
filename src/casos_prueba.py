import os

from estudiante import Estudiante
from lista_circular import ListaCircular
from lista_doble import ListaDoble
from lista_simple import ListaSimple
from persistencia_csv import importar_inscritos_csv
from persistencia_json import importar_grupos_json, importar_historial_json


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def borrar_si_existe(ruta):
    if os.path.exists(ruta):
        os.remove(ruta)


def probar_lista_simple():
    print("Prueba de lista simple")
    lista = ListaSimple()
    ana = Estudiante("Ana", "ana@correo.com")
    luis = Estudiante("Luis", "luis@correo.com")
    mia = Estudiante("Mia", "mia@correo.com")

    lista.insertar_final(ana)
    lista.insertar_final(luis)
    lista.insertar_final(mia)

    encontrado = lista.buscar(luis.id_estudiante)
    assert encontrado is not None
    assert encontrado.nombres == "Luis"

    eliminado = lista.eliminar(ana.id_estudiante)
    assert eliminado is not None
    assert eliminado.nombres == "Ana"

    ruta = os.path.join(DATA_DIR, "inscritos_prueba.csv")
    lista.exportar_csv(ruta)
    nueva = importar_inscritos_csv(ruta)
    estudiante_mia = nueva.buscar(mia.id_estudiante)

    assert nueva.contar() == 2
    assert estudiante_mia is not None
    assert estudiante_mia.correo == "mia@correo.com"
    borrar_si_existe(ruta)
    print("OK lista simple")


def probar_lista_doble():
    print("Prueba de lista doble")
    lista = ListaDoble()
    lista.insertar_ordenado(
        {
            "anio": 2025,
            "term": 2,
            "materias": [{"cod": "MAT1", "nombre": "Matematicas", "nota": 4.5}],
        }
    )
    lista.insertar_ordenado(
        {
            "anio": 2024,
            "term": 2,
            "materias": [{"cod": "PRO1", "nombre": "Programacion", "nota": 4.8}],
        }
    )
    lista.insertar_ordenado(
        {
            "anio": 2025,
            "term": 1,
            "materias": [{"cod": "BD1", "nombre": "Bases de Datos", "nota": 4.2}],
        }
    )

    adelante = lista.recorrer_adelante()
    atras = lista.recorrer_atras()

    assert [(x["anio"], x["term"]) for x in adelante] == [(2024, 2), (2025, 1), (2025, 2)]
    assert [(x["anio"], x["term"]) for x in atras] == [(2025, 2), (2025, 1), (2024, 2)]

    ruta = os.path.join(DATA_DIR, "historial_prueba.json")
    lista.exportar_json(ruta)
    nueva = importar_historial_json(ruta)
    semestre = nueva.buscar(2025, 1)

    assert semestre is not None
    assert semestre["materias"][0]["cod"] == "BD1"
    borrar_si_existe(ruta)
    print("OK lista doble")


def probar_lista_circular():
    print("Prueba de lista circular")
    lista = ListaCircular()
    lista.insertar({"nombre_grupo": "A", "tutor": "Luis", "tema": "Grafos"})
    lista.insertar({"nombre_grupo": "B", "tutor": "Ana", "tema": "Arboles"})
    lista.insertar({"nombre_grupo": "C", "tutor": "Mia", "tema": "Listas"})

    encontrado = lista.buscar_recursivo("B")
    assert encontrado is not None
    assert encontrado["tema"] == "Arboles"

    actual = lista.rotar(2)
    assert actual is not None
    assert actual["nombre_grupo"] == "C"

    eliminado = lista.eliminar("B")
    assert eliminado is not None
    assert eliminado["nombre_grupo"] == "B"

    recorrido = lista.recorrer()
    assert [x["nombre_grupo"] for x in recorrido] == ["C", "A"]

    ruta = os.path.join(DATA_DIR, "grupos_prueba.json")
    lista.exportar_json(ruta)
    nueva = importar_grupos_json(ruta)
    grupo_a = nueva.buscar_recursivo("A")

    assert grupo_a is not None
    assert grupo_a["tutor"] == "Luis"
    assert nueva.actual is not None
    assert nueva.actual.siguiente is not None
    assert nueva.actual.siguiente.siguiente == nueva.actual
    borrar_si_existe(ruta)
    print("OK lista circular")


def ejecutar_pruebas():
    probar_lista_simple()
    probar_lista_doble()
    probar_lista_circular()
    print("Todas las pruebas terminaron correctamente.")


if __name__ == "__main__":
    ejecutar_pruebas()