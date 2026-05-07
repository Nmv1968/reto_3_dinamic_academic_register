"""Aplicación principal del sistema de registros académicos.

Este módulo coordina la interacción por consola entre la lista simple de
inscritos, la lista doble del historial académico y la lista circular de
grupos de exposición. También centraliza las validaciones de entrada, los
formatos de visualización y la carga o exportación de datos persistidos.
"""

import os

from grupos import Grupo, ListaCircular
from historial import ListaDoble, Materia, Semestre
from inscritos import Estudiante, ListaSimple


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RUTA_INSCRITOS = os.path.join(DATA_DIR, "inscritos.csv")
RUTA_HISTORIAL = os.path.join(DATA_DIR, "historial.json")
RUTA_GRUPOS = os.path.join(DATA_DIR, "grupos.json")


def mostrar_titulo(titulo):
    """Imprime un encabezado con una línea de separación.

    Args:
        titulo (str): Texto que se mostrará como título.
    """

    print("\n" + titulo)
    print("=" * len(titulo))


def archivo_tiene_datos(ruta):
    """Verifica si un archivo existe y contiene información.

    Args:
        ruta (str): Ruta del archivo que se desea comprobar.

    Returns:
        bool: True si el archivo existe y su tamaño es mayor que cero.
    """

    return os.path.exists(ruta) and os.path.getsize(ruta) > 0


def validar_input(mensaje):
    """Solicita una entrada de texto no vacía.

    Args:
        mensaje (str): Texto que se muestra al usuario en consola.

    Returns:
        str: Valor ingresado sin espacios al inicio ni al final.
    """

    while True:
        texto = input(mensaje)
        if texto.strip() != "":
            return texto.strip()
        print("Entrada no válida. Ingrese un valor no vacío. ⛔")


def validar_opcion(mensaje, opciones_validas):
    """Solicita una opción y valida que pertenezca al conjunto permitido.

    Args:
        mensaje (str): Texto que se muestra al solicitar la opción.
        opciones_validas (list[str] | tuple[str, ...]): Opciones aceptadas.

    Returns:
        str: Opción válida seleccionada por el usuario.
    """

    while True:
        opcion = validar_input(mensaje)
        if opcion in opciones_validas:
            return opcion
        print("Opción no válida. Intente nuevamente. ⛔")


def pedir_entero(mensaje, minimo=None, maximo=None):
    """Solicita un número entero dentro de un rango opcional.

    Args:
        mensaje (str): Texto mostrado al solicitar el valor.
        minimo (int | None): Límite inferior aceptado.
        maximo (int | None): Límite superior aceptado.

    Returns:
        int: Número entero validado.
    """

    while True:
        texto = validar_input(mensaje)
        try:
            numero = int(texto)
            if minimo is not None and numero < minimo:
                print("El número ingresado es demasiado pequeño. ⛔")
                continue
            if maximo is not None and numero > maximo:
                print("El número ingresado es demasiado grande. ⛔")
                continue
            return numero
        except ValueError:
            print("Ingrese un número entero válido. ⛔")


def pedir_flotante(mensaje, minimo=None, maximo=None):
    """Solicita un número flotante dentro de un rango opcional.

    Args:
        mensaje (str): Texto mostrado al solicitar el valor.
        minimo (float | None): Límite inferior aceptado.
        maximo (float | None): Límite superior aceptado.

    Returns:
        float: Número decimal validado.
    """

    while True:
        texto = validar_input(mensaje)
        try:
            numero = float(texto)
            if minimo is not None and numero < minimo:
                print("El número ingresado es demasiado pequeño. ⛔")
                continue
            if maximo is not None and numero > maximo:
                print("El número ingresado es demasiado grande. ⛔")
                continue
            return numero
        except ValueError:
            print("Ingrese un número válido. ⛔")


def validar_ci(mensaje):
    """Solicita una cédula ecuatoriana de 10 dígitos.

    Args:
        mensaje (str): Texto mostrado al solicitar la cédula.

    Returns:
        str: Cédula válida compuesta solo por dígitos.
    """

    while True:
        ci_estudiante = validar_input(mensaje)
        if not ci_estudiante.isdigit():
            print("La cédula solo debe contener dígitos. ⛔")
            continue
        if len(ci_estudiante) != 10:
            print("La cédula debe tener exactamente 10 dígitos. ⛔")
            continue
        return ci_estudiante


