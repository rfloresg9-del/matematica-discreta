
import tkinter as tk
import math

# =====================================
# ARBOL AVL BALANCEADO
# =====================================

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None
        self.altura = 1


def altura(nodo):
    if nodo is None:
        return 0
    return nodo.altura


def factor_balance(nodo):
    if nodo is None:
        return 0
    return altura(nodo.izquierda) - altura(nodo.derecha)


def actualizar_altura(nodo):
    nodo.altura = 1 + max(
        altura(nodo.izquierda),
        altura(nodo.derecha)
    )


# ROTACION SIMPLE A LA DERECHA
def rotacion_derecha(y):
    x = y.izquierda
    temporal = x.derecha

    x.derecha = y
    y.izquierda = temporal

    actualizar_altura(y)
    actualizar_altura(x)

    print("Rotacion simple a la derecha")
    return x


# ROTACION SIMPLE A LA IZQUIERDA
def rotacion_izquierda(x):
    y = x.derecha
    temporal = y.izquierda

    y.izquierda = x
    x.derecha = temporal

    actualizar_altura(x)
    actualizar_altura(y)

    print("Rotacion simple a la izquierda")
    return y


# INSERTAR NUMEROS Y BALANCEAR
def insertar(raiz, valor):
    if raiz is None:
        return Nodo(valor)

    if valor < raiz.valor:
        raiz.izquierda = insertar(raiz.izquierda, valor)
    elif valor > raiz.valor:
        raiz.derecha = insertar(raiz.derecha, valor)
    else:
        return raiz

    actualizar_altura(raiz)

    balance = factor_balance(raiz)

    # Caso izquierda-izquierda
    if balance > 1 and valor < raiz.izquierda.valor:
        return rotacion_derecha(raiz)

    # Caso derecha-derecha
    if balance < -1 and valor > raiz.derecha.valor:
        return rotacion_izquierda(raiz)

    # Caso izquierda-derecha
    if balance > 1 and valor > raiz.izquierda.valor:
        print("Rotacion doble izquierda-derecha")
        raiz.izquierda = rotacion_izquierda(raiz.izquierda)
        return rotacion_derecha(raiz)

    # Caso derecha-izquierda
    if balance < -1 and valor < raiz.derecha.valor:
        print("Rotacion doble derecha-izquierda")
        raiz.derecha = rotacion_derecha(raiz.derecha)
        return rotacion_izquierda(raiz)

    return raiz


# =====================================
# RECORRIDOS DEL ARBOL
# =====================================

def preorden(raiz):
    if raiz is None:
        return []

    return (
        [raiz.valor]
        + preorden(raiz.izquierda)
        + preorden(raiz.derecha)
    )


def inorden(raiz):
    if raiz is None:
        return []

    return (
        inorden(raiz.izquierda)
        + [raiz.valor]
        + inorden(raiz.derecha)
    )


def postorden(raiz):
    if raiz is None:
        return []

    return (
        postorden(raiz.izquierda)
        + postorden(raiz.derecha)
        + [raiz.valor]
    )


# =====================================
# DIBUJAR ARBOL AVL
# =====================================

