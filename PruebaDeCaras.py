import json
import os
import cv2
import numpy as np

# ================================
# Cargar grafo
# ================================
def cargar_grafo(ruta_relativa):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_completa = os.path.join(base_dir, ruta_relativa)

    if not os.path.exists(ruta_completa):
        raise FileNotFoundError(f"No se encontró:\n{ruta_completa}")

    with open(ruta_completa, "r", encoding="utf-8") as f:
        return json.load(f)


# ================================
# Verificar estructura
# ================================
def misma_estructura(g1, g2):
    aristas1 = sorted([sorted(a) for a in g1["aristas"]])
    aristas2 = sorted([sorted(a) for a in g2["aristas"]])
    return aristas1 == aristas2


# ================================
# Diferencia promedio
# ================================
def diferencia_promedio(g1, g2):
    grafo1 = g1["grafo_normalizado"]
    grafo2 = g2["grafo_normalizado"]

    total = 0
    contador = 0

    for nodo in grafo1:
        if nodo in grafo2:
            for vecino in grafo1[nodo]:
                if vecino in grafo2[nodo]:
                    total += abs(grafo1[nodo][vecino] - grafo2[nodo][vecino])
                    contador += 1

    if contador == 0:
        return float("inf")

    return total / contador


# ================================
# Comparación
# ================================
def comparar_grafos(ruta1, ruta2, umbral):
    g1 = cargar_grafo(ruta1)
    g2 = cargar_grafo(ruta2)

    if not misma_estructura(g1, g2):
        return False

    error = diferencia_promedio(g1, g2)
    return error < umbral


# ================================
# Dibujar resultado en imagen
# ================================
from PIL import Image, ImageDraw, ImageFont


def dibujar_resultado(imagen, nombre, reconocido):
    alto, ancho = imagen.shape[:2]

    if reconocido:
        color = (0, 255, 0)  # Verde
        texto = nombre
    else:
        color = (0, 0, 255)  # Rojo
        texto = "Desconocido"

    # Dibujar rectángulo con OpenCV
    cv2.rectangle(imagen, (20, 20), (ancho - 20, alto - 20), color, 3)

    # Convertir imagen OpenCV (BGR) → PIL (RGB)
    imagen_pil = Image.fromarray(cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(imagen_pil)

    # Cargar fuente
    try:
        font = ImageFont.truetype("arial.ttf", 32)
    except:
        font = ImageFont.load_default()

    # Fondo del texto
    text_width, text_height = draw.textbbox((0, 0), texto, font=font)[2:]
    draw.rectangle(
        [(20, alto - 70), (20 + text_width + 20, alto - 20)],
        fill=color
    )

    # Dibujar texto (blanco)
    draw.text(
        (30, alto - 60),
        texto,
        font=font,
        fill=(255, 255, 255)
    )

    # Convertir de vuelta a OpenCV (RGB → BGR)
    imagen_final = cv2.cvtColor(np.array(imagen_pil), cv2.COLOR_RGB2BGR)

    return imagen_final


# ================================
# PROGRAMA PRINCIPAL
# ================================
if __name__ == "__main__":

    umbral = 0.1

    personas = [
        {
            "nombre": "Alberto Castillo",
            "entrada": "Entradas/Grafos/grafoEntradaAlbertoCastillo.json",
            "prueba": "Pruebas/Grafos/grafoPruebaAlbertoCastillo.json",
            "imagen": "AlbertoCastillo/PruebaAlbertoCastillo.jpg"
        },
        {
            "nombre": "Andrés Meza",
            "entrada": "Entradas/Grafos/grafoEntradaMezaEsquer.json",
            "prueba": "Pruebas/Grafos/grafoPruebaMezaEsquer.json",
            "imagen": "MezaEsquer/PruebaMezaEsquer.jpg"
        },
        {
            "nombre": "Miguel Núñez",
            "entrada": "Entradas/Grafos/grafoEntradaMiguelNunez.json",
            "prueba": "Pruebas/Grafos/grafoPruebaMiguelNunez.json",
            "imagen": "MiguelNunez/PruebaMiguelNunez.jpg"
        },
        {
            "nombre": "Dario Rábago",
            "entrada": "Entradas/Grafos/grafoEntradaDarioRabago.json",
            "prueba": "Pruebas/Grafos/grafoPruebaDarioRabago.json",
            "imagen": "DarioRabago/PruebaDarioRabago.jpg"
        }
    ]

    imagenes = []

    for persona in personas:

        reconocido = comparar_grafos(
            persona["entrada"],
            persona["prueba"],
            umbral
        )

        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_imagen = os.path.join(base_dir, persona["imagen"])

        img = cv2.imread(ruta_imagen)

        if img is None:
            print("No se pudo cargar imagen:", ruta_imagen)
            continue

        img = cv2.resize(img, (400, 400))
        img = dibujar_resultado(img, persona["nombre"], reconocido)

        imagenes.append(img)

    # Unir imágenes en cuadrícula 2x2
    fila1 = np.hstack((imagenes[0], imagenes[1]))
    fila2 = np.hstack((imagenes[2], imagenes[3]))
    pantalla = np.vstack((fila1, fila2))

    cv2.imshow("Sistema de Reconocimiento Facial", pantalla)
    cv2.waitKey(0)
    cv2.destroyAllWindows()