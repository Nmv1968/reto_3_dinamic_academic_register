# Reto 3 - Registros dinamicos academicos

Este proyecto implementa tres estructuras de datos enlazadas en Python para una actividad de Programacion II:

- Lista simple para inscritos
- Lista doble para historial academico
- Lista circular para grupos rotativos

Tambien incluye persistencia en CSV y JSON, un menu en consola, reportes y casos de prueba basicos.

Como referencia visual y de validaciones, se tomo la idea del reto 2 de colas, pero manteniendo las estructuras pedidas para este reto.

## Estructura

```text
/reto_3_registros_dinamicos_academicos_mesias_naim
	/src
		app.py
		casos_prueba.py
		estudiante.py
		lista_circular.py
		lista_doble.py
		lista_simple.py
		nodo_circular.py
		nodo_doble.py
		nodo_simple.py
		persistencia_csv.py
		persistencia_json.py
	/data
		grupos.json
		historial.json
		inscritos.csv
	README.md
```

## Como ejecutar

Desde la carpeta raiz del proyecto:

```bash
.venv/bin/python src/app.py
```

Para correr los casos de prueba:

```bash
.venv/bin/python src/casos_prueba.py
```

## Funcionalidades

### Lista simple

- Insertar al final
- Buscar por id
- Eliminar por id
- Recorrer la lista
- Exportar e importar en CSV
- Cada inscrito se maneja con un objeto `Estudiante`
- El ID del inscrito se genera automaticamente con UUID, parecido al reto 2

### Lista doble

- Insertar ordenado por `(anio, term)`
- Buscar un semestre
- Eliminar un semestre
- Recorrer hacia adelante
- Recorrer hacia atras
- Exportar e importar en JSON

### Lista circular

- Insertar grupos
- Buscar con recursividad
- Eliminar un grupo
- Rotar `k` posiciones
- Recorrer la lista
- Exportar e importar en JSON

### Reportes

- Top 3 mejores promedios por semestre
- Siguiente grupo en turno
- Cantidad de inscritos

## Complejidad

- Insercion en lista simple: O(n)
- Busqueda en lista simple: O(n)
- Eliminacion en lista simple: O(n)
- Recorrido en lista simple: O(n)
- Insercion ordenada en lista doble: O(n)
- Busqueda en lista doble: O(n)
- Eliminacion en lista doble: O(n)
- Recorrido adelante y atras: O(n)
- Insercion en lista circular: O(n)
- Busqueda recursiva en lista circular: O(n)
- Eliminacion en lista circular: O(n)
- Recorrido en lista circular: O(n)
- Rotacion en lista circular: O(k)

## Archivos de datos

- `data/inscritos.csv` guarda los inscritos
- `data/historial.json` guarda el historial academico
- `data/grupos.json` guarda los grupos rotativos

## Nota

El codigo se hizo con un estilo sencillo y directo, pensado para una actividad academica de estructuras de datos.

La interfaz de consola usa encabezados visuales, mensajes de error simples y validaciones reutilizables para mantener una presentacion parecida a la del reto 2.