def dibujar_arbol(raiz):
    ventana = tk.Tk()
    ventana.title("Arbol AVL Balanceado")
    ventana.geometry("950x650")
    ventana.configure(bg="white")

    tk.Label(
        ventana,
        text="ARBOL AVL BALANCEADO",
        font=("Arial", 18, "bold"),
        bg="white",
        fg="#174a7e"
    ).pack(pady=10)

    lienzo = tk.Canvas(
        ventana,
        bg="white",
        width=900,
        height=440
    )
    lienzo.pack(fill="both", expand=True)

    def dibujar(nodo, x, y, separacion):
        if nodo is None:
            return

        siguiente = separacion / 2

        if nodo.izquierda:
            nx = x - separacion
            ny = y + 75

            lienzo.create_line(
                x, y, nx, ny,
                fill="#555555",
                width=2
            )

            dibujar(nodo.izquierda, nx, ny, siguiente)

        if nodo.derecha:
            nx = x + separacion
            ny = y + 75

            lienzo.create_line(
                x, y, nx, ny,
                fill="#555555",
                width=2
            )

            dibujar(nodo.derecha, nx, ny, siguiente)

        lienzo.create_oval(
            x-22, y-22,
            x+22, y+22,
            fill="#a9d6ff",
            outline="#175fa5",
            width=2
        )

        lienzo.create_text(
            x, y,
            text=str(nodo.valor),
            font=("Arial", 12, "bold")
        )

    def actualizar(event=None):
        lienzo.delete("all")
        ancho = lienzo.winfo_width()
        dibujar(raiz, ancho / 2, 40, ancho / 4)

    lienzo.bind("<Configure>", actualizar)

    texto = (
        "PREORDEN: "
        + ", ".join(map(str, preorden(raiz)))
        + "\nINORDEN: "
        + ", ".join(map(str, inorden(raiz)))
        + "\nPOSTORDEN: "
        + ", ".join(map(str, postorden(raiz)))
    )

    tk.Label(
        ventana,
        text=texto,
        font=("Arial", 11),
        bg="white",
        justify="left",
        wraplength=850
    ).pack(pady=15)

    tk.Button(
        ventana,
        text="Cerrar ventana",
        command=ventana.destroy
    ).pack(pady=10)

    ventana.mainloop()


def opcion_arbol():
    print("\n===== CREAR ARBOL AVL =====")

    try:
        entrada = input(
            "Ingrese numeros separados por comas: "
        )

        numeros = [
            int(x.strip())
            for x in entrada.split(",")
        ]

        if len(numeros) != len(set(numeros)):
            print("No se permiten numeros repetidos.")
            return

        raiz = None

        for numero in numeros:
            print("\nInsertando:", numero)
            raiz = insertar(raiz, numero)

        print("\nARBOL AVL CREADO CORRECTAMENTE")
        print("Preorden:", preorden(raiz))
        print("Inorden:", inorden(raiz))
        print("Postorden:", postorden(raiz))

        dibujar_arbol(raiz)

    except ValueError:
        print("Error: ingrese numeros enteros.")


# =====================================
# TRAYECTORIA HAMILTONIANA
# =====================================

def buscar_hamiltoniana(grafo):
    vertices = list(grafo.keys())

    def explorar(actual, camino, visitados):
        if len(camino) == len(vertices):
            return camino.copy()

        for vecino in grafo[actual]:
            if vecino not in visitados:
                visitados.add(vecino)
                camino.append(vecino)

                resultado = explorar(
                    vecino, camino, visitados
                )

                if resultado is not None:
                    return resultado

                camino.pop()
                visitados.remove(vecino)

        return None

    for inicio in vertices:
        resultado = explorar(
            inicio, [inicio], {inicio}
        )

        if resultado is not None:
            return resultado

    return None


# =====================================
# DIBUJAR GRAFO
# =====================================

