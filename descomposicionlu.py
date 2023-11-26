import numpy as np
import tkinter as tk
from tkinter import Label, Entry, Button, messagebox, scrolledtext

def lu_decomposition(matrix):
    n = len(matrix)
    lower = np.zeros((n, n))
    upper = np.zeros((n, n))
    steps = []

    for i in range(n):
        lower[i, i] = 1
        step = {"i": i + 1, "L": np.copy(lower), "U": np.copy(upper)}

        for j in range(i, n):
            sum_val = sum(lower[i, k] * upper[k, j] for k in range(i))
            upper[i, j] = matrix[i, j] - sum_val

        step["U"] = np.copy(upper)
        steps.append(step)

        for j in range(i + 1, n):
            sum_val = sum(lower[j, k] * upper[k, i] for k in range(i))
            lower[j, i] = (matrix[j, i] - sum_val) / upper[i, i]

        step["L"] = np.copy(lower)
        steps.append(step)

    return lower, upper, steps

def solve_lu_system(lower, upper, b):
    n = len(b)
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - sum(lower[i, k] * y[k] for k in range(i))

    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(upper[i, k] * x[k] for k in range(i + 1, n))) / upper[i, i]

    return x

def solve_linear_system():
    try:
        size = int(entry_size.get())
        A = np.zeros((size, size))

        for i in range(size):
            for j in range(size):
                A[i, j] = float(entry_A[i][j].get())

        b = np.zeros(size)
        for i in range(size):
            b[i] = float(entry_b[i].get())

        lower, upper, steps = lu_decomposition(A)
        solution = solve_lu_system(lower, upper, b)

        result_window = tk.Toplevel(root)
        result_window.title("Resultados")
        result_text = scrolledtext.ScrolledText(result_window, width=80, height=20)

        result_str = "Matriz de Coeficientes (A):\n{}\n\n".format(A)
        result_str += "Vector de Términos Independientes (b):\n{}\n\n".format(b)

        result_str += "Pasos intermedios:\n"
        for step in steps:
            result_str += "Paso {}: i = {}\n".format(step["i"], step["i"])
            result_str += "Matriz L:\n{}\n".format(step["L"])
            result_str += "Matriz U:\n{}\n\n".format(step["U"])

        result_str += "Matriz Lower (L):\n{}\n\n".format(lower)
        result_str += "Matriz Upper (U):\n{}\n\n".format(upper)
        result_str += "Solución del sistema:\n{}".format(solution)

        result_text.insert(tk.END, result_str)
        result_text.pack()

    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_interface():
    size = int(entry_size.get())

    # Limpiar entradas anteriores
    for row in entry_A:
        for entry in row:
            entry.destroy()

    for entry in entry_b:
        entry.destroy()

    entry_A.clear()
    entry_b.clear()

    # Crear nuevas entradas para la matriz A
    for i in range(size):
        entry_A.append([])
        for j in range(size):
            entry = Entry(frame_A)
            entry.grid(row=i, column=j, padx=5, pady=2)
            entry_A[i].append(entry)

    # Crear nuevas entradas para el vector b
    for i in range(size):
        entry = Entry(frame_b)
        entry.grid(row=i, column=0, padx=5, pady=2)
        entry_b.append(entry)

    # Ajustar la geometría de la ventana de acuerdo al nuevo tamaño de la matriz
    root.update_idletasks()
    root.geometry('')

# Crear la interfaz gráfica
root = tk.Tk()
root.title("LU Decomposition Solver")

# Crear y colocar widgets en la interfaz
Label(root, text="Tamaño de la matriz cuadrada:").pack(pady=5)
entry_size = Entry(root)
entry_size.pack(pady=5)

Button(root, text="Actualizar", command=update_interface).pack(pady=5)
Button(root, text="Resolver", command=solve_linear_system).pack(pady=10)

frame_A = tk.Frame(root)
frame_A.pack(pady=10)

frame_b = tk.Frame(root)
frame_b.pack(pady=10)

entry_A = []
entry_b = []

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