def validar_correo(mensaje):
    """Solicita un correo electrónico con formato básico válido.

    Args:
        mensaje (str): Texto mostrado al solicitar el correo.

    Returns:
        str: Correo validado.
    """

    while True:
        correo = validar_input(mensaje)
        if " " in correo:
            print("El correo no puede tener espacios. ⛔")
            continue
        if "@" not in correo:
            print("El correo debe tener el símbolo @. ⛔")
            continue
        partes = correo.split("@")
        if len(partes) != 2 or partes[0] == "" or partes[1] == "":
            print("El correo no tiene un formato válido. ⛔")
            continue
        if "." not in partes[1]:
            print("El dominio del correo no es válido. ⛔")
            continue
        return correo


def cargar_datos(inscritos, historial, grupos):
    """Carga los datos persistidos del sistema.

    Args:
        inscritos (ListaSimple): Estructura donde se cargan los inscritos.
        historial (ListaDoble): Estructura donde se cargan los semestres.
        grupos (ListaCircular): Estructura donde se cargan los grupos.
    """

    if archivo_tiene_datos(RUTA_INSCRITOS):
        inscritos.importar_csv(RUTA_INSCRITOS)
    if archivo_tiene_datos(RUTA_HISTORIAL):
        historial.importar_json(RUTA_HISTORIAL)
    if archivo_tiene_datos(RUTA_GRUPOS):
        grupos.importar_json(RUTA_GRUPOS)


def mostrar_tabla(titulo, encabezados, filas, detalles=None, total=None):
    """Renderiza una tabla ASCII con detalles opcionales.

    Args:
        titulo (str): Título que se mostrará antes de la tabla.
        encabezados (tuple[str, ...]): Nombres de las columnas.
        filas (list[tuple[str, ...]]): Datos principales de cada fila.
        detalles (list[str] | None): Texto adicional asociado a cada fila.
        total (str | None): Resumen final que se imprime bajo la tabla.
    """

    mostrar_titulo(titulo)

    anchos = []
    for indice, encabezado in enumerate(encabezados):
        ancho = len(encabezado)
        for fila in filas:
            ancho = max(ancho, len(str(fila[indice])))
        anchos.append(ancho)

    ancho_interno = sum(anchos) + (3 * (len(encabezados) - 1))
    if detalles:
        ancho_detalle = max(len(detalle) for detalle in detalles)
        if ancho_detalle > ancho_interno:
            anchos[-1] += ancho_detalle - ancho_interno
            ancho_interno = ancho_detalle

    separador = "+-" + "-+-".join("-" * ancho for ancho in anchos) + "-+"
    encabezado_tabla = "| " + " | ".join(
        encabezado.ljust(ancho) for encabezado, ancho in zip(encabezados, anchos)
    ) + " |"

    print(separador)
    print(encabezado_tabla)
    print(separador)
    for indice, fila in enumerate(filas):
        print(
            "| "
            + " | ".join(str(valor).ljust(ancho) for valor, ancho in zip(fila, anchos))
            + " |"
        )
        if detalles:
            print("| " + detalles[indice].ljust(ancho_interno) + " |")
        print(separador)

    if total is not None:
        print(total)


def mostrar_inscritos(inscritos):
    """Muestra el listado tabular de estudiantes inscritos.

    Args:
        inscritos (ListaSimple): Lista simple con los estudiantes registrados.
    """

    datos = inscritos.recorrer()
    if len(datos) == 0:
        print("No hay inscritos registrados. ⛔")
        return

    encabezados = ("No", "Nombres", "CI", "Correo")
    filas = [
        (
            str(indice + 1),
            inscrito.nombres,
            inscrito.ci_estudiante,
            inscrito.correo,
        )
        for indice, inscrito in enumerate(datos)
    ]

    detalles = [f"ID: {inscrito.id_estudiante}" for inscrito in datos]
    mostrar_tabla(
        "Listado de inscritos",
        encabezados,
        filas,
        detalles,
        f"Total de inscritos: {len(datos)}",
    )


