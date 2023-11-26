import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.stats import pearsonr
from tkinter import filedialog
from tkinter import Tk

# Función para abrir el explorador de archivos y obtener la ruta del archivo Excel
def seleccionar_archivo():
    root = Tk()
    root.withdraw()  # Evitar que se abra una ventana de tkinter
    archivo_excel = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Archivos Excel", "*.xlsx;*.xls")])
    root.destroy()
    return archivo_excel

# Opción para ingresar datos desde la consola o desde un archivo Excel
opcion = input("¿Desea ingresar datos desde la consola (C) o desde un archivo Excel (E)? ").upper()

if opcion == 'C':
    # Ingresar los datos desde la consola (N es la cantidad de datos)
    N = int(input("Ingrese la cantidad de datos: "))

    x = np.zeros(N)
    y = np.zeros(N)

    print("Ingrese los valores de x:")
    for i in range(N):
        x[i] = float(input(f"x[{i + 1}]: "))

    print("Ingrese los valores de y:")
    for i in range(N):
        y[i] = float(input(f"y[{i + 1}]: "))

elif opcion == 'E':
    # Leer datos desde un archivo Excel seleccionado por el usuario
    archivo_excel = seleccionar_archivo()
    datos = pd.read_excel(archivo_excel)

    # Extraer las columnas correspondientes a x e y
    x = datos['x'].values
    y = datos['y'].values

else:
    print("Opción no válida. Por favor, ingrese 'C' o 'E'.")



# Crear un DataFrame para mostrar los datos en forma tabular
datos = pd.DataFrame({'x': x, 'y': y, 'xy': x * y, 'x^2': x**2, 'y^2': y**2})

# Mostrar la tabla con los totales
totales = datos.sum().to_frame('Total').transpose()
print("\nTabla con Totales:")
print(totales)

# Cambiar la forma de los datos para que scikit-learn los acepte
X = x.reshape(-1, 1)

# Crear un modelo de regresión lineal
modelo = LinearRegression()

# Entrenar el modelo con los datos
modelo.fit(X, y)

# Calcular los coeficientes prácticos
a1 = modelo.coef_[0]
a0 = modelo.intercept_

# Calcular la Coeficiencia de Pearson
coef_pearson, _ = pearsonr(x, y)

# Imprimir los resultados
print("\nResultados:")
print(f"Coeficiente a1 (pendiente): {a1}")
print(f"Coeficiente a0 (intercepto): {a0}")
print(f"Coeficiencia de Pearson: {coef_pearson}")

# Realizar predicciones para nuevos datos
nuevos_datos = np.array([6, 7, 8]).reshape(-1, 1)
predicciones = modelo.predict(nuevos_datos)

# Visualizar los resultados
plt.scatter(x, y, color='blue', label='Datos reales')
plt.plot(np.concatenate((x, nuevos_datos[:, 0])), np.concatenate((modelo.predict(X), predicciones)), color='red', label='Regresión lineal')
plt.xlabel('Variable Independiente')
plt.ylabel('Variable Dependiente')
plt.legend()
plt.show()
