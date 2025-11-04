# 🚗 A.D.A.M. - Advanced Driver Assistance Monitor

**A.D.A.M. (Advanced Driver Assistance Monitor)** es una aplicación de escritorio desarrollada en **Python** que utiliza **visión por computadora** y **reconocimiento visual en tiempo real** para ofrecer tres funcionalidades principales de asistencia a la conducción:

- 🔥 **Mapa de calor de proximidad**
- 🧠 **Detección de fatiga del conductor**
- 🚦 **Detección de semáforos**

El objetivo del proyecto es simular un **sistema inteligente de asistencia a la conducción (ADAS)**, combinando algoritmos de visión artificial con una interfaz intuitiva en **Tkinter**.

---

## 🧩 Características principales

### 🔥 HeatMap de Proximidad
Analiza el entorno en tiempo real para determinar **la cercanía de objetos** al vehículo.  
El sistema dibuja líneas de alerta en pantalla (zona amarilla y zona roja) y superpone un **mapa de calor dinámico** que resalta las zonas de peligro.

**Principales técnicas:**
- Detección de bordes con `Canny` y análisis de contornos.  
- Estimación de proximidad según posición vertical y tamaño de objetos.  
- Alerta visual y sonora ante peligro de colisión.

---

### 😴 Detección de Fatiga
Detecta el cierre prolongado de ojos del conductor mediante el uso de clasificadores Haar.  
Si se supera un umbral de tiempo o proporción de ojos cerrados, el sistema emite una **alerta sonora** y un aviso visual en pantalla.

**Principales técnicas:**
- Detección facial y ocular con `haarcascade_frontalface_default.xml` y `haarcascade_eye.xml`.  
- Cálculo del ratio de cierres oculares consecutivos.  
- Alerta por fatiga basada en frames detectados y proporción temporal.

---

### 🚦 Detección de Semáforos
Reconoce el color activo del semáforo dentro de una región definida de la cámara.  
Emite señales visuales y acústicas según el estado detectado.

**Principales técnicas:**
- Conversión a espacio de color HSV.  
- Detección por rangos de color (`rojo`, `amarillo`, `verde`).  
- Filtrado morfológico para reducir ruido.  
- Sistema de prioridad basado en el área del color dominante.

---

## 🖥️ Interfaz gráfica

El sistema cuenta con una interfaz moderna e inmersiva desarrollada en **Tkinter**, que incluye:
- Pantalla de carga animada con logo.  
- Menú principal con tres modos de funcionamiento.  
- Barra lateral con estado del sistema y botón de retorno.  
- Integración visual en tiempo real con cámara.

---

## ⚙️ Requisitos e instalación

### 🧰 Dependencias
Instala las librerías necesarias con:

```bash
pip install opencv-python pillow numpy

```

## 🚀 Ejecución

Para ejecutar la aplicación, asegúrate de tener las dependencias instaladas y ejecuta el archivo principal desde la terminal:

```bash
python ADAM.py

```

## 🧠 Arquitectura del sistema

El sistema **A.D.A.M. (Advanced Driver Assistance Monitor)** está diseñado con una arquitectura modular y escalable, que permite integrar nuevas funcionalidades fácilmente.  
Su estructura principal se compone de los siguientes módulos:

1. **Interfaz gráfica (Tkinter):**  
   Controla el menú principal, los botones y las vistas de cámara en tiempo real.  
   Está diseñada para ser intuitiva y adaptable a pantalla completa.

2. **Captura y procesamiento de vídeo (OpenCV + NumPy):**  
   Se encarga de la adquisición de imágenes desde la cámara y del análisis de cada modo funcional:
   - Detección de ojos y rostro (modo Fatigue)  
   - Detección de color y proximidad (modo Semaphore y HeatMap)

3. **Sistema de alertas (Winsound):**  
   Emite avisos acústicos según el estado detectado por cada modo (fatiga, semáforo o peligro cercano).

4. **Gestión de estados:**  
   Cada modo mantiene su propio bucle de análisis (`_loop_fatigue`, `_loop_heatmap`, `_loop_semaphore`) y su inicialización (`_init_...`), facilitando la independencia y mantenimiento del código.

---

## 🧩 Tecnologías empleadas

| Tecnología       | Función principal                                  |
|------------------|----------------------------------------------------|
| **Python 3.x**   | Lenguaje principal del proyecto                    |
| **OpenCV**       | Procesamiento de vídeo en tiempo real              |
| **Tkinter**      | Creación de la interfaz gráfica                    |
| **NumPy**        | Manipulación eficiente de matrices e imágenes      |
| **Pillow (PIL)** | Conversión de imágenes para mostrar en la interfaz |
| **Winsound**     | Generación de alertas sonoras en Windows           |

---

## 👥 Autores y créditos

**Autor principal:**  
- Alberto Simón Fernández de la Mela
- Estudiante de Ingeniería Informática

**Inspiración y librerías utilizadas:**
- OpenCV y documentación oficial de Haar Cascades
- Comunidad de desarrolladores de visión artificial y detección de fatiga

---

## 🔮 Futuras mejoras

Algunas ideas para evolucionar el sistema A.D.A.M. en versiones futuras:

- 📷 **Integración con cámaras infrarrojas** para detección en baja iluminación.  
- 🧠 **Uso de redes neuronales ligeras (CNNs)** para detección facial más precisa.  
- 🚗 **Reconocimiento de señales de tráfico adicionales** (stop, límite de velocidad, peatones).  
- 🔊 **Sistema de avisos por voz** en lugar de simples pitidos.  

---

## 🏁 Texto final

> “A.D.A.M. no es solo un sistema de visión artificial:  
> es un primer paso hacia una conducción más segura, consciente y asistida.  
> Su propósito es claro, ayudar al conductor a prevenir accidentes antes de que ocurran.”

---