def mostrar_estudiante(estudiante, encabezado="===ESTUDIANTE ENCONTRADO==="):
    """Imprime los datos completos de un estudiante en formato vertical.

    Args:
        estudiante (Estudiante): Estudiante que se desea mostrar.
        encabezado (str): Texto que se imprime como encabezado del bloque.
    """

    print(encabezado)
    print("ID:", estudiante.id_estudiante)
    print("Nombres:", estudiante.nombres)
    print("Correo:", estudiante.correo)
    print("CI:", estudiante.ci_estudiante)
    print("========================")


def obtener_estudiante_por_id(inscritos, estudiante_id):
    """Busca un estudiante inscrito por su identificador interno.

    Args:
        inscritos (ListaSimple): Lista simple de inscritos.
        estudiante_id (str): Identificador único del estudiante.

    Returns:
        Estudiante | None: Estudiante encontrado o None si no existe.
    """

    if estudiante_id == "":
        return None
    return inscritos.buscar(estudiante_id)


def obtener_nombre_estudiante(inscritos, estudiante_id):
    """Obtiene el nombre visible de un estudiante.

    Args:
        inscritos (ListaSimple): Lista simple de inscritos.
        estudiante_id (str): Identificador interno del estudiante.

    Returns:
        str: Nombre del estudiante o un texto de estado si no existe.
    """

    if estudiante_id == "":
        return "Sin asignar"

    estudiante = obtener_estudiante_por_id(inscritos, estudiante_id)
    if estudiante is None:
        return "No inscrito"
    return estudiante.nombres


def obtener_resumen_estudiante(inscritos, estudiante_id):
    """Devuelve un resumen corto de un estudiante.

    Args:
        inscritos (ListaSimple): Lista simple de inscritos.
        estudiante_id (str): Identificador interno del estudiante.

    Returns:
        str: Texto con cédula y nombres, o un mensaje de estado.
    """

    if estudiante_id == "":
        return "Sin asignar"

    estudiante = obtener_estudiante_por_id(inscritos, estudiante_id)
    if estudiante is None:
        return "No inscrito"
    return f"CI: {estudiante.ci_estudiante} - Nombres: {estudiante.nombres}"


def describir_materias(semestre):
    """Construye una descripción resumida de las materias de un semestre.

    Args:
        semestre (Semestre): Semestre cuyas materias se desean describir.

    Returns:
        str: Texto con las materias registradas o un mensaje de ausencia.
    """

    if len(semestre.materias) == 0:
        return "Sin materias registradas"

    return " | ".join(
        f"{materia.cod} - {materia.nombre} (Nota: {materia.nota})"
        for materia in semestre.materias
    )


def describir_integrantes(grupo, inscritos):
    """Genera las descripciones visibles de los integrantes de un grupo.

    Args:
        grupo (Grupo): Grupo cuyos integrantes se desean listar.
        inscritos (ListaSimple): Lista simple usada para resolver estudiantes.

    Returns:
        list[str]: Lista de textos con el resumen de cada integrante.
    """

    if len(grupo.integrantes_ids) == 0:
        return ["Sin integrantes registrados"]

    descripciones = []
    for integrante_id in grupo.integrantes_ids:
        descripciones.append(obtener_resumen_estudiante(inscritos, integrante_id))
    return descripciones


def mostrar_semestre(inscritos, semestre, encabezado="===SEMESTRE ENCONTRADO==="):
    """Muestra un semestre individual con el estudiante asociado.

    Args:
        inscritos (ListaSimple): Lista simple usada para resolver el estudiante.
        semestre (Semestre): Semestre que se desea mostrar.
        encabezado (str): Texto que se imprime como encabezado.
    """

    resumen_estudiante = obtener_resumen_estudiante(inscritos, semestre.estudiante_id)
    print(encabezado)
    print("Estudiante:", resumen_estudiante)
    print("Año:", semestre.anio)
    print("Término:", semestre.term)
    print("Materias registradas:", len(semestre.materias))
    print("Detalle de materias:")
    if len(semestre.materias) == 0:
        print("- Sin materias registradas")
    else:
        for materia in semestre.materias:
            print(f"- {materia.cod} | {materia.nombre} | Nota: {materia.nota}")
    print("========================")


