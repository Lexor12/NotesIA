#   Interfaz Gráfica.
import customtkinter as ctk
from lib.recorder import *
from lib.transcriber import *
from lib.ollamacon import *
import tkinter as Tk # Para pedir confirmación
import os,subprocess,sys,shutil,json

ctk.set_default_color_theme("blue")

class App(ctk.CTk):#Heredamos de la ventana para poder crear nuestra clase a partir de esta
    def __init__(self):
        super().__init__()
        os.makedirs("recordings", exist_ok=True)
        os.makedirs("summaries", exist_ok=True)
        os.makedirs("transcripts", exist_ok=True)
        self.title("NotesIA") 
        self.geometry("1200x900")
        self.minsize(800, 900)  # ancho, alto
        self.maxsize(1200, 900)

        self.Transcriber = Transcriber()
        self.Grabadora = Grabadora()
        self.Resumidor = Resumidor()
        
        self.Transcriber_mode = 1#1 -> Automatico
        self.Resumer_mode = 0#0 -> Manual

        self.bottom_frame = ctk.CTkFrame(self,height=100,bg_color="#9FC0DC",fg_color="#197571",corner_radius=0)
        self.bottom_frame.pack(side="bottom",fill="x")
        self.bottom_frame.pack_propagate(False)  # evita que se achique
        
        self.nav_inner = ctk.CTkFrame(self.bottom_frame,fg_color="transparent",corner_radius=0)
        self.nav_inner.pack(pady=20,expand=True)
        
        self.btn_config = nav_button(self.nav_inner, "Configuración", "#D13C3C")
        self.btn_config.pack(side="left", padx=10)

        self.btn_grab = nav_button(self.nav_inner, "Grabar Audio", "#0D7F4A")
        self.btn_grab.pack(side="left", padx=10)

        self.btn_audios = nav_button(self.nav_inner, "Audios", "#F2873B")
        self.btn_audios.pack(side="left", padx=10)

        self.btn_trans = nav_button(self.nav_inner, "Transcripciones", "#51B4ED")
        self.btn_trans.pack(side="left", padx=10)

        self.btn_res = nav_button(self.nav_inner, "Resúmenes", "#B87255")
        self.btn_res.pack(side="left", padx=10)
        
        self.container = ctk.CTkFrame(self,fg_color="#A8E3E1")
        self.container.pack(fill="both",expand=True)
        
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.btn_config.configure(command=lambda: self.show_frame(Configuracion))
        self.btn_grab.configure(command=lambda: self.show_frame(Grabador))
        self.btn_audios.configure(command=lambda: self.show_frame(Audios))
        self.btn_trans.configure(command=lambda: self.show_frame(Transcripciones))
        self.btn_res.configure(command=lambda: self.show_frame(Resumenes))
        
        self.author_lbl = ctk.CTkLabel(self,text="Hecho por Lexor12 (Lexor_12) on Github. https://github.com/Lexor12",font=("Times New Roman",10,"italic"))
        self.author_lbl.pack(side="bottom",fill="x")
        
        self.frames = {}

        for F in (Configuracion, Grabador, Audios, Transcripciones, Resumenes):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Configuracion)

        
    def show_frame(self, FrameClass):
        frame = self.frames[FrameClass]
        frame.tkraise()   # solo trae al frente, NO destruye
        
    def run(self):
        self.mainloop() 

