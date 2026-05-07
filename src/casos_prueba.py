import os

from grupos import Grupo, ListaCircular, importar_grupos_json
from historial import ListaDoble, Materia, Semestre, importar_historial_json
from inscritos import Estudiante, ListaSimple, importar_inscritos_csv


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def borrar_si_existe(ruta):
    if os.path.exists(ruta):
        os.remove(ruta)


def probar_lista_simple():
    print("Prueba de lista simple")
    lista = ListaSimple()
    ana = Estudiante("Ana", "ana@correo.com", "1000000001")
    luis = Estudiante("Luis", "luis@correo.com", "1000000002")
    mia = Estudiante("Mia", "mia@correo.com", "1000000003")

    try:
        Estudiante("Invalido", "invalido@correo.com", "123")
        assert False
    except ValueError:
        pass

    lista.insertar_final(ana)
    lista.insertar_final(luis)
    lista.insertar_final(mia)

    encontrado = lista.buscar(luis.id_estudiante)
    assert encontrado is not None
    assert encontrado.nombres == "Luis"

    encontrado_por_ci = lista.buscar_por_ci(luis.ci_estudiante)
    assert encontrado_por_ci is not None
    assert encontrado_por_ci.correo == "luis@correo.com"

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
    assert estudiante_mia.ci_estudiante == mia.ci_estudiante
    assert estudiante_mia.id_estudiante == mia.id_estudiante
    borrar_si_existe(ruta)
    print("OK lista simple")


def probar_lista_doble():
    print("Prueba de lista doble")
    lista = ListaDoble()
    lista.insertar_ordenado(
        Semestre(2025, 2, [Materia("MAT1", "Matematicas", 4.5)])
    )
    lista.insertar_ordenado(
        Semestre(2024, 2, [Materia("PRO1", "Programacion", 4.8)])
    )
    lista.insertar_ordenado(
        Semestre(2025, 1, [Materia("BD1", "Bases de Datos", 4.2)])
    )

    adelante = lista.recorrer_adelante()
    atras = lista.recorrer_atras()

    assert [(x.anio, x.term) for x in adelante] == [(2024, 2), (2025, 1), (2025, 2)]
    assert [(x.anio, x.term) for x in atras] == [(2025, 2), (2025, 1), (2024, 2)]
    assert lista.existe_anio(2025) is True
    assert lista.existe_anio(2023) is False
    assert lista.obtener_terminos_por_anio(2025) == [1, 2]

    ruta = os.path.join(DATA_DIR, "historial_prueba.json")
    lista.exportar_json(ruta)
    nueva = importar_historial_json(ruta)
    semestre = nueva.buscar(2025, 1)

    assert semestre is not None
    assert semestre.materias[0].cod == "BD1"
    borrar_si_existe(ruta)
    print("OK lista doble")


def probar_lista_circular():
    print("Prueba de lista circular")
    lista = ListaCircular()
    lista.insertar(Grupo("A", "Luis", "Grafos"))
    lista.insertar(Grupo("B", "Ana", "Arboles"))
    lista.insertar(Grupo("C", "Mia", "Listas"))

    encontrado = lista.buscar_recursivo("B")
    assert encontrado is not None
    assert encontrado.tema == "Arboles"

    actual = lista.rotar(2)
    assert actual is not None
    assert actual.nombre_grupo == "C"

    eliminado = lista.eliminar("B")
    assert eliminado is not None
    assert eliminado.nombre_grupo == "B"

    recorrido = lista.recorrer()
    assert [x.nombre_grupo for x in recorrido] == ["C", "A"]

    ruta = os.path.join(DATA_DIR, "grupos_prueba.json")
    lista.exportar_json(ruta)
    nueva = importar_grupos_json(ruta)
    grupo_a = nueva.buscar_recursivo("A")

    assert grupo_a is not None
    assert grupo_a.tutor == "Luis"
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