def mostrar_grupo(inscritos, grupo, encabezado="===GRUPO ENCONTRADO==="):
    """Muestra los datos de un grupo y sus integrantes.

    Args:
        inscritos (ListaSimple): Lista simple usada para resolver integrantes.
        grupo (Grupo): Grupo que se desea mostrar.
        encabezado (str): Texto que se imprime como encabezado.
    """

    print(encabezado)
    print("Nombre del grupo:", grupo.nombre_grupo)
    print("Tutor:", grupo.tutor)
    print("Tema:", grupo.tema)
    print("Integrantes registrados:", len(grupo.integrantes_ids))
    print("Detalle de integrantes:")
    for integrante in describir_integrantes(grupo, inscritos):
        print(f"- {integrante}")
    print("========================")


def mostrar_historial(inscritos, historial, hacia_atras=False):
    """Muestra todo el historial académico en formato tabular.

    Args:
        inscritos (ListaSimple): Lista simple usada para resolver estudiantes.
        historial (ListaDoble): Lista doble con los semestres registrados.
        hacia_atras (bool): Indica si el recorrido debe hacerse desde la cola.
    """

    if hacia_atras:
        datos = historial.recorrer_atras()
        titulo = "Listado del historial académico (hacia atrás)"
    else:
        datos = historial.recorrer_adelante()
        titulo = "Listado del historial académico (hacia adelante)"

    if len(datos) == 0:
        print("No hay semestres registrados. ⛔")
        return

    encabezados = ("No", "Estudiante", "Año", "Término", "Materias")
    filas = [
        (
            str(indice + 1),
            obtener_resumen_estudiante(inscritos, semestre.estudiante_id),
            str(semestre.anio),
            str(semestre.term),
            str(len(semestre.materias)),
        )
        for indice, semestre in enumerate(datos)
    ]
    detalles = [f"Materias: {describir_materias(semestre)}" for semestre in datos]

    mostrar_tabla(titulo, encabezados, filas, detalles, f"Total de semestres: {len(datos)}")


def mostrar_historial_estudiante(inscritos, estudiante, semestres):
    """Muestra el historial de un estudiante con formato vertical o tabular.

    Args:
        inscritos (ListaSimple): Lista simple de inscritos.
        estudiante (Estudiante): Estudiante dueño del historial.
        semestres (list[Semestre]): Semestres asociados al estudiante.
    """

    if len(semestres) == 1:
        mostrar_semestre(inscritos, semestres[0], "===HISTORIAL DEL ESTUDIANTE===")
        return

    encabezados = ("No", "Año", "Término", "Materias")
    filas = [
        (
            str(indice + 1),
            str(semestre.anio),
            str(semestre.term),
            str(len(semestre.materias)),
        )
        for indice, semestre in enumerate(semestres)
    ]
    detalles = [f"Detalle: {describir_materias(semestre)}" for semestre in semestres]
    mostrar_tabla(
        f"Historial de {estudiante.ci_estudiante} | {estudiante.nombres}",
        encabezados,
        filas,
        detalles,
        f"Total de semestres: {len(semestres)}",
    )


def mostrar_grupos(inscritos, grupos):
    """Muestra el listado tabular de grupos con sus integrantes.

    Args:
        inscritos (ListaSimple): Lista simple usada para resolver integrantes.
        grupos (ListaCircular): Lista circular con los grupos registrados.
    """

    datos = grupos.recorrer()
    if len(datos) == 0:
        print("No hay grupos registrados. ⛔")
        return

    encabezados = ("No", "Grupo", "Tutor", "Tema", "Integrantes")
    filas = [
        (
            str(indice + 1),
            grupo.nombre_grupo,
            grupo.tutor,
            grupo.tema,
            str(len(grupo.integrantes_ids)),
        )
        for indice, grupo in enumerate(datos)
    ]
    detalles = [f"Integrantes: {' | '.join(describir_integrantes(grupo, inscritos))}" for grupo in datos]
    mostrar_tabla(
        "Listado de grupos",
        encabezados,
        filas,
        detalles,
        total=f"Total de grupos: {len(datos)}",
    )


