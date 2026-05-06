import csv

from estudiante import Estudiante


CAMPOS_INSCRITOS = ("id", "ci_estudiante", "nombres", "correo")


def exportar_inscritos_csv(lista, ruta):
	with open(ruta, "w", newline="", encoding="utf-8") as archivo:
		escritor = csv.DictWriter(archivo, fieldnames=CAMPOS_INSCRITOS)
		escritor.writeheader()
		for inscrito in lista.recorrer():
			escritor.writerow(inscrito.to_dict())


def importar_inscritos_csv(ruta, lista=None):
	from lista_simple import ListaSimple

	destino = lista if lista is not None else ListaSimple()
	destino.limpiar()

	with open(ruta, "r", newline="", encoding="utf-8") as archivo:
		lector = csv.DictReader(archivo)
		for fila in lector:
			destino.insertar_final(Estudiante.desde_dict(fila))

	return destino
