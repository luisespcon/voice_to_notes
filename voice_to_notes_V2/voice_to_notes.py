import os
import sys
import argparse
import asyncio
import aiohttp
import uuid
from pydub import AudioSegment
from datetime import datetime
import google.generativeai as genai
import json
import time

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

if HF_API_TOKEN is None:
    raise EnvironmentError("HF_API_TOKEN not found in environment variables.")

WHISPER_MODELS = {
    "tiny": "openai/whisper-tiny",
    "base": "openai/whisper-base",
    "small": "openai/whisper-small",
    "medium": "openai/whisper-medium",
    "large": "openai/whisper-large",
}

HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}


def fragment_audio(audio_path, chunk_dir):
    os.makedirs(chunk_dir, exist_ok=True)
    audio = AudioSegment.from_file(audio_path)
    duration_ms = len(audio)

    if duration_ms <= 10 * 60 * 1000:
        output_path = os.path.join(chunk_dir, "chunk_0.mp3")
        audio.export(output_path, format="mp3")
        return [output_path]

    chunk_len = duration_ms // 4
    chunk_paths = []

    for i in range(4):
        start = i * chunk_len
        end = (i + 1) * chunk_len if i < 3 else duration_ms
        chunk = audio[start:end]
        path = os.path.join(chunk_dir, f"chunk_{i}.mp3")
        chunk.export(path, format="mp3")
        chunk_paths.append(path)

    return chunk_paths


async def transcribe_chunk(session, file_path, model_url):
    with open(file_path, "rb") as f:
        audio_data = f.read()

    async with session.post(model_url, headers=HEADERS, data=audio_data) as resp:
        if resp.status == 200:
            json_data = await resp.json()
            return json_data.get("text", "")
        else:
            error = await resp.text()
            return f"[ERROR] {resp.status}: {error}"


async def transcribe_all_chunks(chunk_paths, model):
    model_url = f"https://api-inference.huggingface.co/models/{WHISPER_MODELS[model]}"
    async with aiohttp.ClientSession() as session:
        tasks = [transcribe_chunk(session, path, model_url) for path in chunk_paths]
        return await asyncio.gather(*tasks)


def save_transcription(text, output_dir, base_name):
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{base_name}.txt")
    with open(path, "w") as f:
        f.write(text)
    print(f"Transcription saved to: {path}")
    return path


def create_obsidian_summary_only(gemini_summary, original_filename, output_path, gemini_model="gemini-1.5-flash"):
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M")

    markdown_content = f"""# Resumen de Clase - {original_filename}

## Metadatos
- **Fecha:** {current_date}
- **Hora:** {current_time}
- **Archivo original:** {original_filename}
- **Modelo IA:** {gemini_model}

## Resumen Ejecutivo
{gemini_summary.get('resumen_ejecutivo', 'No disponible')}

## Puntos Clave Principales
"""
    for punto in gemini_summary.get("puntos_clave", []):
        markdown_content += f"- {punto}\n"

    markdown_content += "\n## Conceptos Importantes\n"
    for concepto in gemini_summary.get("conceptos_importantes", []):
        markdown_content += f"- {concepto}\n"

    markdown_content += "\n## Preguntas y Dudas\n"
    for pregunta in gemini_summary.get("preguntas_dudas", []):
        markdown_content += f"- {pregunta}\n"

    markdown_content += "\n## Tareas y Acciones\n"
    for tarea in gemini_summary.get("tareas_acciones", []):
        markdown_content += f"- [ ] {tarea}\n"

    markdown_content += "\n## Detalles Adicionales\n"
    for detalle in gemini_summary.get("detalles_adicionales", []):
        markdown_content += f"- {detalle}\n"

    markdown_content += "\n## Estructura del Contenido\n"
    for estructura in gemini_summary.get("estructura_contenido", []):
        markdown_content += f"- {estructura}\n"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    print(f"Summary saved to: {output_path}")

def get_available_gemini_models():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    models = genai.list_models()
    return [model.name for model in models]