def pedir_semestre(estudiante_id):
    """Solicita por consola los datos necesarios para crear un semestre.

    Args:
        estudiante_id (str): Identificador del estudiante asociado al semestre.

    Returns:
        Semestre: Objeto construido con los datos ingresados por el usuario.
    """

    anio = pedir_entero("Ingrese el año: ", 2000, 2100)
    term = pedir_entero("Ingrese el término: ", 1, 2)
    cantidad = pedir_entero("¿Cuántas materias desea agregar?: ", 1)
    materias: list[Materia] = []

    contador = 0
    while contador < cantidad:
        print("Materia", contador + 1)
        cod = validar_input("Código: ")
        nombre = validar_input("Nombre: ")
        nota = pedir_flotante("Nota: ", 0, 10)
        materias.append(Materia(cod, nombre, nota))
        contador += 1

    return Semestre(anio, term, materias, estudiante_id)


def promedio_semestre(semestre):
    """Calcula el promedio de notas de un semestre.

    Args:
        semestre (Semestre): Semestre cuyo promedio se desea calcular.

    Returns:
        float: Promedio de notas o 0 si no hay materias registradas.
    """

    materias = semestre.materias
    if len(materias) == 0:
        return 0

    suma = 0
    for materia in materias:
        suma += materia.nota
    return suma / len(materias)


def reporte_top_3(historial, inscritos):
    """Genera el reporte de los tres mejores promedios semestrales.

    Args:
        historial (ListaDoble): Lista doble con el historial académico.
        inscritos (ListaSimple): Lista simple usada para resolver estudiantes.
    """

    semestres = historial.recorrer_adelante()
    if len(semestres) == 0:
        print("No hay historial para calcular promedios. ⛔")
        return

    datos = []
    for semestre in semestres:
        datos.append(
            {
                "estudiante": obtener_nombre_estudiante(inscritos, semestre.estudiante_id),
                "estudiante_id": semestre.estudiante_id or "Sin asignar",
                "anio": semestre.anio,
                "term": semestre.term,
                "promedio": promedio_semestre(semestre),
            }
        )

    limite = len(datos)
    while limite > 1:
        posicion = 0
        while posicion < limite - 1:
            if datos[posicion]["promedio"] < datos[posicion + 1]["promedio"]:
                temporal = datos[posicion]
                datos[posicion] = datos[posicion + 1]
                datos[posicion + 1] = temporal
            posicion += 1
        limite -= 1

    tope = 3
    if len(datos) < 3:
        tope = len(datos)

    filas = []
    detalles = []
    indice = 0
    while indice < tope:
        item = datos[indice]
        filas.append(
            (
                str(indice + 1),
                item["estudiante"],
                str(item["anio"]),
                str(item["term"]),
                str(round(item["promedio"], 2)),
            )
        )
        detalles.append(f"ID estudiante: {item['estudiante_id']}")
        indice += 1

    mostrar_tabla(
        "Top 3 mejores promedios",
        ("Puesto", "Estudiante", "Año", "Término", "Promedio"),
        filas,
        detalles,
        total=f"Total mostrado: {tope}",
    )


def reporte_siguiente_grupo(grupos, inscritos):
    """Muestra el siguiente grupo después de rotar la lista circular.

    Args:
        grupos (ListaCircular): Lista circular de grupos.
        inscritos (ListaSimple): Lista simple usada para resolver integrantes.
    """

    grupo = grupos.rotar(1)
    if grupo is None:
        print("No hay grupos registrados. ⛔")
        return
    mostrar_grupo(inscritos, grupo, "===SIGUIENTE GRUPO EN TURNO===")


def reporte_cantidad_inscritos(inscritos):
    """Imprime la cantidad total de estudiantes inscritos.

    Args:
        inscritos (ListaSimple): Lista simple de inscritos.
    """

    print("Cantidad de inscritos:", inscritos.contar())


def crear_estudiante():
    """Solicita los datos del estudiante y crea la entidad correspondiente.

    Returns:
        Estudiante: Estudiante construido con los datos validados.
    """

    nombres = validar_input("Ingrese los nombres del estudiante: ")
    correo = validar_correo("Ingrese el correo del estudiante: ")
    ci_estudiante = validar_ci("Ingrese la cédula del estudiante: ")
    return Estudiante(nombres, correo, ci_estudiante)


