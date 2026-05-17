import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from datetime import datetime
import os

class Grabadora:
    def __init__(self):
        self.device_num = -1
        self.fs = 48000
        self.grabando = False
        self.audio_data = []
    
    def config(self,device_num):
        self.device_num = device_num
        self.fs = int(sd.query_devices(device_num)['default_samplerate'])
        
    def _callback(self, indata, frames, time, status):
        if self.grabando:
            self.audio_data.append(indata.copy())

    # INICIAR
    def iniciar_grabacion(self):
        print("[+] Grabando...")

        self.audio_data = []
        self.grabando = True

        self.stream = sd.InputStream(
            samplerate=self.fs,
            channels=1,
            dtype='int16',
            callback=self._callback,
            device=self.device_num
        )
        self.stream.start()

    # DETENER
    def detener_grabacion(self):
        if not self.grabando:
            return None

        print("[+] Deteniendo grabación")
        self.grabando = False
        self.stream.stop()
        self.stream.close()

        # Unimos todos los pedazos
        audio = np.concatenate(self.audio_data, axis=0)

        os.makedirs("recordings", exist_ok=True)
        filename = datetime.now().strftime("Grabacion_%Y%m%d_%H%M%S.wav")
        path_filename = os.path.join("recordings", filename)

        write(path_filename, self.fs, audio)

        print(f"[+] Guardado en {path_filename}")
        return filename

def dispositivos_entrada():
    devices = sd.query_devices()
    lista = []
    for i, device in enumerate(devices):
        if device['max_input_channels'] > 0:  # solo los que pueden grabar
            nombre = device['name']
            lista.append(f"{i} - {nombre}")  # 🔥 formato index - name
    if not lista:
        lista = ["No hay dispositivos de entrada"]
    return lista
"""
seleccion = self.mic_var.get()      
index = int(seleccion.split(" - ")[0]) (para obtener el index)
print(index)
"""