class Configuracion(ctk.CTkFrame):
    def __init__(self,parent,controller):
        super().__init__(parent,fg_color="#D6DEDE",corner_radius=0)
        self.controller = controller
        
        #self.controller.Grabador.config()
        #self.controller.Transcriber.config()
        
        #Frame superior
        self.up_frame = ctk.CTkFrame(self,fg_color="transparent",height=100,corner_radius=0)
        self.up_frame.pack(side="top",fill="x")
        
        self.up_frame_title = ctk.CTkLabel(self.up_frame,font=("Arial",50,"bold"),text="Configuración",anchor="w",text_color="#050D1F")
        self.up_frame_title.pack(padx=20,pady=20,anchor="w")
        self.up_frame_text = ctk.CTkLabel(self.up_frame,font=("Arial",15),justify="left",text="Desde aquí puedes definir el dispositivo de entrada de audio, el idioma de transcripción, el nivel de calidad del modelo y el formato del resumen generado.",wraplength=1,anchor="w",text_color="#050D1F")
        self.up_frame_text.pack(padx=20,pady=(0,20),anchor="w",fill="x")
        self.up_frame.bind("<Configure>", self.ajustar_wrap)
        
        #Frame main
        self.main_frame = ctk.CTkFrame(self,fg_color="transparent",corner_radius=0,height=400)
        self.main_frame.pack(side="top",fill="x",pady=(0,20))
        
        self.main_frame_TxtbxTitle = ctk.CTkLabel(self.main_frame,font=("Arial",25,"bold"),text="AI Prompt",anchor="w",text_color="#050D1F")
        self.main_frame_TxtbxTitle.pack(padx=20,pady=(0,20),anchor="w",fill="x")
        self.main_frame_txtbx = ctk.CTkTextbox(self.main_frame,600,height=100,corner_radius=10,fg_color="white",text_color="#262525",border_color="#454545")
        self.main_frame_txtbx.pack(padx=30,pady=10,anchor="w")
        default_prompt = """Eres un asistente experto en análisis, redacción y estructuración de información.

Vas a recibir una transcripción de audio que puede contener:
- Errores gramaticales
- Frases incompletas
- Ideas desordenadas
- Muletillas
- Información mal expresada o poco clara

Tu tarea es transformar esa transcripción en un documento claro, profesional y útil.

INSTRUCCIONES OBLIGATORIAS:

1. Corrige todos los errores de redacción propios del habla.
2. Interpreta correctamente frases mal estructuradas o confusas.
3. Si una idea está mal explicada pero se puede deducir su intención, reescríbela correctamente.
4. Elimina muletillas, repeticiones, ruido verbal o información irrelevante.
5. Identifica el TEMA PRINCIPAL del contenido.
6. Identifica SUBTEMAS importantes.
7. Amplía conceptos clave con información útil y precisa (sin inventar datos irreales).
8. Si el contenido menciona procesos, pasos o explicaciones, organízalos de forma lógica.
9. Si hay ideas sueltas, intégralas en la sección que corresponda.
10. Convierte el resultado en un texto estructurado, coherente y fácil de leer.

FORMATO DE SALIDA (OBLIGATORIO):

TÍTULO:
(Un título claro basado en el tema principal)

TEMA PRINCIPAL:
(Explicación clara del núcleo del contenido)

SUBTEMAS Y DESARROLLO:
(Subtema 1)
- Explicación ampliada

(Subtema 2)
- Explicación ampliada

(..Si es necesario incluye mas)

PUNTOS CLAVE:
- Punto importante 1
- Punto importante 2
- Punto importante 3

CONCLUSIÓN:
(Resumen final del contenido ya mejorado)

REGLAS IMPORTANTES:
- NO expliques lo que estás haciendo.
- NO menciones que es una transcripción.
- NO incluyas instrucciones.
- NO agregues texto fuera del formato.
- SOLO devuelve el documento final estructurado.

"""
        self.main_frame_txtbx.insert("1.0", default_prompt)
        
        ##################################################################################Frame footer
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.footer_frame.pack(side="top", fill="x")

        # 🔥 columnas proporcionales
        self.footer_frame.grid_columnconfigure((0,1,2), weight=1)
        self.footer_frame.grid_rowconfigure(0, weight=1)
        
        self.footer_frame_left = ctk.CTkFrame(self.footer_frame, fg_color="transparent", corner_radius=0)
        self.footer_frame_left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.footer_frame_center = ctk.CTkFrame(self.footer_frame, fg_color="transparent")
        self.footer_frame_center.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.footer_frame_center.grid_columnconfigure(0, weight=1)
        self.footer_frame_center.grid_rowconfigure(2, weight=1)  # 👈 ESTA FILA EMPUJA TODO



        self.footer_frame_right = ctk.CTkFrame(self.footer_frame, fg_color="transparent", corner_radius=0)
        self.footer_frame_right.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        
        self.footer_frame_left.grid_columnconfigure(0, weight=1)
        ##################################################################################Frame footer items
        self.footer_frame_Mic_title = ctk.CTkLabel(
            self.footer_frame_left, font=("Arial", 22, "bold"),
            text="Micrófono", anchor="w", text_color="#050D1F"
        )
        self.footer_frame_Mic_title.grid(row=0, column=0, padx=30, pady=(10,30), sticky="w")

        self.mic_var = ctk.StringVar(value="Seleccionar micrófono")

        self.footer_frame_Mic_option = ctk.CTkOptionMenu(
            self.footer_frame_left,
            values=dispositivos_entrada(),
            variable=self.mic_var,
            width=200
        )
        self.footer_frame_Mic_option.grid(row=1, column=0, padx=30, pady=10, sticky="w")
        
        self.footer_frame_center.grid_columnconfigure(0, weight=1)

        self.footer_frame_Lan_title = ctk.CTkLabel(
            self.footer_frame_center, font=("Arial", 22, "bold"),
            text="Lenguaje", anchor="w", text_color="#050D1F"
        )
        self.footer_frame_Lan_title.grid(row=0, column=0, padx=30, pady=(10,30), sticky="w")

        self.footer_frame_Lan_option = ctk.CTkOptionMenu(
            self.footer_frame_center,
            values=["Español","Inglés"],
            width=180
        )
        self.footer_frame_Lan_option.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        
        
        self.footer_frame_right.grid_columnconfigure(0, weight=1)

        self.footer_frame_Cal_title = ctk.CTkLabel(
            self.footer_frame_right, font=("Arial", 22, "bold"),
            text="Calidad de transcripción",
            anchor="w", text_color="#050D1F", wraplength=180
        )
        self.footer_frame_Cal_title.grid(row=0, column=0, padx=20, pady=(10,10), sticky="w")

        self.footer_frame_Cal_option = ctk.CTkOptionMenu(
            self.footer_frame_right,
            values=["Baja (4GB RAM)","Media (4GB RAM)","Alta (8GB RAM)"],
            width=200
        )
        self.footer_frame_Cal_option.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.footer_frame_Cal_option.set("Alta (8GB RAM)")
        
        ##################################################################################Frame last
        
        self.last_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.last_frame.pack(side="top", fill="x")
        
        # 🔥 columnas proporcionales
        self.last_frame.grid_columnconfigure((0,1,2), weight=1)
        self.last_frame.grid_rowconfigure(0, weight=1)
        
        self.last_frame_left = ctk.CTkFrame(self.last_frame, fg_color="transparent", corner_radius=0)
        self.last_frame_left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.last_frame_center = ctk.CTkFrame(self.last_frame, fg_color="transparent")
        self.last_frame_center.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.last_frame_center.grid_columnconfigure(0, weight=1)
        self.last_frame_center.grid_rowconfigure(2, weight=1)  # 👈 ESTA FILA EMPUJA TODO

        self.last_frame_right = ctk.CTkFrame(self.last_frame, fg_color="transparent", corner_radius=0)
        self.last_frame_right.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        
        self.last_frame_left.grid_columnconfigure(0, weight=1)

        self.last_frame_Trans_title = ctk.CTkLabel(
            self.last_frame_left, font=("Arial", 22, "bold"),
            text="Modo de transcripción", anchor="w", text_color="#050D1F"
        )
        self.last_frame_Trans_title.grid(row=0, column=0, padx=30, pady=(10,30), sticky="w")

        self.last_frame_Trans_option = ctk.CTkOptionMenu(
            self.last_frame_left,
            values=["Automático","Manual"],
            width=180
        )
        self.last_frame_Trans_option.grid(row=1, column=0, padx=(40,30), pady=10, sticky="w")
        
        self.last_frame_Res_title = ctk.CTkLabel(
            self.last_frame_center, font=("Arial", 22, "bold"),
            text="Modo de resumen", anchor="w", text_color="#050D1F"
        )
        self.last_frame_Res_title.grid(row=0, column=0, padx=(5,40), pady=(10,30), sticky="w")

        self.last_frame_Res_option = ctk.CTkOptionMenu(
            self.last_frame_center,
            values=["Automático","Manual"],
            width=180
        )
        self.last_frame_Res_option.grid(row=1, column=0, padx=(5,50), pady=10, sticky="w")
        self.last_frame_Res_option.set("Manual")
        
        self.last_frame_Mod_title = ctk.CTkLabel(
            self.last_frame_right, font=("Arial", 22, "bold"),
            text="Modelo de Ollama", anchor="w", text_color="#050D1F"
        )
        self.last_frame_Mod_title.grid(row=0, column=0, padx=(5,40), pady=(10,30), sticky="w")
        modelos_disponibles = [
                "llama3.2",       # tu modelo principal
                "mistral",
                "qwen2.5",
                "phi3",
                "gemma2",
                "llava",
                "deepcoder",
                "starcoder",
                "vicuna",
                "falcon"
            ]
        self.last_frame_Mod_option = ctk.CTkOptionMenu(
            self.last_frame_right,
            values=modelos_disponibles,
            width=180
        )
        self.last_frame_Mod_option.grid(row=1, column=0, padx=(5,50), pady=10, sticky="w")
        
        self.accept_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.accept_frame.pack(side="top", fill="both", expand=True)
        
        self.btn_accept = ctk.CTkButton(
            self.accept_frame,
            text="Aceptar",
            fg_color="#47DC3A",
            text_color="#E3E6E5",
            hover_color="#93CEA1",
            font=("Arial",15,"bold"),
            corner_radius=8,
            height=40,
            anchor="center"
        )
        self.btn_accept.pack(pady=10)
        self.btn_accept.configure(command=self.guardar_config)
        if os.path.exists("config.json"):
            self.cargar_config()
            self.guardar_config()
        
    def guardar_config(self):
        
        idioma = self.footer_frame_Lan_option.get()
        self.prompt = self.main_frame_txtbx.get("1.0", "end").strip()
        calidad = self.footer_frame_Cal_option.get()
        mic = self.mic_var.get()      
        transcrip = self.last_frame_Trans_option.get()
        res = self.last_frame_Res_option.get()
        model = self.last_frame_Mod_option.get()
        selectMap = {
            "Automático":1,
            "Manual":0
        }
        self.controller.Transcriber_mode = selectMap[transcrip]
        self.controller.Resumer_mode = selectMap[res]
        if " - " in mic:
            index = int(mic.split(" - ")[0])
            self.controller.Grabadora.config(index)
        self.controller.Resumidor.config(model,self.prompt)
        self.controller.Transcriber.config(calidad,idioma)
        self.guardar_datos_json(self.prompt,transcrip,calidad,res)
    def guardar_datos_json(self,AIprompt,transcriber_mode,calidad_trans,resumer):
        config = {
            "AI_prompt": AIprompt,
            "Transcriber_mode": transcriber_mode,
            "Calidad_trans": calidad_trans,
            "Resumer_mode": resumer
        }
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
        
    def cargar_config(self):
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                config = json.load(f)

            Prompt = config.get("AI_prompt", "Resume el siguiente texto")

            Resumer_mode = (
                config.get("Resumer_mode", "Manual")
                if config.get("Resumer_mode") in ("Automático", "Manual")
                else "Manual"
            )

            Transcriber_mode = (
                config.get("Transcriber_mode", "Manual")
                if config.get("Transcriber_mode") in ("Automático", "Manual")
                else "Manual"
            )

            Cality_mode = (
                config.get("Calidad_trans", "Media (4GB RAM)")
                if config.get("Calidad_trans") in (
                    "Baja (4GB RAM)",
                    "Media (4GB RAM)",
                    "Alta (8GB RAM)"
                )
                else "Media (4GB RAM)"
            )

            self.main_frame_txtbx.delete("1.0", "end")
            self.main_frame_txtbx.insert("1.0", Prompt)

            self.footer_frame_Cal_option.set(Cality_mode)
            self.last_frame_Trans_option.set(Transcriber_mode)
            self.last_frame_Res_option.set(Resumer_mode)

        except (FileNotFoundError, json.JSONDecodeError):
            # defaults seguros
            self.main_frame_txtbx.delete("1.0", "end")
            self.main_frame_txtbx.insert("1.0", "Resume el siguiente texto")

            self.footer_frame_Cal_option.set("Media (4GB RAM)")
            self.last_frame_Trans_option.set("Manual")
            self.last_frame_Res_option.set("Manual")

    def ajustar_wrap(self, event):
        nuevo_ancho = event.width - 40
        self.up_frame_text.configure(wraplength=nuevo_ancho)


        
