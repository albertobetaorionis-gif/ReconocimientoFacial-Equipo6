from PIL import Image, ImageTk
import tkinter as tk
import json
import math


class AnalizadorImagen:

    def __init__(self, ruta_imagen):
        self.ruta_imagen = ruta_imagen
        self.width = 0
        self.height = 0
        self.landmarks = []

    def cargar_dimensiones(self):
        img = Image.open(self.ruta_imagen)
        self.width, self.height = img.size

    def agregar_landmark(self, x, y):
        self.landmarks.append((x, y))

    # ==========================
    # CARACTERÍSTICAS GEOMÉTRICAS
    # ==========================

    def calcular_caracteristicas(self):

        if len(self.landmarks) == 0:
            return {}

        suma_x = sum(p[0] for p in self.landmarks)
        suma_y = sum(p[1] for p in self.landmarks)

        centro_x = suma_x / len(self.landmarks)
        centro_y = suma_y / len(self.landmarks)

        distancias = []
        for (x, y) in self.landmarks:
            d = math.sqrt((x - centro_x) ** 2 + (y - centro_y) ** 2)
            distancias.append(d)

        return {
            "total_puntos": len(self.landmarks),
            "centroide": {"x": centro_x, "y": centro_y},
            "distancia_promedio": sum(distancias) / len(distancias),
            "distancia_maxima": max(distancias),
            "vector_distancias": distancias
        }

    def guardar_json(self):

        datos = {
            "width": self.width,
            "height": self.height,
            "landmarks": [
                {"id": i + 1, "x": p[0], "y": p[1]}
                for i, p in enumerate(self.landmarks)
            ],
            "caracteristicas": self.calcular_caracteristicas()
        }

        with open("landmark.json", "w") as f:
            json.dump(datos, f, indent=4)

        print("✅ landmark.json generado automáticamente.")


# ==========================
# INTERFAZ CON SCROLL
# ==========================

def mostrar_ventana():

    ruta = "MezaEsquer/PruebaMezaEsquer.jpg"
    analizador = AnalizadorImagen(ruta)
    analizador.cargar_dimensiones()

    ventana = tk.Tk()
    ventana.title("Landmarks con Scroll")

    frame = tk.Frame(ventana)
    frame.pack(fill=tk.BOTH, expand=True)

    # Scrollbars
    scroll_y = tk.Scrollbar(frame, orient=tk.VERTICAL)
    scroll_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL)

    canvas = tk.Canvas(
        frame,
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    scroll_y.config(command=canvas.yview)
    scroll_x.config(command=canvas.xview)

    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    img = Image.open(ruta)
    img_tk = ImageTk.PhotoImage(img)

    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

    canvas.config(scrollregion=(0, 0, img.width, img.height))

    contador = {"valor": 0}

    def marcar_punto(event):

        # Ajustar coordenadas al scroll
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)

        analizador.agregar_landmark(x, y)

        contador["valor"] += 1
        numero = contador["valor"]

        canvas.create_oval(x-5, y-5, x+5, y+5, fill="red")
        canvas.create_text(x+10, y-10,
                           text=str(numero),
                           fill="yellow",
                           font=("Arial", 12, "bold"))

    canvas.bind("<Button-1>", marcar_punto)

    def al_cerrar():
        analizador.guardar_json()
        ventana.destroy()

    ventana.protocol("WM_DELETE_WINDOW", al_cerrar)

    ventana.mainloop()


if __name__ == "__main__":
    mostrar_ventana()