def pedir_estudiante_inscrito_por_id(inscritos, accion):
    """Solicita un ID de estudiante y valida que exista.

    Args:
        inscritos (ListaSimple): Lista simple donde se busca al estudiante.
        accion (str): Descripción breve de la acción que se va a realizar.

    Returns:
        Estudiante | None: Estudiante encontrado o None si no existe.
    """

    if inscritos.contar() == 0:
        print("No hay estudiantes inscritos registrados. ⛔")
        return None

    id_estudiante = validar_input(f"ID del estudiante para {accion}: ")
    estudiante = inscritos.buscar(id_estudiante)
    if estudiante is None:
        print("No existe un estudiante inscrito con ese ID. ⛔")
        return None
    return estudiante


def pedir_integrantes_grupo(inscritos):
    """Solicita los integrantes de un grupo verificando que estén inscritos.

    Args:
        inscritos (ListaSimple): Lista simple donde se validan los estudiantes.

    Returns:
        list[str] | None: Lista de IDs válidos o None si no hay inscritos.
    """

    if inscritos.contar() == 0:
        print("Debe existir al menos un estudiante inscrito para crear un grupo. ⛔")
        return None

    cantidad = pedir_entero("¿Cuántos integrantes tendrá el grupo?: ", 1, inscritos.contar())
    integrantes_ids = []

    while len(integrantes_ids) < cantidad:
        indice = len(integrantes_ids) + 1
        id_estudiante = validar_input(f"ID del integrante {indice}: ")
        estudiante = inscritos.buscar(id_estudiante)
        if estudiante is None:
            print("No existe un estudiante inscrito con ese ID. ⛔")
            continue
        if id_estudiante in integrantes_ids:
            print("Ese estudiante ya fue agregado al grupo. ⛔")
            continue
        integrantes_ids.append(id_estudiante)

    return integrantes_ids


def pedir_anio_y_termino_existente(historial, estudiante_id, accion):
    """Solicita un año y un término existentes para un estudiante.

    Args:
        historial (ListaDoble): Lista doble con el historial académico.
        estudiante_id (str): Identificador del estudiante dueño del historial.
        accion (str): Descripción breve de la operación actual.

    Returns:
        tuple[int, int] | None: Par año-término válido o None si falla la validación.
    """

    anio = pedir_entero(f"Año a {accion}: ", 2000, 2100)

    if not historial.existe_anio_de_estudiante(estudiante_id, anio):
        print("Ese estudiante no tiene semestres registrados para ese año. ⛔")
        return None

    terminos_disponibles = historial.obtener_terminos_por_estudiante_y_anio(
        estudiante_id, anio
    )
    print(
        "Términos disponibles para ese estudiante en ese año:",
        ", ".join(str(item) for item in terminos_disponibles),
    )

    term = pedir_entero(f"Término a {accion}: ", 1, 2)
    if term not in terminos_disponibles:
        print("No existe ese término para el año ingresado. ⛔")
        return None

    return anio, term


def menu_inscritos(inscritos):
    """Gestiona las operaciones disponibles para el módulo de inscritos.

    Args:
        inscritos (ListaSimple): Lista simple de estudiantes inscritos.
    """

    while True:
        mostrar_titulo("=== 👥 Módulo Inscritos 👥 ===")
        print("1. Agregar estudiante ➕")
        print("2. Eliminar estudiante 🗑️")
        print("3. Buscar estudiante 🔎")
        print("4. Mostrar inscritos 📋")
        print("5. Exportar CSV 💾")
        print("6. Importar CSV 📥")
        print("0. Volver ↩️")
        opcion = validar_opcion(
            "Seleccione una opción: ", ["1", "2", "3", "4", "5", "6", "0"]
        )

        match opcion:
            case "1":
                estudiante = crear_estudiante()
                inscritos.insertar_final(estudiante)
                print(
                    f"✅ Estudiante agregado con ID: {estudiante.id_estudiante} "
                    f"y CI: {estudiante.ci_estudiante}"
                )
            case "2":
                eliminado = inscritos.eliminar(validar_input("ID a eliminar: "))
                if eliminado is None:
                    print("No se encontró el inscrito. ⛔")
                else:
                    print("✅ Inscrito eliminado:", eliminado.nombres)
            case "3":
                encontrado = inscritos.buscar_por_ci(validar_ci("Cédula a buscar: "))
                if encontrado is None:
                    print("No se encontró el inscrito. ⛔")
                else:
                    mostrar_estudiante(encontrado)
            case "4":
                mostrar_inscritos(inscritos)
            case "5":
                inscritos.exportar_csv(RUTA_INSCRITOS)
                print("✅ Archivo CSV exportado en data/inscritos.csv")
            case "6":
                if archivo_tiene_datos(RUTA_INSCRITOS):
                    inscritos.importar_csv(RUTA_INSCRITOS)
                    print("✅ Archivo CSV importado desde data/inscritos.csv")
                else:
                    print("No hay datos para importar en data/inscritos.csv. ⛔")
            case "0":
                break