class Grabador(ctk.CTkFrame):
    def __init__(self,parent,controller):
        super().__init__(parent,fg_color="#C0EFDE",corner_radius=0)
        self.controller = controller

        self.esta_grabando = False  

        size = 300
        pad = 40
        center = size // 2

        self.canvas = ctk.CTkCanvas(self, width=size, height=size, bg="#C0EFDE", highlightthickness=0)
        self.canvas.pack(pady=40)

        self.circle = self.canvas.create_oval(pad, pad, size-pad, size-pad, fill="white",outline="")
        self.mic_icon = self.canvas.create_text(center, center, text="Iniciar", font=("Arial", 28, "bold"))


        self.canvas.tag_bind(self.circle, "<Button-1>", self.toggle_record)
        self.canvas.tag_bind(self.mic_icon, "<Button-1>", self.toggle_record)
        
        #Frame principal
        
        self.second_frame = ctk.CTkFrame(self,fg_color="transparent",corner_radius=0)
        self.second_frame.pack(fill="both",expand=True)
        
        self.counter_label = ctk.CTkLabel(self.second_frame,text="00:00:00",text_color="#000000",anchor="center",font=("Arial",20,"bold")) #HORAS:MINUTOS:SEGUNDOS
        self.counter_label.pack(padx=20,pady=(20,40))
        self.segundos =0
        self.minutos = 0
        self.horas = 0
        self.actualizar_contador()
        
        self.alert_label = ctk.CTkLabel(self.second_frame,text="",text_color="#EF0D0D",anchor="center",font=("Arial",30,"bold")) #HORAS:MINUTOS:SEGUNDOS
        self.alert_label.pack(padx=20,pady=(30,20))
        
    def actualizar_contador(self):
        if self.esta_grabando:  # solo cuenta si está grabando
            self.segundos += 1

            if self.segundos == 60:
                self.segundos = 0
                self.minutos += 1

            if self.minutos == 60:
                self.minutos = 0
                self.horas += 1

            tiempo = f"{self.horas:02}:{self.minutos:02}:{self.segundos:02}"
            self.counter_label.configure(text=tiempo)
        self.after(1000, self.actualizar_contador)  # se vuelve a llamar sola

    def toggle_record(self, event=None):
        if self.controller.Grabadora.device_num !=-1:
            self.esta_grabando = not self.esta_grabando

            if self.esta_grabando:
                self.canvas.itemconfig(self.circle, fill="#FF4C4C")
                self.canvas.itemconfig(self.mic_icon, fill="white",text="Detener", font=("Arial", 28, "bold"))
                self.controller.Grabadora.iniciar_grabacion()   # tu función real
            else:
                self.canvas.itemconfig(self.circle, fill="white")
                self.canvas.itemconfig(self.mic_icon, fill="black",text="Iniciar", font=("Arial", 28, "bold"))
                self.horas = self.minutos = self.segundos = 0
                self.counter_label.configure(text="00:00:00",text_color="#000000",font=("Arial",20,"bold"))
                filename = self.controller.Grabadora.detener_grabacion()
                if filename: # tu función real
                    if self.controller.Transcriber_mode ==1:
                        self.alert_label.configure(text="Espere un momento.. se estra transcribiendo el audio",text_color="#154112",font=("Arial",20,"bold"))
                        self.update_idletasks()
                        archivo = self.controller.Transcriber.transcribir_audio(filename)
                        self.alert_label.configure(text="✅ Audio transcrito y guardado con exito",text_color="#154112",font=("Arial",20,"bold"))
                        self.after(3000, lambda: self.alert_label.configure(text=""))
                        if self.controller.Resumer_mode==1:
                            self.alert_label.configure(text="Espere un momento.. se estra resumiendo el audio",text_color="#154112",font=("Arial",20,"bold"))
                            self.update_idletasks()
                            resumir_archivo(self,archivo,"transcripts/")
                            self.after(3000, lambda: self.alert_label.configure(text=""))    
                    else:
                        self.alert_label.configure(text="✅ Audio guardado con exito",text_color="#154112",font=("Arial",20,"bold"))
                        self.after(3000, lambda: self.alert_label.configure(text=""))
                else:
                    self.alert_label.configure(text="❌ Error al guardar el audio",text_color="#D63838",font=("Arial",20,"bold"))
                    self.after(3000, lambda: self.alert_label.configure(text=""))
        else:
            self.alert_label.configure(text="⚠️ Seleccioné un microfono adecuado en la ventana de configuración.",text_color="#EA7979")
            self.after(3000, lambda: self.alert_label.configure(text=""))

