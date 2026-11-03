# ia_service.py
import os
import json
from groq import Groq

# El cliente se inicializa una vez
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def predecir_riesgo_pulmonar(datos_paciente: dict) -> dict:
    """
    Llama a Groq para estimar el nivel de riesgo de cáncer pulmonar.
    Retorna un diccionario con nivel_riesgo, probabilidad y texto_generado.
    """
    prompt = f"""Eres un asistente de triaje médico especializado en neumología.
Basándote en los siguientes datos clínicos de un paciente, estima el nivel de riesgo de cáncer pulmonar.

Datos del paciente:
- Edad: {datos_paciente['edad']} años
- Sexo: {datos_paciente['sexo']}
- Fumador: {'Sí' if datos_paciente['fumador'] else 'No'}
- Años fumando: {datos_paciente.get('anios_fumador', 0)}
- Tos crónica: {'Sí' if datos_paciente['tos_cronica'] else 'No'}
- Dificultad para respirar: {'Sí' if datos_paciente['dificultad_respirar'] else 'No'}

Responde ÚNICAMENTE en el siguiente formato JSON, sin texto adicional:
{{
  "nivel_riesgo": "Bajo" | "Medio" | "Alto",
  "probabilidad": <número entre 0 y 1>,
  "justificacion": "<breve explicación clínica en 1-2 oraciones>"
}}
"""
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",  # modelo gratuito y potente
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,  # baja temperatura para respuestas más deterministas
            max_completion_tokens=1000,
        )
        respuesta_texto = completion.choices[0].message.content.strip()

        # Limpiar posibles bloques de código markdown que el modelo pueda añadir
        if respuesta_texto.startswith("```"):
            respuesta_texto = respuesta_texto.split("```")[1]
            if respuesta_texto.startswith("json"):
                respuesta_texto = respuesta_texto[4:]
        respuesta_texto = respuesta_texto.strip()

        resultado = json.loads(respuesta_texto)

        return {
            "nivel_riesgo": resultado.get("nivel_riesgo", "Medio"),
            "probabilidad": float(resultado.get("probabilidad", 0.5)),
            "texto_generado": resultado.get("justificacion", respuesta_texto),
        }

    except json.JSONDecodeError:
        # Si el modelo no devolvió JSON válido, intentar extraer manualmente
        return {
            "nivel_riesgo": "Medio",
            "probabilidad": 0.5,
            "texto_generado": respuesta_texto,
        }
    except Exception as e:
        return {
            "nivel_riesgo": "Error",
            "probabilidad": 0.0,
            "texto_generado": f"Error al llamar a Groq: {str(e)}",
        }