def menu_historial(historial, inscritos):
    """Gestiona las operaciones del historial académico por estudiante.

    Args:
        historial (ListaDoble): Lista doble con los semestres registrados.
        inscritos (ListaSimple): Lista simple usada para validar estudiantes.
    """

    while True:
        mostrar_titulo("=== 📚 Módulo Historial Académico 📚 ===")
        print("1. Agregar semestre ➕")
        print("2. Eliminar semestre 🗑️")
        print("3. Buscar historial por ID 🔎")
        print("4. Recorrer adelante ▶️")
        print("5. Recorrer atrás ◀️")
        print("6. Exportar JSON 💾")
        print("7. Importar JSON 📥")
        print("0. Volver ↩️")
        opcion = validar_opcion(
            "Seleccione una opción: ", ["1", "2", "3", "4", "5", "6", "7", "0"]
        )

        match opcion:
            case "1":
                estudiante = pedir_estudiante_inscrito_por_id(inscritos, "registrar un semestre")
                if estudiante is None:
                    continue

                semestre = pedir_semestre(estudiante.id_estudiante)
                if historial.buscar_semestre(estudiante.id_estudiante, semestre.anio, semestre.term) is not None:
                    print("Ese estudiante ya tiene registrado ese año y término. ⛔")
                    continue

                historial.insertar_ordenado(semestre)
                print(f"✅ Semestre agregado para: {estudiante.nombres}")
            case "2":
                estudiante = pedir_estudiante_inscrito_por_id(inscritos, "eliminar un semestre")
                if estudiante is None:
                    continue

                if not historial.existe_estudiante(estudiante.id_estudiante):
                    print("El estudiante no tiene historial académico registrado. ⛔")
                    continue

                datos_semestre = pedir_anio_y_termino_existente(
                    historial, estudiante.id_estudiante, "eliminar"
                )
                if datos_semestre is None:
                    continue

                anio, term = datos_semestre

                eliminado = historial.eliminar(estudiante.id_estudiante, anio, term)
                if eliminado is None:
                    print("No se encontró el semestre. ⛔")
                else:
                    print("✅ Semestre eliminado.")
            case "3":
                estudiante = pedir_estudiante_inscrito_por_id(inscritos, "buscar el historial")
                if estudiante is None:
                    continue

                semestres = historial.buscar_por_estudiante(estudiante.id_estudiante)
                if len(semestres) == 0:
                    print("El estudiante no tiene historial académico registrado. ⛔")
                else:
                    mostrar_historial_estudiante(inscritos, estudiante, semestres)
            case "4":
                mostrar_historial(inscritos, historial, False)
            case "5":
                mostrar_historial(inscritos, historial, True)
            case "6":
                historial.exportar_json(RUTA_HISTORIAL)
                print("✅ Archivo JSON exportado en data/historial.json")
            case "7":
                if archivo_tiene_datos(RUTA_HISTORIAL):
                    historial.importar_json(RUTA_HISTORIAL)
                    print("✅ Archivo JSON importado desde data/historial.json")
                else:
                    print("No hay datos para importar en data/historial.json. ⛔")
            case "0":
                break