class Audios(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#D9E3E9", corner_radius=0) # Color similar a tu imagen
        self.controller = controller
        
        self.label = ctk.CTkLabel(self, text="Mis Audios", font=("Arial", 40, "bold"), text_color="#2C3E50")
        self.label.pack(pady=20)

        # Contenedor con scroll (el cuadro blanco de tu imagen)
        self.lista_archivos = ctk.CTkScrollableFrame(self, fg_color="white", corner_radius=15, width=450, height=500)
        self.lista_archivos.pack(pady=20, padx=65, fill="both", expand=True)
        self.last_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.last_frame.pack(fill="both", expand=True)
        
        self.btn_rec = ctk.CTkButton(
            self.last_frame,
            text="Recargar",
            fg_color="#349AAC",
            text_color="#E3E6E5",
            hover_color="#B8FAF7",
            font=("Arial",16,"bold"),
            corner_radius=8,
            height=40,
            anchor="center"
        )
        self.btn_rec.pack(padx=20,pady=(20,30))
        self.btn_rec.configure(command=self.cargar_lista)
        
        self.btn_alert = ctk.CTkLabel(self.last_frame,text="",text_color="#0E6640",font=("Arial",20,"bold"))##D42A2A
        self.btn_alert.pack()
        
        self.cargar_lista()
        
    def mostrar_menu2(self,event):
        self.menu2.tk_popup(event.x_root,event.y_root)
        
    def cargar_lista(self):
        for widget in self.lista_archivos.winfo_children():
            widget.destroy()

        ruta = "recordings/"
        if not os.path.exists(ruta):
            os.makedirs(ruta)

        archivos = os.listdir(ruta)

        self.menu2 = Tk.Menu(self,tearoff=0)
        self.menu2.add_command(label="📥 Importar archivo", command=lambda: importarArchivo(self,"recordings",[("Audios compatibles", "*.wav *.mp3 *.m4a *.flac *.ogg *.opus *.aac *.mp4 *.webm"),("WAV", "*.wav"),("MP3", "*.mp3"),]))
        self.menu2.add_separator()
        self.menu2.add_command(label="🔄 Recargar", command=lambda: self.cargar_lista())  
            
        if not archivos:
            label_vacio = ctk.CTkLabel(self.lista_archivos, text="No hay archivos guardados aún.", text_color="gray")
            label_vacio.pack(pady=20)
            self.Frame_archivos = ctk.CTkFrame(self.lista_archivos,height=500,fg_color="transparent")
            self.Frame_archivos.pack(fill="both",expand=True)   
            self.Frame_archivos.bind("<Button-3>", lambda event: self.usarMenu2(event))
            return
        
        self.archivo = ""
        self.menu = Tk.Menu(self,tearoff=0)
        self.menu.add_command(label="▶ Transcribir", command=lambda: self.transcribir_audio(self.archivo))
        self.menu.add_command(label="📂 Abrir archivo", command=lambda: abrir_carpeta(ruta))
        self.menu.add_separator()
        self.menu.add_command(label="🗑 Eliminar", command=lambda: borrar_archivo(self,self.archivo,ruta))
        #al indicar lambda permite que pongamos parametros, si no ponemos lambda y solo ponemos la funcion esta no podra recibir parametros (si intentamos poner aparametros dara error)
        
        
        
        for archivo in archivos:
            btn = ctk.CTkButton(
                self.lista_archivos, 
                text=f"🎙️   {archivo}", 
                anchor="w", # Texto alineado a la izquierda
                fg_color="transparent", 
                text_color="black",
                hover_color="#E0E0E0",
                height=40,
                font=("Arial", 16,"bold"),
            )
            btn.pack(fill="x", padx=5, pady=2)
            btn.bind("<Button-1>", lambda event, f=archivo: self.abrir_archivo(f, ruta))
            btn.bind("<Button-3>", lambda event, f=archivo: self.usarMenu(event,f))
        
        self.Frame_archivos = ctk.CTkFrame(self.lista_archivos,height=500,fg_color="transparent")
        self.Frame_archivos.pack(fill="both",expand=True)
        self.Frame_archivos.bind("<Button-3>", lambda event: self.usarMenu2(event))
        
    def usarMenu2(self,event):
        self.menu2.tk_popup(event.x_root,event.y_root)
        
    def usarMenu(self,event, nombre):
            self.archivo = nombre
            self.menu.tk_popup(event.x_root, event.y_root)

    def abrir_archivo(self, nombre_archivo, carpeta):
        ruta_completa = os.path.join(carpeta, nombre_archivo)
        try:
            os.startfile(os.path.abspath(ruta_completa))
        except Exception as e:
            print(f"Error al abrir: {e}")

    def transcribir_audio(self,nombre_archivo):
        self.btn_alert.configure(text="Espere un momento... se está transcribiendo el texto",text_color="#0E6640",font=("Arial",20,"bold"))
        self.update_idletasks()
        txt = self.controller.Transcriber.transcribir_audio(nombre_archivo)
        self.btn_alert.configure(text="",text_color="#0E6640",font=("Arial",20,"bold"))
        if txt =="":
            self.btn_alert.configure(text="!Error es posible que el audio no se haya transcrito correctamente!",text_color="#7B2323",font=("Arial",20,"bold"))
            self.update_idletasks()
            Tk.messagebox.showinfo("Aceptar", "!ERROR! No se pudo transcribir el audio correctamente (Es posible que no haya texto que transcribir).!")
        else:
            Tk.messagebox.showinfo("Aceptar", "!Audio transcrito con exito.!")
        self.btn_alert.configure(text="",text_color="#0E6640",font=("Arial",20,"bold"))

class Transcripciones(ctk.CTkFrame):
    def __init__(self,parent,controller):
        super().__init__(parent,fg_color="#A8E3E1",corner_radius=0)
        self.controller = controller
        super().__init__(parent, fg_color="#D9E3E9", corner_radius=0) # Color similar a tu imagen
        self.controller = controller
        
        self.label = ctk.CTkLabel(self, text="Mis Transcripciones", font=("Arial", 40, "bold"), text_color="#2C3E50")
        self.label.pack(pady=20)

        # Contenedor con scroll (el cuadro blanco de tu imagen)
        self.lista_archivos = ctk.CTkScrollableFrame(self, fg_color="white", corner_radius=15, width=450, height=500)
        self.lista_archivos.pack(pady=20, padx=65, fill="both", expand=True)

        self.last_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.last_frame.pack(fill="both", expand=True)
        
        self.btn_rec = ctk.CTkButton(
            self.last_frame,
            text="Recargar",
            fg_color="#349AAC",
            text_color="#E3E6E5",
            hover_color="#B8FAF7",
            font=("Arial",16,"bold"),
            corner_radius=8,
            height=40,
            anchor="center"
        )
        self.btn_rec.pack(padx=20,pady=(20,10))
        self.btn_rec.configure(command=self.cargar_lista)
        
        self.btn_alert = ctk.CTkLabel(self.last_frame,text="",text_color="#0E6640",font=("Arial",20,"bold"))##D42A2A
        self.btn_alert.pack()
        
        self.cargar_lista()
        
        

    def cargar_lista(self):
        for widget in self.lista_archivos.winfo_children():
            widget.destroy()

        ruta = "transcripts/"
        if not os.path.exists(ruta):
            os.makedirs(ruta)

        archivos = os.listdir(ruta)

        self.menu2 = Tk.Menu(self,tearoff=0)
        self.menu2.add_command(label="📥 Importar archivo", command=lambda: importarArchivo(self,"transcripts",[("Texto","*.txt")]))
        self.menu2.add_separator()
        self.menu2.add_command(label="🔄 Recargar", command=lambda: self.cargar_lista())
        
        if not archivos:
            label_vacio = ctk.CTkLabel(self.lista_archivos, text="No hay archivos guardados aún.", text_color="gray")
            label_vacio.pack(pady=20)
            self.Frame_archivos = ctk.CTkFrame(self.lista_archivos,height=500,fg_color="transparent")
            self.Frame_archivos.pack(fill="both",expand=True)
            self.Frame_archivos.bind("<Button-3>", lambda event: self.usarMenu2(event))
            return
        self.archivo_name = ""
        self.menu = Tk.Menu(self,tearoff=0)
        self.menu.add_command(label="📝 Resumir",command=lambda:  self.res(ruta))
        self.menu.add_command(label="📂 Abrir archivo",command=lambda: abrir_carpeta(ruta))
        self.menu.add_separator()
        self.menu.add_command(label="🗑 Eliminar", command=lambda: borrar_archivo(self,self.archivo_name,ruta))

        for archivo in archivos:
            btn = ctk.CTkButton(
                self.lista_archivos, 
                text=f"📄   {archivo}", 
                anchor="w", # Texto alineado a la izquierda
                fg_color="transparent", 
                text_color="black",
                hover_color="#E0E0E0",
                height=40,
                font=("Arial", 16,"bold"),
            )
            btn.pack(fill="x", padx=5, pady=2)
            btn.bind("<Button-1>", lambda event, f=archivo: self.abrir_archivo(f, ruta))
            btn.bind("<Button-3>", lambda event, f=archivo: self.usarMenu(event,f))
            
        self.Frame_archivos = ctk.CTkFrame(self.lista_archivos,height=500,fg_color="transparent")
        self.Frame_archivos.pack(fill="both",expand=True)
        self.Frame_archivos.bind("<Button-3>", lambda event: self.usarMenu2(event))
        
    def res(self,ruta):
        self.btn_alert.configure(text="Espere un momento.... se está resumiendo el texto.",text_color="#0E6640",font=("Arial",20,"bold"))
        self.update_idletasks()
        resumir_archivo(self,self.archivo_name,ruta)
        self.btn_alert.configure(text="",text_color="#0E6640",font=("Arial",20,"bold"))
        
    def usarMenu2(self,event):
        self.menu2.tk_popup(event.x_root,event.y_root)
            
    def usarMenu(self,event,archivo):
        self.archivo_name = archivo
        self.menu.tk_popup(event.x_root,event.y_root)

    def abrir_archivo(self, nombre_archivo, carpeta):
        ruta_completa = os.path.join(carpeta, nombre_archivo)
        try:
            os.startfile(os.path.abspath(ruta_completa))
        except Exception as e:
            print(f"Error al abrir: {e}")
            
    def borrar_archivo(self,nombre_archivo,carpeta):
        confirmacion = Tk.messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar {nombre_archivo}?")
        if confirmacion:
            ruta_completa = os.path.join(carpeta, nombre_archivo)
            try:
                if os.path.exists(ruta_completa):
                    os.remove(ruta_completa)
                    self.cargar_lista() 
            except Exception as e:
                print(f"Error al borrar: {e}")

def resumir_archivo(self, nombre_archivo, carpeta):
        try:
            ruta_completa = os.path.join(carpeta, nombre_archivo)
            
            with open(ruta_completa, "r", encoding="utf-8") as f:
                contenido = f.read()
            resumen = self.controller.Resumidor.resumir(contenido)
            carpeta_salida = "summaries/"
            os.makedirs(carpeta_salida, exist_ok=True)
            if resumen == "Error":
                Tk.messagebox.showwarning(title="Error de resumen", message="Es posible que no cuente con Ollama instalado, o el modelo seleccionado no esta descargado.")
                return
            salida = os.path.join(carpeta_salida, nombre_archivo)
            
            try:
                texto = resumen.message.content  # extrae solo el contenido de texto
            except AttributeError:
                texto = getattr(resumen, 'content', str(resumen))
            
            
            with open(salida, "w", encoding="utf-8") as f_salida:
                f_salida.write(texto)
            Tk.messagebox.showinfo(title="Resumen correctamente hecho", message="!Se ha realizado el resumen exitosamente.")

        except FileNotFoundError:
            return f"Error: el archivo '{nombre_archivo}' no existe en la carpeta '{carpeta}'"
        except Exception as e:
            return Tk.messagebox.showwarning(title="IA NO INSTALADA", message="Su dispositivo no cuenta con Ollama y algún modelo de este instalado.")
        
class Resumenes(ctk.CTkFrame):
    def __init__(self,parent,controller):
        super().__init__(parent,fg_color="#A8E3E1",corner_radius=0)
        self.controller = controller
        super().__init__(parent, fg_color="#D9E3E9", corner_radius=0) # Color similar a tu imagen
        self.controller = controller
        
        self.label = ctk.CTkLabel(self, text="Mis Resumenes", font=("Arial", 40, "bold"), text_color="#2C3E50")
        self.label.pack(pady=20)

        # Contenedor con scroll (el cuadro blanco de tu imagen)
        self.lista_archivos = ctk.CTkScrollableFrame(self, fg_color="white", corner_radius=15, width=450, height=500)
        self.lista_archivos.pack(pady=20, padx=65, fill="both", expand=True)

        self.last_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.last_frame.pack(fill="both", expand=True)
        
        self.btn_rec = ctk.CTkButton(
            self.last_frame,
            text="Recargar",
            fg_color="#349AAC",
            text_color="#E3E6E5",
            hover_color="#B8FAF7",
            font=("Arial",16,"bold"),
            corner_radius=8,
            height=40,
            anchor="center"
        )
        self.btn_rec.pack(padx=20,pady=(20,30))
        self.btn_rec.configure(command=self.cargar_lista)
        self.cargar_lista()
        

    def cargar_lista(self):
        for widget in self.lista_archivos.winfo_children():
            widget.destroy()

        ruta = "summaries/"
        if not os.path.exists(ruta):
            os.makedirs(ruta)

        archivos = os.listdir(ruta)
        self.menu2 = Tk.Menu(self,tearoff=0)
        self.menu2.add_command(label="📥 Importar archivo", command=lambda: importarArchivo(self,"summaries"))
        self.menu2.add_separator()
        self.menu2.add_command(label="🔄 Recargar", command=lambda: self.cargar_lista())
        
        if not archivos:
            label_vacio = ctk.CTkLabel(self.lista_archivos, text="No hay archivos guardados aún.", text_color="gray")
            label_vacio.pack(pady=20)
            self.Frame_archivos = ctk.CTkFrame(self.lista_archivos,height=500,fg_color="transparent")
            self.Frame_archivos.pack(fill="both",expand=True)
            self.Frame_archivos.bind("<Button-3>", lambda event: self.usarMenu2(event))
            return

        self.archivo_name = ""
        self.menu = Tk.Menu(self,tearoff=0)
        self.menu.add_command(label="📂 Abrir archivo",command=lambda: abrir_carpeta(ruta))
        self.menu.add_separator()
        self.menu.add_command(label="🗑 Eliminar", command=lambda: borrar_archivo(self,self.archivo_name,ruta))
        
        
        
        for archivo in archivos:
            btn = ctk.CTkButton(
                self.lista_archivos, 
                text=f"📝   {archivo}", 
                anchor="w", # Texto alineado a la izquierda
                fg_color="transparent", 
                text_color="black",
                hover_color="#E0E0E0",
                height=40,
                font=("Arial", 16,"bold"),
            )
            btn.pack(fill="x", padx=5, pady=2)
            btn.bind("<Button-1>", lambda event, f=archivo: self.abrir_archivo(f, ruta))
            btn.bind("<Button-3>", lambda event, f=archivo: self.usarMenu(event,f))
            
        self.Frame_archivos = ctk.CTkFrame(self.lista_archivos,height=500,fg_color="transparent")
        self.Frame_archivos.pack(fill="both",expand=True)
        self.Frame_archivos.bind("<Button-3>", lambda event: self.usarMenu2(event))
        
    def usarMenu2(self,event):
        self.menu2.tk_popup(event.x_root,event.y_root)
            
    def usarMenu(self,event,archivo):
        self.archivo_name = archivo
        self.menu.tk_popup(event.x_root,event.y_root)

    def abrir_archivo(self, nombre_archivo, carpeta):
        ruta_completa = os.path.join(carpeta, nombre_archivo)
        try:
            os.startfile(os.path.abspath(ruta_completa))
        except Exception as e:
            print(f"Error al abrir: {e}")
            
    def borrar_archivo(self,nombre_archivo,carpeta):
        confirmacion = Tk.messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar {nombre_archivo}?")
        if confirmacion:
            ruta_completa = os.path.join(carpeta, nombre_archivo)
            try:
                if os.path.exists(ruta_completa):
                    os.remove(ruta_completa)
                    self.cargar_lista() 
            except Exception as e:
                print(f"Error al borrar: {e}")
                
def abrir_carpeta(carpeta):
        ruta = os.path.abspath(carpeta)

        if sys.platform == "win32":
            subprocess.Popen(f'explorer "{ruta}"')
        elif sys.platform == "darwin":
            subprocess.Popen(["open", ruta])
        else:  # Linux
            subprocess.Popen(["xdg-open", ruta])

def borrar_archivo(parent,nombre_archivo,carpeta):
        confirmacion = Tk.messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar {nombre_archivo}?")
        if confirmacion:
            ruta_completa = os.path.join(carpeta, nombre_archivo)
            try:
                if os.path.exists(ruta_completa):
                    os.remove(ruta_completa)
                    parent.cargar_lista() 
            except Exception as e:
                print(f"Error al borrar: {e}")  

def nav_button(parent, text, color):
        return ctk.CTkButton(
        parent,
        text=text,
        fg_color="#FFFFFF",
        text_color=color,
        hover_color="#E8EEF2",
        corner_radius=8,
        border_width=1,
        border_color="#C5D3DC",
        height=40
        )

def importarArchivo(parent,carpeta,sfiletypes=[("Todos","*.*")]):
    ruta_archivo = Tk.filedialog.askopenfilename(title="Selecciona un archivo.",filetypes=sfiletypes)
    if not ruta_archivo: 
        return
    
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    
    nombre_archivo = os.path.basename(ruta_archivo)
    ruta_destino = os.path.join(carpeta,nombre_archivo)
    
    shutil.copy2(ruta_archivo,ruta_destino)
    parent.cargar_lista() 