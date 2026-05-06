import os

from estudiante import Estudiante
from lista_circular import ListaCircular
from lista_doble import ListaDoble
from lista_simple import ListaSimple


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RUTA_INSCRITOS = os.path.join(DATA_DIR, "inscritos.csv")
RUTA_HISTORIAL = os.path.join(DATA_DIR, "historial.json")
RUTA_GRUPOS = os.path.join(DATA_DIR, "grupos.json")


def mostrar_titulo(titulo):
    print("\n" + titulo)
    print("=" * len(titulo))


def archivo_tiene_datos(ruta):
    return os.path.exists(ruta) and os.path.getsize(ruta) > 0


def validar_input(mensaje):
    while True:
        texto = input(mensaje)
        if texto.strip() != "":
            return texto.strip()
        print("Entrada no válida. Ingrese un valor no vacío. ⛔")


def validar_opcion(mensaje, opciones_validas):
    while True:
        opcion = validar_input(mensaje)
        if opcion in opciones_validas:
            return opcion
        print("Opción no válida. Intente nuevamente. ⛔")


def pedir_entero(mensaje, minimo=None, maximo=None):
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
    if archivo_tiene_datos(RUTA_INSCRITOS):
        inscritos.importar_csv(RUTA_INSCRITOS)
    if archivo_tiene_datos(RUTA_HISTORIAL):
        historial.importar_json(RUTA_HISTORIAL)
    if archivo_tiene_datos(RUTA_GRUPOS):
        grupos.importar_json(RUTA_GRUPOS)


def mostrar_inscritos(inscritos):
    datos = inscritos.recorrer()
    if len(datos) == 0:
        print("No hay inscritos registrados. ⛔")
        return

    for inscrito in datos:
        print(
            "ID:",
            inscrito.id_estudiante,
            "| CI:",
            inscrito.ci_estudiante,
            "| Nombre:",
            inscrito.nombres,
            "| Correo:",
            inscrito.correo,
        )


def mostrar_historial(historial, hacia_atras=False):
    if hacia_atras:
        datos = historial.recorrer_atras()
    else:
        datos = historial.recorrer_adelante()

    if len(datos) == 0:
        print("No hay semestres registrados. ⛔")
        return

    for semestre in datos:
        print("Año:", semestre["anio"], "| Término:", semestre["term"])
        materias = semestre.get("materias", [])
        if len(materias) == 0:
            print("  Sin materias registradas")
        else:
            for materia in materias:
                print(
                    "  -",
                    materia["cod"],
                    materia["nombre"],
                    "Nota:",
                    materia["nota"],
                )


def mostrar_grupos(grupos):
    datos = grupos.recorrer()
    if len(datos) == 0:
        print("No hay grupos registrados. ⛔")
        return

    for grupo in datos:
        print(
            "Grupo:",
            grupo["nombre_grupo"],
            "| Tutor:",
            grupo["tutor"],
            "| Tema:",
            grupo["tema"],
        )


def pedir_semestre():
    anio = pedir_entero("Ingrese el año: ", 2000, 2100)
    term = pedir_entero("Ingrese el término: ", 1, 2)
    cantidad = pedir_entero("¿Cuántas materias desea agregar?: ", 1)
    materias = []

    contador = 0
    while contador < cantidad:
        print("Materia", contador + 1)
        cod = validar_input("Código: ")
        nombre = validar_input("Nombre: ")
        nota = pedir_flotante("Nota: ", 0, 5)
        materias.append({"cod": cod, "nombre": nombre, "nota": nota})
        contador += 1

    return {"anio": anio, "term": term, "materias": materias}


def promedio_semestre(semestre):
    materias = semestre.get("materias", [])
    if len(materias) == 0:
        return 0

    suma = 0
    for materia in materias:
        suma += materia["nota"]
    return suma / len(materias)