def menu_grupos(grupos, inscritos):
    """Gestiona las operaciones del módulo de grupos rotativos.

    Args:
        grupos (ListaCircular): Lista circular con los grupos registrados.
        inscritos (ListaSimple): Lista simple usada para validar integrantes.
    """

    while True:
        mostrar_titulo("=== 🔄 Módulo Grupos Rotativos 🔄 ===")
        print("1. Agregar grupo ➕")
        print("2. Eliminar grupo 🗑️")
        print("3. Buscar grupo recursivamente 🔎")
        print("4. Rotar grupos 🔄")
        print("5. Recorrer grupos 📋")
        print("6. Exportar JSON 💾")
        print("7. Importar JSON 📥")
        print("0. Volver ↩️")
        opcion = validar_opcion(
            "Seleccione una opción: ", ["1", "2", "3", "4", "5", "6", "7", "0"]
        )

        match opcion:
            case "1":
                integrantes_ids = pedir_integrantes_grupo(inscritos)
                if integrantes_ids is None:
                    continue

                grupo = Grupo(
                    validar_input("Nombre del grupo: "),
                    validar_input("Tutor: "),
                    validar_input("Tema: "),
                    integrantes_ids,
                )
                grupos.insertar(grupo)
                print("✅ Grupo agregado.")
            case "2":
                eliminado = grupos.eliminar(validar_input("Grupo a eliminar: "))
                if eliminado is None:
                    print("No se encontró el grupo. ⛔")
                else:
                    print("✅ Grupo eliminado:", eliminado.nombre_grupo)
            case "3":
                encontrado = grupos.buscar_recursivo(validar_input("Grupo a buscar: "))
                if encontrado is None:
                    print("No se encontró el grupo. ⛔")
                else:
                    mostrar_grupo(inscritos, encontrado)
            case "4":
                grupo = grupos.rotar(pedir_entero("Cantidad de rotaciones: ", 0))
                if grupo is None:
                    print("No hay grupos registrados. ⛔")
                else:
                    mostrar_grupo(inscritos, grupo, "===GRUPO ACTUAL===")
            case "5":
                mostrar_grupos(inscritos, grupos)
            case "6":
                grupos.exportar_json(RUTA_GRUPOS)
                print("✅ Archivo JSON exportado en data/grupos.json")
            case "7":
                if archivo_tiene_datos(RUTA_GRUPOS):
                    grupos.importar_json(RUTA_GRUPOS)
                    print("✅ Archivo JSON importado desde data/grupos.json")
                else:
                    print("No hay datos para importar en data/grupos.json. ⛔")
            case "0":
                break


def menu_reportes(inscritos, historial, grupos):
    """Gestiona los reportes consolidados del sistema académico.

    Args:
        inscritos (ListaSimple): Lista simple de estudiantes inscritos.
        historial (ListaDoble): Lista doble con el historial académico.
        grupos (ListaCircular): Lista circular con los grupos registrados.
    """

    while True:
        mostrar_titulo("=== 📊 Módulo Reportes 📊 ===")
        print("1. Top 3 mejores promedios 🏆")
        print("2. Siguiente grupo en turno 🔄")
        print("3. Cantidad de inscritos 👥")
        print("0. Volver ↩️")
        opcion = validar_opcion("Seleccione una opción: ", ["1", "2", "3", "0"])

        match opcion:
            case "1":
                reporte_top_3(historial, inscritos)
            case "2":
                reporte_siguiente_grupo(grupos, inscritos)
            case "3":
                reporte_cantidad_inscritos(inscritos)
            case "0":
                break


def main():
    """Inicializa las estructuras, carga datos y ejecuta el menú principal."""

    inscritos = ListaSimple()
    historial = ListaDoble()
    grupos = ListaCircular()

    cargar_datos(inscritos, historial, grupos)

    while True:
        mostrar_titulo("=== 🏫 Sistema de Registros Académicos 🏫 ===")
        print("1. Inscritos 👥")
        print("2. Historial 📚")
        print("3. Grupos 🔄")
        print("4. Reportes 📊")
        print("5. Salir 🚪")
        opcion = validar_opcion("Seleccione una opción: ", ["1", "2", "3", "4", "5"])

        match opcion:
            case "1":
                menu_inscritos(inscritos)
            case "2":
                menu_historial(historial, inscritos)
            case "3":
                menu_grupos(grupos, inscritos)
            case "4":
                menu_reportes(inscritos, historial, grupos)
            case "5":
                print("Saliendo del sistema... 🚪")
                break


if __name__ == "__main__":
    main()