def dibujar_grafo(grafo, trayectoria):
    ventana = tk.Tk()
    ventana.title("Trayectoria Hamiltoniana")
    ventana.geometry("850x650")
    ventana.configure(bg="white")

    tk.Label(
        ventana,
        text="TRAYECTORIA HAMILTONIANA",
        font=("Arial", 18, "bold"),
        bg="white",
        fg="#174a7e"
    ).pack(pady=15)

    lienzo = tk.Canvas(
        ventana,
        width=800,
        height=450,
        bg="white"
    )
    lienzo.pack(fill="both", expand=True)

    vertices = list(grafo.keys())
    cantidad = len(vertices)
    posiciones = {}

    for i, vertice in enumerate(vertices):
        angulo = 2 * math.pi * i / cantidad

        x = 400 + 170 * math.cos(angulo)
        y = 220 + 170 * math.sin(angulo)

        posiciones[vertice] = (x, y)

    conexiones_camino = set()

    if trayectoria is not None:
        for i in range(len(trayectoria) - 1):
            a = trayectoria[i]
            b = trayectoria[i + 1]

            conexiones_camino.add(
                frozenset((a, b))
            )

    for a in grafo:
        for b in grafo[a]:
            if a < b:
                x1, y1 = posiciones[a]
                x2, y2 = posiciones[b]

                es_camino = (
                    frozenset((a, b))
                    in conexiones_camino
                )

                color = (
                    "#16a34a" if es_camino
                    else "#999999"
                )

                grosor = 4 if es_camino else 2

                lienzo.create_line(
                    x1, y1, x2, y2,
                    fill=color,
                    width=grosor
                )

    for vertice, (x, y) in posiciones.items():
        lienzo.create_oval(
            x-23, y-23,
            x+23, y+23,
            fill="#b9e6ff",
            outline="#175fa5",
            width=2
        )

        lienzo.create_text(
            x, y,
            text=vertice,
            font=("Arial", 15, "bold")
        )

    if trayectoria is not None:
        mensaje = (
            "SI EXISTE TRAYECTORIA HAMILTONIANA\n"
            + " -> ".join(trayectoria)
        )
        color = "green"
    else:
        mensaje = "NO EXISTE TRAYECTORIA HAMILTONIANA"
        color = "red"

    tk.Label(
        ventana,
        text=mensaje,
        font=("Arial", 13, "bold"),
        fg=color,
        bg="white"
    ).pack(pady=15)

    tk.Button(
        ventana,
        text="Cerrar ventana",
        command=ventana.destroy
    ).pack(pady=10)

    ventana.mainloop()


def opcion_hamiltoniana():
    print("\n===== TRAYECTORIA HAMILTONIANA =====")

    try:
        cantidad = int(input(
            "Cantidad de vertices (1 a 10): "
        ))

        if cantidad < 1 or cantidad > 10:
            print("Ingrese entre 1 y 10 vertices.")
            return

        vertices = [
            chr(65 + i)
            for i in range(cantidad)
        ]

        grafo = {v: [] for v in vertices}

        print("\nVertices:", ", ".join(vertices))
        print("Ingrese conexiones como A,B")
        print("Escriba FIN para terminar.")

        while True:
            entrada = input(
                "Conexion: "
            ).strip().upper()

            if entrada == "FIN":
                break

            partes = [
                x.strip()
                for x in entrada.split(",")
            ]

            if len(partes) != 2:
                print("Formato incorrecto.")
                continue

            a, b = partes

            if a not in grafo or b not in grafo:
                print("Vertice no valido.")
                continue

            if a == b:
                print("No se permiten lazos.")
                continue

            if b not in grafo[a]:
                grafo[a].append(b)
                grafo[b].append(a)
                print("Conexion agregada.")
            else:
                print("Conexion repetida.")

        print("\nGRAFO CREADO:")
        for v in grafo:
            print(v, "->", ", ".join(grafo[v]))

        trayectoria = buscar_hamiltoniana(grafo)

        if trayectoria is not None:
            print("\nTrayectoria encontrada:")
            print(" -> ".join(trayectoria))
        else:
            print("\nNo existe trayectoria hamiltoniana.")

        dibujar_grafo(grafo, trayectoria)

    except ValueError:
        print("Error: ingrese un numero valido.")


# =====================================
# MENU PRINCIPAL
# =====================================

def menu():
    while True:
        print("\n========================================")
        print("      PROYECTO MATEMATICA DISCRETA")
        print("========================================")
        print("1. Crear arbol AVL balanceado y recorridos")
        print("2. Trayectoria hamiltoniana")
        print("3. Salir")
        print("========================================")

        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            opcion_arbol()

        elif opcion == "2":
            opcion_hamiltoniana()

        elif opcion == "3":
            print("Gracias por utilizar el programa.")
            break

        else:
            print("Opcion incorrecta.")


if __name__ == "__main__":
    menu()