def reporte_top_3(historial):
    semestres = historial.recorrer_adelante()
    if len(semestres) == 0:
        print("No hay historial para calcular promedios. ⛔")
        return

    datos = []
    for semestre in semestres:
        datos.append(
            {
                "anio": semestre["anio"],
                "term": semestre["term"],
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

    print("Top de promedios:")
    indice = 0
    while indice < tope:
        item = datos[indice]
        print(
            indice + 1,
            ". Año:",
            item["anio"],
            "Término:",
            item["term"],
            "Promedio:",
            round(item["promedio"], 2),
            sep="",
        )
        indice += 1


def reporte_siguiente_grupo(grupos):
    grupo = grupos.rotar(1)
    if grupo is None:
        print("No hay grupos registrados. ⛔")
        return
    print(
        "Siguiente grupo en turno:",
        grupo["nombre_grupo"],
        "| Tutor:",
        grupo["tutor"],
        "| Tema:",
        grupo["tema"],
    )


def reporte_cantidad_inscritos(inscritos):
    print("Cantidad de inscritos:", inscritos.contar())


def crear_estudiante():
    nombres = validar_input("Ingrese los nombres del estudiante: ")
    correo = validar_correo("Ingrese el correo del estudiante: ")
    ci_estudiante = validar_ci("Ingrese la cédula del estudiante: ")
    return Estudiante(nombres, correo, ci_estudiante)


def menu_inscritos(inscritos):
    while True:
        mostrar_titulo("=== 👥 Módulo Inscritos 👥 ===")
        print("1. Agregar estudiante ➕")
        print("2. Eliminar estudiante 🗑️")
        print("3. Buscar estudiante 🔎")
        print("4. Mostrar inscritos 📋")
        print("5. Exportar CSV 💾")
        print("6. Importar CSV 📥")
        print("0. Volver ↩️")
        opcion = validar_opcion("Seleccione una opción: ", ["1", "2", "3", "4", "5", "6", "0"])

        if opcion == "1":
            estudiante = crear_estudiante()
            inscritos.insertar_final(estudiante)
            print(
                f"✅ Estudiante agregado con ID: {estudiante.id_estudiante} "
                f"y CI: {estudiante.ci_estudiante}"
            )
        elif opcion == "2":
            eliminado = inscritos.eliminar(validar_input("ID a eliminar: "))
            if eliminado is None:
                print("No se encontró el inscrito. ⛔")
            else:
                print("✅ Inscrito eliminado:", eliminado.nombres)
        elif opcion == "3":
            encontrado = inscritos.buscar(validar_input("ID a buscar: "))
            if encontrado is None:
                print("No se encontró el inscrito. ⛔")
            else:
                print(encontrado)
        elif opcion == "4":
            mostrar_inscritos(inscritos)
        elif opcion == "5":
            inscritos.exportar_csv(RUTA_INSCRITOS)
            print("✅ Archivo CSV exportado en data/inscritos.csv")
        elif opcion == "6":
            if archivo_tiene_datos(RUTA_INSCRITOS):
                inscritos.importar_csv(RUTA_INSCRITOS)
                print("✅ Archivo CSV importado desde data/inscritos.csv")
            else:
                print("No hay datos para importar en data/inscritos.csv. ⛔")
        elif opcion == "0":
            break
        else:
            print("Opción inválida. ⛔")


def menu_historial(historial):
    while True:
        mostrar_titulo("=== 📚 Módulo Historial Académico 📚 ===")
        print("1. Agregar semestre ➕")
        print("2. Eliminar semestre 🗑️")
        print("3. Buscar semestre 🔎")
        print("4. Recorrer adelante ▶️")
        print("5. Recorrer atrás ◀️")
        print("6. Exportar JSON 💾")
        print("7. Importar JSON 📥")
        print("0. Volver ↩️")
        opcion = validar_opcion("Seleccione una opción: ", ["1", "2", "3", "4", "5", "6", "7", "0"])

        if opcion == "1":
            historial.insertar_ordenado(pedir_semestre())
            print("✅ Semestre agregado.")
        elif opcion == "2":
            anio = pedir_entero("Año a eliminar: ", 2000, 2100)
            term = pedir_entero("Término a eliminar: ", 1, 2)
            eliminado = historial.eliminar(anio, term)
            if eliminado is None:
                print("No se encontró el semestre. ⛔")
            else:
                print("✅ Semestre eliminado.")
        elif opcion == "3":
            anio = pedir_entero("Año a buscar: ", 2000, 2100)
            term = pedir_entero("Término a buscar: ", 1, 2)
            encontrado = historial.buscar(anio, term)
            if encontrado is None:
                print("No se encontró el semestre. ⛔")
            else:
                print(encontrado)
        elif opcion == "4":
            mostrar_historial(historial, False)
        elif opcion == "5":
            mostrar_historial(historial, True)
        elif opcion == "6":
            historial.exportar_json(RUTA_HISTORIAL)
            print("✅ Archivo JSON exportado en data/historial.json")
        elif opcion == "7":
            if archivo_tiene_datos(RUTA_HISTORIAL):
                historial.importar_json(RUTA_HISTORIAL)
                print("✅ Archivo JSON importado desde data/historial.json")
            else:
                print("No hay datos para importar en data/historial.json. ⛔")
        elif opcion == "0":
            break
        else:
            print("Opción inválida. ⛔")


def menu_grupos(grupos):
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
        opcion = validar_opcion("Seleccione una opción: ", ["1", "2", "3", "4", "5", "6", "7", "0"])

        if opcion == "1":
            grupo = {
                "nombre_grupo": validar_input("Nombre del grupo: "),
                "tutor": validar_input("Tutor: "),
                "tema": validar_input("Tema: "),
            }
            grupos.insertar(grupo)
            print("✅ Grupo agregado.")
        elif opcion == "2":
            eliminado = grupos.eliminar(validar_input("Grupo a eliminar: "))
            if eliminado is None:
                print("No se encontró el grupo. ⛔")
            else:
                print("✅ Grupo eliminado:", eliminado["nombre_grupo"])
        elif opcion == "3":
            encontrado = grupos.buscar_recursivo(validar_input("Grupo a buscar: "))
            if encontrado is None:
                print("No se encontró el grupo. ⛔")
            else:
                print(encontrado)
        elif opcion == "4":
            grupo = grupos.rotar(pedir_entero("Cantidad de rotaciones: ", 0))
            if grupo is None:
                print("No hay grupos registrados. ⛔")
            else:
                print("✅ Grupo actual:", grupo["nombre_grupo"])
        elif opcion == "5":
            mostrar_grupos(grupos)
        elif opcion == "6":
            grupos.exportar_json(RUTA_GRUPOS)
            print("✅ Archivo JSON exportado en data/grupos.json")
        elif opcion == "7":
            if archivo_tiene_datos(RUTA_GRUPOS):
                grupos.importar_json(RUTA_GRUPOS)
                print("✅ Archivo JSON importado desde data/grupos.json")
            else:
                print("No hay datos para importar en data/grupos.json. ⛔")
        elif opcion == "0":
            break
        else:
            print("Opción inválida. ⛔")


def menu_reportes(inscritos, historial, grupos):
    while True:
        mostrar_titulo("=== 📊 Módulo Reportes 📊 ===")
        print("1. Top 3 mejores promedios 🏆")
        print("2. Siguiente grupo en turno 🔄")
        print("3. Cantidad de inscritos 👥")
        print("0. Volver ↩️")
        opcion = validar_opcion("Seleccione una opción: ", ["1", "2", "3", "0"])

        if opcion == "1":
            reporte_top_3(historial)
        elif opcion == "2":
            reporte_siguiente_grupo(grupos)
        elif opcion == "3":
            reporte_cantidad_inscritos(inscritos)
        elif opcion == "0":
            break
        else:
            print("Opción inválida. ⛔")


def main():
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

        if opcion == "1":
            menu_inscritos(inscritos)
        elif opcion == "2":
            menu_historial(historial)
        elif opcion == "3":
            menu_grupos(grupos)
        elif opcion == "4":
            menu_reportes(inscritos, historial, grupos)
        elif opcion == "5":
            print("Saliendo del sistema... 🚪")
            break
        else:
            print("Opción inválida. ⛔")


if __name__ == "__main__":
    main()
    