def generate_gemini_summary(text, model="gemini-1.5-flash"):
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found")
        return None

    genai.configure(api_key=api_key)

    prompt = f"""
Eres un asistente especializado en crear resúmenes académicos detallados en español.

Analiza esta transcripción y genera un resumen completo en español.

TRANSCRIPCIÓN:
{text}

Crea un análisis con:
1. RESUMEN EJECUTIVO: Un párrafo completo (3-5 oraciones) que capture la esencia de la sesión
2. PUNTOS CLAVE PRINCIPALES: Lista (3-8 puntos) con explicaciones de cada tema abordado
3. CONCEPTOS IMPORTANTES: Términos técnicos, teorías, definiciones importantes
4. PREGUNTAS Y DUDAS: Interrogantes, discusiones y puntos de reflexión mencionados
5. TAREAS Y ACCIONES: Exámenes, trabajos, fechas, entregas mencionadas
6. DETALLES ADICIONALES: Ejemplos dados, referencias mencionadas, datos específicos
7. ESTRUCTURA DEL CONTENIDO: Organización de los temas tratados

IMPORTANTE: Responde ÚNICAMENTE con un JSON válido usando estas claves exactas:
{{
    "resumen_ejecutivo": "string con párrafo detallado",
    "puntos_clave": ["explicación del punto 1", "explicación del punto 2"],
    "conceptos_importantes": ["concepto: explicación", "concepto: explicación"],
    "preguntas_dudas": ["pregunta con contexto", "pregunta con contexto"],
    "tareas_acciones": ["tarea específica", "acción específica"],
    "detalles_adicionales": ["ejemplo relevante", "dato específico"],
    "estructura_contenido": ["tema 1: descripción", "tema 2: descripción"]
}}

Solo JSON, sin texto adicional.
"""

    model_config = {
        "max_tokens": 4096,
        "temperature": 0.7,
    }

    generation_config = genai.types.GenerationConfig(
        max_output_tokens=model_config["max_tokens"],
        temperature=model_config["temperature"],
    )

    gemini_model = genai.GenerativeModel(model)

    time.sleep(2)  # Evitar rate limits

    try:
        response = gemini_model.generate_content(prompt, generation_config=generation_config)
        content = response.text.strip()

        if content.startswith('```json'):
            content = content[7:]
        elif content.startswith('```'):
            content = content[3:]
        if content.endswith('```'):
            content = content[:-3]

        summary_json = json.loads(content)

        required_keys = [
            "resumen_ejecutivo", "puntos_clave", "conceptos_importantes",
            "preguntas_dudas", "tareas_acciones", "detalles_adicionales", 
            "estructura_contenido"
        ]
        for key in required_keys:
            if key not in summary_json:
                summary_json[key] = []

        return summary_json

    except Exception as e:
        print(f"Error llamando a Gemini: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Transcribe audio using Hugging Face Whisper and summarize with Gemini.")
    parser.add_argument("audio_path", help="Path to audio file")
    parser.add_argument("--model", default="small", choices=WHISPER_MODELS.keys(), help="Whisper model to use")
    parser.add_argument("--output-dir", default="./output", help="Directory to save output files")
    args = parser.parse_args()

    base_name = os.path.splitext(os.path.basename(args.audio_path))[0]
    chunk_dir = "./chunks"
    chunk_paths = fragment_audio(args.audio_path, chunk_dir)

    print(f"Audio split into {len(chunk_paths)} chunk(s)")
    print(f"Sending chunks to Hugging Face API using model: {args.model}")

    transcriptions = asyncio.run(transcribe_all_chunks(chunk_paths, args.model))
    full_text = "\n\n".join(transcriptions)
    txt_path = save_transcription(full_text, args.output_dir, base_name)

    print("Sending full transcription to Gemini...")
    summary_json = generate_gemini_summary(full_text)
    summary_path = os.path.join(args.output_dir, f"{base_name}_resumen.md")
    create_obsidian_summary_only(summary_json, base_name, summary_path)


if __name__ == "__main__":
    main()