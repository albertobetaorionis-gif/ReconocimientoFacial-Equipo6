import json
import math


def distancia(p1, p2):
    return math.sqrt(
        (p2["x"] - p1["x"])**2 +
        (p2["y"] - p1["y"])**2
    )


def construir_grafo_estructural(ruta_json):

    with open(ruta_json, "r") as f:
        datos = json.load(f)

    landmarks = datos["landmarks"]

    # Convertir a diccionario rápido por id
    puntos = {p["id"]: p for p in landmarks}

    # -------------------------
    # Aristas definidas por ti
    # -------------------------

    aristas = [
        (1,2),(1,3),(2,4),(3,9),(4,10),
        (5,6),(7,8),
        (1,14),(14,11),(12,13),
        (14,15),(2,15),
        (16,17),(15,18),
        (9,19),(19,20),(20,21),
        (21,22),(22,23),(10,23),
        (19,24),(24,25),(25,27),
        (27,28),(23,28),
        (24,30),(28,30),
        (26,29),(29,30)
    ]

    # -------------------------
    # Unidad base = distancia 1-2
    # -------------------------

    unidad = distancia(puntos[1], puntos[2])

    print("Unidad base (1-2) =", unidad)

    # -------------------------
    # Construir grafo ponderado
    # -------------------------

    grafo = {}

    for (a, b) in aristas:

        d_real = distancia(puntos[a], puntos[b])
        d_norm = d_real / unidad

        # Grafo no dirigido
        grafo.setdefault(a, {})
        grafo.setdefault(b, {})

        grafo[a][b] = d_norm
        grafo[b][a] = d_norm

    # -------------------------
    # Guardar resultado
    # -------------------------

    salida = {
        "unidad_base_1_2": unidad,
        "aristas": aristas,
        "grafo_normalizado": grafo
    }

    with open("grafo_estructural.json", "w") as f:
        json.dump(salida, f, indent=4)

    print("✅ grafo_estructural.json creado correctamente.")


if __name__ == "__main__":
    construir_grafo_estructural("landmark.json")