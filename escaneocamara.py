import cv2 
from pyzbar.pyzbar import decode
import pandas as pd
from datetime import datetime
import os
import time
import tkinter as tk
from tkinter import messagebox

# Generar nombre de archivo con fecha
fecha_actual = datetime.now().strftime('%Y-%m-%d')
archivo_excel = f'GUIAS_ESCANEADAS_{fecha_actual}.xlsx'

# Lista para almacenar códigos escaneados
codigos_guardados = []

# Variables
cooldown_codigos = {}
cooldown_time = 2  # Reducir el tiempo de espera entre el mismo código
pausa_global = 1   # Reducir la pausa entre escaneos
ultimo_escaneo = time.time()
tiempo_espera = 10  # Reducir el tiempo de espera antes de cerrar

def abrir_ubicacion_archivo():
    """ Abre la ubicación del archivo Excel en el explorador de archivos """
    os.startfile(os.path.abspath(archivo_excel))

def guardar_codigos_excel():
    """ Guarda todos los códigos almacenados en la lista en un archivo Excel """
    if codigos_guardados:
        df = pd.DataFrame(codigos_guardados, columns=['Número de Guía', 'Fecha'])
        df.to_excel(archivo_excel, index=False)
        messagebox.showinfo("Guardado", "Todos los códigos han sido guardados en el archivo Excel.")
        abrir_ubicacion_archivo()

def guardar_codigo(guia):
    """ Agrega el código a la lista si no está duplicado """
    fecha = datetime.now().strftime('%Y-%m-%d')
    
    # Verificar si el código ya está registrado en la lista
    if guia in [item[0] for item in codigos_guardados]:        
        messagebox.showwarning("Código Duplicado", f"El código {guia} ya está registrado.")
        return
    
    codigos_guardados.append([guia, fecha])

def mostrar_interfaz(guia):
    """ Interfaz para mostrar el código escaneado y permitir modificaciones """
    def confirmar():
        nuevo_codigo = texto_codigo.get("1.0", tk.END).strip()
        if nuevo_codigo:
            guardar_codigo(nuevo_codigo)
            if messagebox.askyesno("Continuar", "¿Desea escanear otro código?"):
                ventana.destroy()
                escanear_codigo()
            else:
                ventana.destroy()
                guardar_codigos_excel()
                return
    
    ventana = tk.Tk()
    ventana.title("Escáner de Código")
    ventana.geometry("400x300")

    etiqueta = tk.Label(ventana, text="Código escaneado:")
    etiqueta.pack(pady=5)
    
    texto_codigo = tk.Text(ventana, height=2, width=40)
    texto_codigo.pack(pady=5)
    texto_codigo.insert(tk.END, guia)
    
    boton_confirmar = tk.Button(ventana, text="Guardar Código", command=confirmar)
    boton_confirmar.pack(pady=10)
    
    ventana.mainloop()

def escanear_codigo():
    """ Función para escanear códigos de barras """
    global ultimo_escaneo
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    tiempo_inicio = time.time()
    
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for code in decode(gray):
            data = code.data.decode('utf-8')
            ahora = time.time()
            
            if (ahora - ultimo_escaneo) >= pausa_global:
                if data not in cooldown_codigos or (ahora - cooldown_codigos[data]) > cooldown_time:
                    cooldown_codigos[data] = ahora
                    cap.release()
                    cv2.destroyAllWindows()
                    mostrar_interfaz(data)
                    return
        
        cv2.imshow('Escaneo Continuo', frame)
        if cv2.waitKey(1) == 27 or (time.time() - tiempo_inicio) > tiempo_espera:
            break
    
    cap.release()
    cv2.destroyAllWindows()
    preguntar_ingreso_manual()

def preguntar_ingreso_manual():
    """ Pregunta al usuario si desea ingresar el código manualmente o intentar otro escaneo """
    ventana = tk.Tk()
    ventana.withdraw()
    if messagebox.askyesno("Tiempo agotado", "No se detectó un código. ¿Desea ingresar uno manualmente?"):
        agregar_manual()
    else:
        if messagebox.askyesno("Intentar de nuevo", "¿Desea escanear otro código?"):
            escanear_codigo()
        else:
            guardar_codigos_excel()

def agregar_manual():
    """ Interfaz para ingresar manualmente un código """
    def confirmar_manual():
        codigo_manual = texto_codigo.get("1.0", tk.END).strip()
        if codigo_manual:
            guardar_codigo(codigo_manual)
            if messagebox.askyesno("Continuar", "¿Desea escanear otro código?"):
                ventana.destroy()
                escanear_codigo()
            else:
                ventana.destroy()
                guardar_codigos_excel()
                return
    
    ventana = tk.Tk()
    ventana.title("Agregar Código Manualmente")
    ventana.geometry("400x300")
    
    etiqueta = tk.Label(ventana, text="No se detectó un código. Ingrese manualmente:")
    etiqueta.pack(pady=5)
    
    texto_codigo = tk.Text(ventana, height=2, width=40)
    texto_codigo.pack(pady=5)
    
    boton_confirmar = tk.Button(ventana, text="Guardar Código", command=confirmar_manual)
    boton_confirmar.pack(pady=10)
    
    ventana.mainloop()

def iniciar_app():
    """ Interfaz principal con menú """
    ventana = tk.Tk()
    ventana.title("Sistema de Escaneo de Códigos")
    ventana.geometry("400x200")
    
    etiqueta = tk.Label(ventana, text="Sistema de Escaneo de Códigos", font=("Arial", 14))
    etiqueta.pack(pady=10)
    
    boton_escanear = tk.Button(ventana, text="Escanear Código", command=escanear_codigo, height=2, width=20)
    boton_escanear.pack(pady=20)
    
    ventana.mainloop()

if __name__ == "__main__":
    iniciar_app()
