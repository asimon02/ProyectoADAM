import cv2
import winsound
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

# ===============================
#     CONFIGURACIÓN INICIAL
# ===============================

HAAR_FACE = 'haarcascades/haarcascade_frontalface_default.xml'
HAAR_EYE = 'haarcascades/haarcascade_eye.xml'
CAM_INDEX = 0
WINDOW_BG = "#2C2C2C"

# ===============================
#     CLASE PRINCIPAL ADAM
# ===============================

class ADAM:
    def __init__(self, root):
        self.root = root
        self.root.title("A.D.A.M. - Advanced Driver Assistance Monitor")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg=WINDOW_BG)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close_all)

        # ===============================
        #            LOGO ADAM
        # ===============================
        try:
            logo_cv = cv2.imread('Logo/ADAM.jpg')
            if logo_cv is not None:
                logo_rgb = cv2.cvtColor(logo_cv, cv2.COLOR_BGR2RGB)
                logo_large = cv2.resize(logo_rgb, (335, 335))
                self.logo_main = ImageTk.PhotoImage(Image.fromarray(logo_large))
                logo_small = cv2.resize(logo_rgb, (230, 230))
                self.logo_small = ImageTk.PhotoImage(Image.fromarray(logo_small))
            else:
                print("⚠️ No se pudo cargar el logo ADAM desde 'Logo/ADAM.jpg'")
                self.logo_main = self.logo_small = None
        except Exception as e:
            print("Error al cargar el logo:", e)
            self.logo_main = self.logo_small = None

        # ===============================
        #         CLASIFICADORES
        # ===============================
        self.face_cascade = cv2.CascadeClassifier(HAAR_FACE)
        self.eye_cascade = cv2.CascadeClassifier(HAAR_EYE)

        # ===============================
        #         MENÚ PRINCIPAL
        # ===============================
        self.main_frame = tk.Frame(self.root, bg=WINDOW_BG)

        title = tk.Label(self.main_frame, text="A.D.A.M. - Advanced Driver Assistance Monitor",
                         font=("Segoe UI", 28, "bold"), fg="white", bg=WINDOW_BG)
        title.pack(pady=24)

        subtitle = tk.Label(self.main_frame, text="Selecciona un modo:",
                            font=("Segoe UI", 16), fg="white", bg=WINDOW_BG)
        subtitle.pack(pady=(0, 20))

        btn_style = {"font": ("Segoe UI", 16, "bold"), "fg": "white", "bd": 0, "cursor": "hand2"}

        self.btn_heatmap = tk.Button(self.main_frame, text="🔥 Heatmap de Proximidad",
                                     command=self.open_heatmap_mode, bg="#229954", **btn_style)
        self.btn_heatmap.pack(ipadx=20, ipady=10, fill="x", padx=160, pady=10)
        
        self.btn_fatigue = tk.Button(self.main_frame, text="😴 Detección de Fatiga",
                                     command=self.open_fatigue_mode, bg="#FF8C00", **btn_style)
        self.btn_fatigue.pack(ipadx=20, ipady=10, fill="x", padx=160, pady=10)

        self.btn_semaphore = tk.Button(self.main_frame, text="🚦 Detección de Semáforos",
                                     command=self.open_semaphore_mode, bg="#007ACC", **btn_style)
        self.btn_semaphore.pack(ipadx=20, ipady=10, fill="x", padx=160, pady=10)

        if self.logo_main:
            self.logo_label_main = tk.Label(self.main_frame, image=self.logo_main, bg=WINDOW_BG)
            self.logo_label_main.pack(pady=(30, 20))

        footer = tk.Label(self.main_frame, text="Presiona ESC para salir del modo / volver al menú",
                          font=("Segoe UI", 10), fg="white", bg=WINDOW_BG)
        footer.pack(side="bottom", pady=12)

        # ===============================
        #        MÓDULOS DE APP
        # ===============================
        self.mode_frame = tk.Frame(self.root, bg=WINDOW_BG)
        self.video_frame = tk.Frame(self.mode_frame, bg="#1F1F1F", highlightbackground="#656C6E", highlightthickness=3)
        self.video_frame.place(relx=0.2, rely=0.05, relwidth=0.75, relheight=0.85)
        self.label_video = tk.Label(self.video_frame, bg="#2C2C2C")
        self.label_video.pack(fill="both", expand=True)

        self.side_frame = tk.Frame(self.mode_frame, bg=WINDOW_BG)
        self.side_frame.place(relx=0.02, rely=0.05, relwidth=0.15, relheight=0.9)

        self.btn_back = tk.Button(self.side_frame, text="← Volver", command=self._close_mode,
                                  font=("Segoe UI", 12, "bold"), bg="#C0392B", fg="white", bd=0, cursor="hand2")
        self.btn_back.pack(fill="x", pady=(0, 12))

        if self.logo_small:
            self.logo_label_small = tk.Label(self.side_frame, image=self.logo_small, bg=WINDOW_BG)
            self.logo_label_small.pack(pady=(10, 20))

        self.status_label = tk.Label(self.side_frame, text="", font=("Segoe UI", 12),
                                     fg="white", bg=WINDOW_BG, wraplength=130, justify="left")
        self.status_label.pack(anchor="n", pady=6)

        # ===============================
        #     FLAGS Y BINDS GLOBALES
        # ===============================
        self.cap = None
        self.running = False
        self.current_mode = None
        self.root.bind("<Escape>", lambda e: self._on_escape())
        self._show_startup_screen()

    # ===============================
    #    PANTALLA DE CARGA INICIAL
    # ===============================
    def _show_startup_screen(self):
        self.root.withdraw()

        splash = tk.Toplevel(self.root)
        splash.overrideredirect(True)
        splash.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        splash.configure(bg="#000000")
        splash.attributes('-topmost', True)
        splash.lift()

        if self.logo_main:
            logo_label = tk.Label(splash, image=self.logo_main, bg="#000000")
            logo_label.place(relx=0.5, rely=0.45, anchor="center")

        texto = tk.Label(splash, text="Arrancando sistemas A.D.A.M...",
                         fg="#B856F1", bg="#000000", font=("Aptos", 18, "bold"))
        texto.place(relx=0.5, rely=0.7, anchor="center")

        mensajes = ["Arrancando sistemas A.D.A.M...",
                    "Inicializando módulos visuales...",
                    "Calibrando sensores...",
                    "Todo listo para conducir 👍"]

        def animar(i=0):
            if i < len(mensajes):
                texto.config(text=mensajes[i])
                splash.after(900, lambda: animar(i + 1))
            else:
                splash.destroy()
                self.root.deiconify()
                self.main_frame.pack(fill="both", expand=True)

        splash.after(600, animar)

    # ===============================
    #    PANTALLA DE CARGA DE MODO
    # ===============================
    def _show_mode_loading(self, mode_name, callback):
        splash = tk.Toplevel(self.root)
        splash.overrideredirect(True)
        splash.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        splash.configure(bg="#000000")
        splash.transient(self.root)
        splash.attributes('-topmost', True)
        splash.lift()
        splash.grab_set()

        label_text = tk.Label(splash, text=f"Activando modo: {mode_name}...",
                              font=("Aptos", 18, "bold"), fg="#B856F1", bg="#000000")
        label_text.place(relx=0.5, rely=0.45, anchor="center")

        barra = tk.Canvas(splash, width=400, height=20, bg="#222", highlightthickness=0)
        barra.place(relx=0.5, rely=0.55, anchor="center")
        rect = barra.create_rectangle(0, 0, 0, 20, fill="#B856F1")

        def animar(val=0):
            if val <= 400:
                barra.coords(rect, 0, 0, val, 20)
                splash.after(10, lambda: animar(val + 10))
            else:
                splash.grab_release()
                splash.destroy()

                def _safe_callback():
                    self.root.update_idletasks()
                    callback()

                self.root.after(50, _safe_callback)

        splash.after(600, animar)

    # ===============================
    #     MODOS DE FUNCIONAMIENTO
    # ===============================
    def open_heatmap_mode(self): self._open_mode("HeatMap")
    def open_fatigue_mode(self): self._open_mode("Fatigue")
    def open_semaphore_mode(self): self._open_mode("Semaphore")

    def _open_mode(self, mode_name):
        self.main_frame.pack_forget()

        def iniciar_modo():
            self.mode_frame.pack(fill="both", expand=True)
            self.current_mode = mode_name
            self.status_label.config(text="Inicializando cámara...")
            self._start_camera()

            if mode_name == "HeatMap":
                self._init_heatmap()
                self.root.after(100, self._loop_heatmap)
            elif mode_name == "Fatigue":
                self._init_fatigue()
                self.root.after(100, self._loop_fatigue)
            elif mode_name == "Semaphore":
                self._init_semaphore()
                self.root.after(100, self._loop_semaphore)

        self._show_mode_loading(mode_name, iniciar_modo)

    # ===============================
    #         GESTIÓN GENERAL
    # ===============================
    def _close_mode(self):
        self.running = False
        self._stop_camera()
        self.mode_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)
        self.current_mode = None
        self.status_label.config(text="")

    def _on_escape(self):
        if self.current_mode:
            self._close_mode()
        else:
            self._on_close_all()

    def _on_close_all(self):
        self.running = False
        self._stop_camera()
        self.root.quit()
        self.root.destroy()

    # ===============================
    #   CONFIGURACIÓN DE LA CÁMARA
    # ===============================
    def _start_camera(self):
        self.cap = cv2.VideoCapture(CAM_INDEX)
        self.running = True

    def _stop_camera(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()
        self.cap = None
        self.running = False

    # ===============================
    #             ÚTILES
    # ===============================
    def _show_frame_on_label(self, frame):
        if frame is None:
            return
        
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)
        w = self.label_video.winfo_width()
        h = self.label_video.winfo_height()

        if w > 1 and h > 1:
            img = img.resize((w, h))
        
        imgtk = ImageTk.PhotoImage(image=img)
        self.label_video.imgtk = imgtk
        self.label_video.configure(image=imgtk)

    def _beep(self, freq, dur):
        winsound.Beep(int(freq), int(dur))

    # ===============================
    #         MODO: Heatmap
    # ===============================
    def _init_heatmap(self):
        self.h_prev_gray = None
        self.h_heatmap = None
        self.h_decay = 0.5
        self.h_min_area = 1200
        self.h_alert_distance_area = 6000
        self.h_warning_area = 3500
        self.h_smooth_frames = []
        self.h_intensity = 6
        self.h_danger_frames = 0
        self.h_warning_frames = 0

        self.status_label.config(
            text="Modo: Heatmap de proximidad\nAnalizando tamaño y cercanía de objetos..."
        )

    def _loop_heatmap(self):
        if not self.running or (self.current_mode or "").lower() != "heatmap":
            return

        ret, frame = self.cap.read()
        if not ret:
            self.status_label.config(text="Error leyendo cámara")
            self.root.after(200, self._loop_heatmap)
            return

        frame = cv2.flip(frame, 1)
        display = frame.copy()
        h, w = frame.shape[:2]

        if self.h_heatmap is None or self.h_heatmap.shape != (h, w):
            self.h_heatmap = np.zeros((h, w), dtype=np.float32)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (11, 11), 0)

        # ===============================
        #  Detección de objetos grandes
        # ===============================
        edges = cv2.Canny(gray, 50, 150)
        edges = cv2.dilate(edges, None, iterations=2)
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        largest_area = 0
        danger = False

        # ===============================
        #      Líneas de proximidad
        # ===============================
        warning_line_y = int(h * 0.7)
        danger_line_y = int(h * 0.85)
        cv2.line(display, (0, warning_line_y), (w, warning_line_y), (0, 255, 255), 2)
        cv2.line(display, (0, danger_line_y), (w, danger_line_y), (0, 0, 255), 3)

        # ===============================
        #     Análisis de contornos
        # ===============================
        for c in contours:
            area = cv2.contourArea(c)
            if area < self.h_min_area:
                continue

            largest_area = max(largest_area, area)
            (x, y, wb, hb) = cv2.boundingRect(c)
            cx, cy = x + wb // 2, y + hb // 2

            if y + hb > danger_line_y:
                color = (0, 0, 255)  # rojo
                danger = True
            elif y + hb > warning_line_y:
                color = (0, 255, 255)  # amarillo
            else:
                color = (0, 255, 0)  # verde

            cv2.rectangle(display, (x, y), (x + wb, y + hb), color, 2)
            cv2.circle(self.h_heatmap, (cx, cy), int(max(wb, hb) / 2), self.h_intensity, -1)

        self.h_heatmap *= self.h_decay

        self.h_smooth_frames.append(largest_area)
        if len(self.h_smooth_frames) > 10:
            self.h_smooth_frames.pop(0)
        avg_area = np.mean(self.h_smooth_frames) if self.h_smooth_frames else 0

        # ===============================
        #      Sistema de alertas
        # ===============================
        if danger or avg_area > self.h_alert_distance_area:
            self.h_danger_frames += 1
            if self.h_danger_frames > 3:
                self.status_label.config(text="⚠️ PELIGRO: Objeto demasiado cerca")
        elif avg_area > self.h_warning_area:
            self.h_warning_frames += 1
            if self.h_warning_frames > 5:
                self.status_label.config(text="⚠️ Precaución: Objeto cercano")
        else:
            self.h_danger_frames = self.h_warning_frames = 0
            self.status_label.config(text="Modo: Heatmap de proximidad")

        # ===============================
        #    Superposición del heatmap
        # ===============================
        heat_smooth = cv2.GaussianBlur(self.h_heatmap, (0, 0), sigmaX=25)
        heat_norm = cv2.normalize(heat_smooth, None, 0, 255, cv2.NORM_MINMAX)
        heat_color = cv2.applyColorMap(heat_norm.astype(np.uint8), cv2.COLORMAP_JET)
        display = cv2.addWeighted(display, 0.7, heat_color, 0.3, 0)

        self._show_frame_on_label(display)
        self.root.after(50, self._loop_heatmap)

    # ===============================
    #          MODO: Fatigue
    # ===============================
    def _init_fatigue(self):
        self.f_count_closed = 0
        self.f_total_frames = 0
        self.f_alert = False
        self.f_threshold = 15
        self.f_ratio_limit = 0.35
        self.f_beep_freq = 1000
        self.f_beep_dur = 400

        self.status_label.config(
            text="Modo: Detección de fatiga\nAnalizando cierres oculares..."
        )

    def _loop_fatigue(self):
        if not self.running or self.current_mode != "Fatigue":
            return

        ret, frame = self.cap.read()
        if not ret:
            self.status_label.config(text="Error leyendo cámara")
            self.root.after(200, self._loop_fatigue)
            return

        frame = cv2.flip(frame, 1)
        display = frame.copy()
        self.f_total_frames += 1

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        eyes_detected = 0

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            eyes = self.eye_cascade.detectMultiScale(roi_gray, 1.2, 8, minSize=(20, 20))
            eyes_detected = len(eyes)
            cv2.rectangle(display, (x, y), (x+w, y+h), (0, 255, 255), 2)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(display, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (0, 255, 0), 2)

        # =============================
        #     Lógica de detección
        # =============================
        if eyes_detected == 0:
            self.f_count_closed = min(self.f_threshold, self.f_count_closed + 1)
        else:
            self.f_count_closed = max(0, self.f_count_closed - 1)

        ratio_cerrado = self.f_count_closed / max(1, self.f_total_frames)

        if (self.f_count_closed >= self.f_threshold or ratio_cerrado > self.f_ratio_limit) and not self.f_alert:
            self.f_alert = True
            self.status_label.config(
                text="ALARMA: Fatiga detectada\nFrames cerrados: %d (%.0f%%)"
                % (self.f_count_closed, ratio_cerrado * 100)
            )
            winsound.Beep(self.f_beep_freq, self.f_beep_dur)
        elif eyes_detected > 0:
            self.f_alert = False
            self.status_label.config(
                text="Modo: Fatiga\nFrames cerrados: %d (%.0f%%)"
                % (self.f_count_closed, ratio_cerrado * 100)
            )

        # =============================
        #     Mostrar estado visual
        # =============================
        estado_txt = "Ojos cerrados" if eyes_detected == 0 else "Ojos abiertos"
        color_txt = (0, 255, 0) if eyes_detected > 0 else (0, 0, 255)
        cv2.putText(display, f"Estado: {estado_txt}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color_txt, 2)

        if self.f_alert:
            cv2.putText(display, "FATIGA DETECTADA", (20, 90),
                        cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 255), 3)

        self._show_frame_on_label(display)
        self.root.after(30, self._loop_fatigue)

    # ===============================
    #        MODO: Semaphore
    # ===============================
    def _init_semaphore(self):
        self.t_last_state = None
        self.t_area_threshold = 400
        self.t_beep_dur = 200
        self.status_label.config(
            text="Modo: Detección de semáforos\nMantén el semáforo dentro del recuadro"
        )

    def _loop_semaphore(self):
        if not self.running or self.current_mode != "Semaphore":
            return

        ret, frame = self.cap.read()
        if not ret:
            self.status_label.config(text="Error leyendo cámara")
            self.root.after(200, self._loop_semaphore)
            return

        frame = cv2.flip(frame, 1)
        display = frame.copy()
        h, w = frame.shape[:2]

        x1, y1, x2, y2 = int(w * 0.30), int(h * 0.30), int(w * 0.70), int(h * 0.70)
        roi = frame[y1:y2, x1:x2]

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        rojo1 = cv2.inRange(hsv, (0, 100, 120), (10, 255, 255))
        rojo2 = cv2.inRange(hsv, (165, 100, 120), (179, 255, 255))
        rojo = cv2.add(rojo1, rojo2)
        amarillo = cv2.inRange(hsv, (18, 100, 140), (35, 255, 255))
        verde = cv2.inRange(hsv, (35, 80, 100), (85, 255, 255))

        kernel = np.ones((5, 5), np.uint8)
        rojo = cv2.morphologyEx(rojo, cv2.MORPH_OPEN, kernel)
        amarillo = cv2.morphologyEx(amarillo, cv2.MORPH_OPEN, kernel)
        verde = cv2.morphologyEx(verde, cv2.MORPH_OPEN, kernel)

        area_rojo = cv2.countNonZero(rojo)
        area_amarillo = cv2.countNonZero(amarillo)
        area_verde = cv2.countNonZero(verde)
        max_area = max(area_rojo, area_amarillo, area_verde)

        estado = "Sin semaforo detectado"
        color_box = (200, 200, 200)

        if max_area < self.t_area_threshold:
            estado = "Sin semaforo detectado"
        elif area_rojo > 1.2 * max(area_amarillo, area_verde):
            estado = "ROJO - Detenerse"
            color_box = (0, 0, 255)
        elif area_amarillo > 1.1 * max(area_rojo, area_verde):
            estado = "AMARILLO - Precaucion"
            color_box = (0, 255, 255)
        elif area_verde > 1.1 * max(area_rojo, area_amarillo):
            estado = "VERDE - Avanzar"
            color_box = (0, 255, 0)

        cv2.rectangle(display, (x1, y1), (x2, y2), color_box, 2)
        cv2.putText(display, estado, (20, 50), cv2.FONT_HERSHEY_DUPLEX, 1.0, color_box, 2)

        if estado != self.t_last_state:
            self.t_last_state = estado
            if "ROJO" in estado:
                self._beep(600, self.t_beep_dur)
            elif "AMARILLO" in estado:
                self._beep(1000, self.t_beep_dur)
            elif "VERDE" in estado:
                self._beep(1400, self.t_beep_dur)

        self._show_frame_on_label(display)
        self.status_label.config(text=f"Modo: Semaforo\nEstado: {estado}")
        self.root.after(120, self._loop_semaphore)

# ===============================
#           EJECUCIÓN
# ===============================

if __name__ == "__main__":
    root = tk.Tk()
    app = ADAM(root)
    root.mainloop()
