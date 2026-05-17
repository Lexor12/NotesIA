# IA (Whisper)
from faster_whisper import WhisperModel
import os
import tkinter as Tk

class Transcriber:
    def __init__(self):
        self.model = None
        self.lan = "es"
        
    def config(self,mode,lan):
        self.setTranscriptionMod(mode)     
        self.lan = "es"
        
    def setTranscriptionMod(self,mode):
        modelo_map  = {
            "Baja (4GB RAM)":"tiny",
            "Media (4GB RAM)":"base",
            "Alta (8GB RAM)":"small"
        }
        if self.model:          #liberar modelo anterior
            del self.model
        self.model = WhisperModel(modelo_map[mode], device="cpu", compute_type="int8") 
        print("[+] Nuevo modelo cargado")
        
    def transcribir_audio(self,filename):
        try:
            path_filename = "recordings/" + filename
            
            if self.model == None:
                self.model = WhisperModel("base", device="cpu", compute_type="int8") 
                
            segments, info = self.model.transcribe(path_filename, language=self.lan)
            
            texto = ""
            for segment in segments:
                texto += segment.text + "\n"
            
            if not os.path.exists("transcripts"):
                os.makedirs("transcripts")

            nombre_base = os.path.splitext(filename)[0]
            txt_file = os.path.join("transcripts", nombre_base + ".txt")
            with open(txt_file, "w", encoding="utf-8") as f:
                f.write(texto.strip())
            return nombre_base + ".txt"
        except FileNotFoundError:
            Tk.messagebox.showerror("Error", "El archivo no existe.")

        except RuntimeError as e:
            Tk.messagebox.showerror("Error de modelo", f"No se pudo procesar el audio.\n{e}")

        except Exception as e:
            Tk.messagebox.showerror("Error inesperado", f"Ocurrió un problema:\n{e}")