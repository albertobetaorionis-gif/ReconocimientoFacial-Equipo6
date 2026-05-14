import json
import os
import cv2
import matplotlib.pyplot as plt


# ==========================================
# CARGAR JSON
# ==========================================
def cargar_json(ruta_relativa):

    base_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    ruta_completa = os.path.join(
        base_dir,
        ruta_relativa
    )

    with open(
        ruta_completa,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# ==========================================
# CALCULAR DIFERENCIA
# ==========================================
def diferencia_promedio(g1, g2):

    grafo1 = g1["grafo_normalizado"]
    grafo2 = g2["grafo_normalizado"]

    total = 0
    contador = 0

    for nodo in grafo1:

        if nodo in grafo2:

            for vecino in grafo1[nodo]:

                if vecino in grafo2[nodo]:

                    total += abs(
                        grafo1[nodo][vecino]
                        -
                        grafo2[nodo][vecino]
                    )

                    contador += 1

    if contador == 0:
        return 0

    return total / contador


# ==========================================
# CALCULAR SIMILITUD
# ==========================================
def calcular_similitud(error):

    return round(
        max(0, 100 - (error * 100)),
        2
    )


# ==========================================
# CARGAR IMAGEN
# ==========================================
def cargar_imagen(ruta):

    imagen = cv2.imread(ruta)

    if imagen is None:

        raise Exception(
            f"No se pudo cargar:\n{ruta}"
        )

    return cv2.cvtColor(
        imagen,
        cv2.COLOR_BGR2RGB
    )


# ==========================================
# DIBUJAR GRAFO
# ==========================================
def dibujar_grafo(
    ax,
    landmarks,
    aristas,
    titulo
):

    puntos = {}

    for punto in landmarks:

        x = punto["x"]
        y = -punto["y"]

        idx = punto["id"]

        puntos[idx] = (x, y)

        ax.scatter(x, y)

        ax.text(
            x,
            y,
            str(idx),
            fontsize=8
        )

    for (a, b) in aristas:

        if a in puntos and b in puntos:

            x1, y1 = puntos[a]
            x2, y2 = puntos[b]

            ax.plot(
                [x1, x2],
                [y1, y2]
            )

    ax.set_title(titulo)

    ax.axis("equal")


# ==========================================
# MOSTRAR PERSONA
# ==========================================
def mostrar_persona(indice):

    comparacion = comparaciones[indice]

    entrada = comparacion["entrada"]
    prueba = comparacion["prueba"]

    # ==============================
    # CARGAR GRAFOS
    # ==============================
    g1 = cargar_json(
        entrada["grafo"]
    )

    g2 = cargar_json(
        prueba["grafo"]
    )

    # ==============================
    # SIMILITUD
    # ==============================
    error = diferencia_promedio(
        g1,
        g2
    )

    similitud = calcular_similitud(
        error
    )

    # ==============================
    # CLASIFICACION
    # ==============================
    if similitud > 90:

        clasificacion = (
            "Muy alta similitud "
            "(posiblemente misma persona)"
        )

    elif similitud >= 75:

        clasificacion = (
            "Similitud media "
            "(caso ambiguo o similar)"
        )

    else:

        clasificacion = (
            "Baja similitud "
            "(probablemente personas distintas)"
        )

    # ==============================
    # LANDMARKS
    # ==============================
    landmarks1 = cargar_json(
        entrada["landmarks"]
    )

    landmarks2 = cargar_json(
        prueba["landmarks"]
    )

    # ==============================
    # IMAGENES
    # ==============================
    img1 = cargar_imagen(
        entrada["imagen"]
    )

    img2 = cargar_imagen(
        prueba["imagen"]
    )

    # ==============================
    # LIMPIAR FIGURA
    # ==============================
    plt.clf()

    # ==============================
    # IMAGEN 1
    # ==============================
    ax1 = plt.subplot(2, 2, 1)

    ax1.imshow(img1)

    ax1.set_title(
        f"Entrada\n{entrada['nombre']}"
    )

    ax1.axis("off")

    # ==============================
    # IMAGEN 2
    # ==============================
    ax2 = plt.subplot(2, 2, 2)

    ax2.imshow(img2)

    ax2.set_title(
        f"Prueba\n{prueba['nombre']}"
    )

    ax2.axis("off")

    # ==============================
    # GRAFO 1
    # ==============================
    ax3 = plt.subplot(2, 2, 3)

    dibujar_grafo(

        ax3,

        landmarks1["landmarks"],

        g1["aristas"],

        "Grafo Entrada"

    )

    # ==============================
    # GRAFO 2
    # ==============================
    ax4 = plt.subplot(2, 2, 4)

    dibujar_grafo(

        ax4,

        landmarks2["landmarks"],

        g2["aristas"],

        "Grafo Prueba"

    )

    # ==============================
    # TITULO
    # ==============================
    plt.suptitle(
        f"{clasificacion}\n"
        f"Similitud: {similitud}%",

        fontsize=16

    )

    # ==============================
    # TEXTO ABAJO
    # ==============================
    fig.text(

        0.5,
        0.02,

        "Presiona A = Anterior | D = Siguiente",

        ha="center",

        fontsize=12,

        fontweight="bold"

    )

    plt.tight_layout(
        rect=[0, 0.05, 1, 0.92]
    )

    plt.draw()


# ==========================================
# EVENTOS TECLADO
# ==========================================
def teclado(event):

    global indice_actual

    # ==============================
    # SIGUIENTE
    # ==============================
    if event.key == "d":

        indice_actual += 1

        if indice_actual >= len(comparaciones):

            indice_actual = 0

        mostrar_persona(
            indice_actual
        )

    # ==============================
    # ANTERIOR
    # ==============================
    elif event.key == "a":

        indice_actual -= 1

        if indice_actual < 0:

            indice_actual = (
                len(comparaciones) - 1
            )

        mostrar_persona(
            indice_actual
        )


# ==========================================
# DATOS
# ==========================================
personas = [

    {
        "nombre": "Alberto Castillo",

        "grafo":
        "Entradas/Grafos/grafoEntradaAlbertoCastillo.json",

        "landmarks":
        "Entradas/Landmarks/landmarkEntradaAlbertoCastillo.json",

        "imagen":
        r"AlbertoCastillo\CaraAlbertoCastillo.jpg"
    },

    {
        "nombre": "Carlos Meza",

        "grafo":
        "Entradas/Grafos/grafoEntradaCarlosMeza.json",

        "landmarks":
        "Entradas/Landmarks/landmarkEntradaCarlosMeza.json",

        "imagen":
        r"CarlosMeza\CaraCarlosMeza.jpg"
    },

    {
        "nombre": "Darío Rabago",

        "grafo":
        "Entradas/Grafos/grafoEntradaDarioRabago.json",

        "landmarks":
        "Entradas/Landmarks/landmarkEntradaDarioRabago.json",

        "imagen":
        r"DarioRabago\CaraDarioRabago.jpg"
    },

    {
        "nombre": "Miguel Núñez",

        "grafo":
        "Entradas/Grafos/grafoEntradaMiguelNunez.json",

        "landmarks":
        "Entradas/Landmarks/landmarkEntradaMiguelNunez.json",

        "imagen":
        r"MiguelNunez\CaraMiguelNunez.jpg"
    }

]


# ==========================================
# GENERAR TODAS LAS COMPARACIONES
# ==========================================
comparaciones = []

for persona1 in personas:

    for persona2 in personas:

        comparaciones.append({

            "entrada": persona1,
            "prueba": persona2

        })


# ==========================================
# INICIO
# ==========================================
indice_actual = 0

fig = plt.figure(
    figsize=(14, 8)
)

fig.canvas.mpl_connect(
    "key_press_event",
    teclado
)

mostrar_persona(
    indice_actual
)

plt.show()