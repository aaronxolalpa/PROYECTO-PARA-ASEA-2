Sistema de Escaneo de Códigos con Cámara y Guardado en Excel realizado durante mi servicio social en ASEA(Agencia de Seguridad Energia y Medio Ambiente)
Este proyecto en Python permite escanear códigos de barras utilizando la cámara web y guardar los códigos de barras de guias de SEPOMEX capturados en un archivo Excel, con opción de edición manual y validación de duplicados, todo gestionado mediante una interfaz gráfica construida con Tkinter ayudando a tener registro de cuales son las guias ingresadas.

Funcionalidades
Escaneo en tiempo real de códigos con la cámara (usando OpenCV y Pyzbar).

Detección automática de duplicados para evitar registros repetidos.

Interfaz para editar o ingresar manualmente códigos cuando el escaneo falla.

Exportación automática a archivo Excel con la fecha actual en el nombre (por ejemplo: GUIAS_ESCANEADAS_2025-04-30.xlsx).

Mecanismo de tiempo de espera para evitar registrar el mismo código varias veces seguidas.

Interfaz sencilla e intuitiva con opciones de confirmación y navegación.

Interfaz principal
Un botón principal permite iniciar el escaneo de códigos.

Si no se detecta un código en un tiempo determinado, el sistema pregunta si se desea ingresar el código manualmente.

Cada código puede revisarse y editarse antes de ser guardado.

Al finalizar, todos los códigos se exportan a un archivo Excel.

Salida esperada
El archivo generado tendrá el nombre GUIAS_ESCANEADAS_YYYY-MM-DD.xlsx y contendrá dos columnas:

Número de Guía

Fecha

Consideraciones
El sistema utiliza la cámara predeterminada del equipo mediante cv2.VideoCapture.

Puede ser adaptado para integrarse con otros sistemas, como bases de datos o servicios web.

Es útil para tareas logísticas como control de recepción, escaneo de guías o auditoría de envíos.
