import ollama
import requests
import subprocess

class Resumidor:
    def __init__(self):
        self.model = "llama3.2"
        self.prompt = default_prompt = """Eres un asistente experto en análisis, redacción y estructuración de información.
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
    def config(self,model,prompt):
        self.model = model
        self.prompt = prompt
    
    @staticmethod
    def estaIAinstalada():
        try:
            r = requests.get("http://localhost:11434")
            return r.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def resumir(self, transcripcion: str) -> str:
        if not Resumidor.estaIAinstalada():
            return "Error"
        try:
            prompt_final = f"{self.prompt}\n*Aquí está la transcripción:*\n{transcripcion}"
            respuesta = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt_final}]
            )
            return respuesta
        except Exception as e:
            return "Error"