import pandas as pd

df = pd.read_excel('../Libro Excel Descriptivo.xlsx', header=1)
print('=== FIRST 10 ROWS ===')
for i in range(10):
    print(f'Row {i}:')
    print(f'  Nombre: {df.iloc[i].get("Nombre del ejercicio")}')
    print(f'  Movimiento: {df.iloc[i].get("Por movimiento")}')
    print(f'  Muscular: {df.iloc[i].get("Por Plano Muscular")}')
    print(f'  Implemento: {df.iloc[i].get("Por implemento")}')
    print(f'  Clasificación: {df.iloc[i].get("Clasificación del ejercicio")}')
    print()
