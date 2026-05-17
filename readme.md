# 🎙️ NotesIA

> **Graba. Transcribe. Resume.** — Todo desde tu computadora, sin internet, sin suscripciones.

NotesIA es una aplicación de escritorio construida en Python que te permite **grabar audio**, **transcribirlo automáticamente** con Whisper y **resumirlo con IA local** usando Ollama. Pensada para estudiantes, investigadores, periodistas o cualquiera que necesite convertir su voz en notas estructuradas de forma rápida y privada.

---

## 🖼️ Vista previa

> ![Pantalla principal](assets/inicio.png)
> ![Pantalla grabar audios](assets/grabar.png)
> ![Pantalla grabaciones](assets/audios.png)
> ![Pantalla transcripciones](assets/transcripciones.png)
> ![Pantalla resumenes](assets/resumenes.png)

---

## ✨ Características

- 🎙️ **Grabación de audio** directamente desde el micrófono seleccionado
- 📝 **Transcripción automática** con [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (modelos tiny, base, small)
- 🤖 **Resumen estructurado con IA local** mediante [Ollama](https://ollama.com/) — sin enviar datos a la nube
- 📂 **Gestión de archivos**: audios, transcripciones y resúmenes organizados en carpetas
- ⚙️ **Configuración persistente** guardada en `config.json`
- 🌐 Soporte para **Español e Inglés**
- 💻 Interfaz gráfica moderna con [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python **3.11.9** (recomendado) | Lenguaje principal |
| [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) | Interfaz gráfica |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | Transcripción de audio con Whisper (OpenAI) |
| [sounddevice](https://python-sounddevice.readthedocs.io/) | Captura de audio del micrófono |
| [scipy](https://scipy.org/) | Escritura de archivos WAV |
| [numpy](https://numpy.org/) | Procesamiento de arrays de audio |
| [Ollama](https://ollama.com/) | Ejecución local de modelos LLM |
| [ollama (Python SDK)](https://github.com/ollama/ollama-python) | Comunicación con la API de Ollama |

---

## 📋 Requisitos previos

### 1. Python — versión exacta recomendada: **3.11.9**

> ⚠️ **Lee esto antes de instalar Python, en serio.**

Descarga específicamente la versión **3.11.9** desde → [https://www.python.org/downloads/release/python-3119/](https://www.python.org/downloads/release/python-3119/)

**¿Por qué no la versión más nueva (3.12, 3.13...)?**

NotesIA depende de `faster-whisper` y su motor interno `ctranslate2`, librerías de IA que están compiladas en C++ y que son extremadamente sensibles a la versión de Python. Cuando sale una versión nueva de Python, estas librerías tardan **meses** en actualizar sus compilaciones para ser compatibles. Intentar instalarlas en Python 3.12+ muy probablemente resulte en errores de instalación o fallos en tiempo de ejecución.

**Python 3.11.9 es la versión más estable para este stack (Whisper + ML + CustomTkinter) a día de hoy. No cambies de versión.**

Sobre el `pip`: Python 3.11.9 viene empaquetado con **pip 24**, que es exactamente lo que necesitas. No es necesario actualizarlo.

```bash
# Verifica que tienes la versión correcta después de instalar
python --version
# Debe mostrar: Python 3.11.9
```

### 2. Ollama (para la función de resumen)
NotesIA usa **Ollama** para resumir transcripciones de forma local. Debes instalarlo por separado:

1. Descarga e instala Ollama desde → [https://ollama.com/download](https://ollama.com/download)
2. Una vez instalado, descarga el modelo que prefieras. El modelo por defecto en la app es `llama3.2`:

```bash
ollama pull llama3.2
```

**Modelos compatibles disponibles en la app:**

| Modelo | Descripción | RAM recomendada |
|---|---|---|
| `llama3.2` ⭐ *(por defecto)* | Buena calidad general | ~4-6 GB |
| `mistral` | Rápido y eficiente | ~4 GB |
| `qwen2.5` | Multilingüe, excelente en español | ~4-6 GB |
| `phi3` | Ligero y rápido | ~2-3 GB |
| `gemma2` | Modelo de Google, buena calidad | ~5 GB |
| `llava` | Multimodal (texto + imágenes) | ~4 GB |

> ⚠️ **Nota**: Ollama debe estar **corriendo en segundo plano** (`ollama serve`) para que la función de resumen funcione. Si instalas Ollama en Windows/macOS, esto ocurre automáticamente al iniciar sesión.

---

## 🚀 Instalación y uso

### Clonar el repositorio

```bash
git clone https://github.com/Lexor12/NotesIA.git
cd NotesIA
```

### Instalar dependencias de Python

Se recomienda usar un entorno virtual:

```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (macOS / Linux)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecutar la aplicación

```bash
python main.py
```

---

## 📦 Compilar como ejecutable (.exe / binario)

Si quieres distribuir la app sin que el usuario necesite Python instalado, puedes compilarla con **PyInstaller**.

### 1. Instalar PyInstaller

```bash
pip install pyinstaller
```

### 2. Compilar

```bash
pyinstaller --onefile --windowed --name "NotesIA" main.py
```

**Flags explicados:**
- `--onefile` → Genera un solo archivo ejecutable
- `--windowed` → No muestra la consola de fondo (ideal para apps con GUI)
- `--name "NotesIA"` → Nombre del ejecutable generado

El ejecutable aparecerá en la carpeta `dist/`.

### 3. Incluir recursos adicionales (si aplica)

Si la app necesita acceder a carpetas como `recordings/`, `transcripts/` o `summaries/`, estas se crean automáticamente al ejecutar. No necesitas incluirlas manualmente.

> ⚠️ **Importante al compilar**: faster-whisper descarga los modelos de Whisper en la primera ejecución. El usuario necesitará conexión a internet la primera vez que use cada nivel de calidad. Los modelos se guardan en caché localmente después.

---

## 📁 Estructura del proyecto

```
NotesIA/
│
├── main.py                 # Punto de entrada
├── requirements.txt        # Dependencias Python
├── config.json             # Configuración guardada (generado automáticamente)
│
├── lib/
│   ├── recorder.py         # Grabación de audio (sounddevice)
│   ├── transcriber.py      # Transcripción (faster-whisper)
│   └── ollamacon.py        # Conexión con Ollama
│
├── gui/
│   └── app_gui.py          # Interfaz gráfica (CustomTkinter)
│
├── recordings/             # Audios grabados (generado automáticamente)
├── transcripts/            # Transcripciones generadas (generado automáticamente)
└── summaries/              # Resúmenes generados (generado automáticamente)
```

---

## ⚙️ Configuración de la app

Al abrir la app por primera vez ve a la sección **Configuración** y ajusta:

| Opción | Descripción |
|---|---|
| **Micrófono** | Selecciona el dispositivo de entrada de audio |
| **Lenguaje** | Español o Inglés para la transcripción |
| **Calidad de transcripción** | Baja (tiny) / Media (base) / Alta (small) |
| **Modo de transcripción** | Automático (al terminar de grabar) o Manual |
| **Modo de resumen** | Automático o Manual |
| **Modelo de Ollama** | El LLM que se usará para resumir |
| **AI Prompt** | Personaliza cómo la IA estructura el resumen |

---

## 🔒 Privacidad y seguridad

- ✅ **Todo corre 100% localmente** — ningún audio, transcripción o resumen se envía a servidores externos
- ✅ **Sin claves API** — no se requieren cuentas ni tokens
- ✅ **Sin telemetría** — la app no recopila ningún dato
- El archivo `config.json` contiene tu prompt personalizado y preferencias. Está en el `.gitignore` por defecto

---

## 🐛 Problemas comunes

**La transcripción no funciona:**
- Verifica que seleccionaste un micrófono válido en Configuración
- Asegúrate de que el archivo de audio no esté vacío

**El resumen da error:**
- Verifica que Ollama esté corriendo: abre una terminal y escribe `ollama list`
- Asegúrate de haber descargado el modelo: `ollama pull llama3.2`

**La app no inicia:**
- Verifica que todas las dependencias estén instaladas: `pip install -r requirements.txt`
- Usa Python 3.10 o superior

---

## 👤 Autor

**Lexor12**
- GitHub: [@Lexor12](https://github.com/Lexor12)

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

> Hecho con 🎙️ y mucho café por **Lexor12**
