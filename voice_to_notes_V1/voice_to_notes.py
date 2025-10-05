#!/usr/bin/env python3
"""
Voice Note Processor for Obsidian with Google Gemini
Automatically transcribes audio files using Whisper and generates intelligent summaries using Google Gemini.
Supports Gemini Pro models with free tier (15 requests/minute).

Generates 3 output files:
1. Detailed summary in Markdown format (Obsidian-optimized)
2. Transcription-only in Markdown format (Obsidian-optimized)
3. Plain text transcription
"""

import os
import sys
import subprocess
import argparse
import json
from datetime import datetime
from pathlib import Path
import google.generativeai as genai
import time

def transcribe_audio(audio_file, model="medium", output_dir="."):
    """
    Transcribe audio file using Whisper
    """
    try:
        cmd = [
            "whisper",
            audio_file,
            "--model", model,
            "--output_format", "txt",
            "--output_dir", output_dir
        ]
        
        print(f"Transcribing {audio_file} with model {model}...")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        audio_name = Path(audio_file).stem
        txt_file = os.path.join(output_dir, f"{audio_name}.txt")
        
        if os.path.exists(txt_file):
            print(f"Transcription completed: {txt_file}")
            return txt_file
        else:
            raise FileNotFoundError(f"Expected transcription file not found: {txt_file}")
             
    except subprocess.CalledProcessError as e:
        print(f"Error running Whisper: {e}")
        return None
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None

def check_gemini_access():
    """
    Check Google Gemini API access and configuration
    """
    try:
        print("🔍 Checking Google Gemini access...")
        
        # Check if API key is set
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ GEMINI_API_KEY not found in environment")
            print("💡 Get your free API key from: https://aistudio.google.com/app/apikey")
            print("💡 Then set it: export GEMINI_API_KEY='your_key_here'")
            return False
            
        print("✅ GEMINI_API_KEY found")
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Test connection with a simple request
        print("🔄 Testing API connection...")
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            "Hello", 
            generation_config=genai.types.GenerationConfig(max_output_tokens=10)
        )
        
        if response.text:
            print("✅ Google Gemini API is working correctly")
            print(f"🔍 Test response: {response.text[:50]}...")
            return True
        else:
            print("❌ Empty response from Gemini API")
            return False
            
    except Exception as e:
        print(f"❌ Error checking Gemini access: {e}")
        print("💡 Possible issues:")
        print("  - Invalid API key")
        print("  - Network connection problems")
        print("  - API quota/rate limits exceeded")
        print("  - API service temporarily unavailable")
        return False

def get_available_gemini_models():
    """
    Return available Google Gemini models with their configurations
    """
    return {
        "gemini-1.5-flash": {
            "max_tokens": 8192,
            "temperature": 0.7,
            "description": "Gemini 1.5 Flash - Modelo rápido y eficiente (recomendado)"
        },
        "gemini-1.5-pro": {
            "max_tokens": 8192,
            "temperature": 0.7,
            "description": "Gemini 1.5 Pro - Modelo avanzado con más contexto"
        },
        "gemini-pro": {
            "max_tokens": 4096,
            "temperature": 0.7,
            "description": "Gemini Pro - Modelo básico (puede no estar disponible)"
        },
        "gemini-2.0-flash": {
            "max_tokens": 8192,
            "temperature": 0.7,
            "description": "Gemini 2.0 Flash - Modelo más reciente (experimental)"
        }
    }

def generate_basic_summary(text):
    """
    Generate a basic summary when Gemini is not available
    This is a fallback method using simple text processing
    """
    lines = text.split('\n')
    sentences = []
    for line in lines:
        if line.strip():
            sentences.extend([s.strip() for s in line.split('.') if s.strip()])
    
    # Take first few sentences as a basic summary
    max_sentences = min(5, len(sentences))
    summary_sentences = sentences[:max_sentences]
    
    summary = {
        "resumen_ejecutivo": ". ".join(summary_sentences) + ".",
        "puntos_clave": [
            "Transcripción automática procesada",
            "Análisis básico sin IA externa",
            f"Texto de {len(text)} caracteres procesado"
        ],
        "conceptos_importantes": ["Audio transcrito", "Procesamiento local"],
        "preguntas_dudas": [],
        "tareas_acciones": ["Revisar transcripción completa", "Configurar acceso a Gemini para análisis avanzado"],
        "detalles_adicionales": [],
        "estructura_contenido": []
    }
    
    return summary

def generate_gemini_summary(text, model="gemini-1.5-flash"):
    """
    Generate summary using Google Gemini Pro
    
    Args:
        text (str): The transcribed text to analyze
        model (str): Gemini model to use for analysis
    """
    try:
        # Check if API key is configured
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ GEMINI_API_KEY not found")
            return None
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Verificar que el modelo esté disponible - usar modelo por defecto si no está disponible
        available_models = get_available_gemini_models()
        if model not in available_models:
            print(f"⚠️ Model '{model}' not in our list. Trying anyway...")
        
        # Truncate text if too long - más conservador para asegurar que funcione
        max_chars = 12000  # Más conservador para evitar límites
        if len(text) > max_chars:
            print(f"⚠️  Text too long ({len(text)} chars), truncating to {max_chars} chars")
            text = text[:max_chars] + "...\n[TEXTO TRUNCADO PARA ANÁLISIS]"
        
        print(f"🤖 Generating summary with Google Gemini ({model})...")
        
        # Create the optimized prompt for detailed academic summaries
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
        
        # Get model configuration
        model_config = available_models.get(model, available_models["gemini-1.5-flash"])
        generation_config = genai.types.GenerationConfig(
            max_output_tokens=model_config.get("max_tokens", 4096),
            temperature=model_config.get("temperature", 0.7),
        )
        
        # Create the model
        gemini_model = genai.GenerativeModel(model)
        
        # Add rate limiting to respect API limits (15 requests/minute for free tier)
        print("⏳ Respecting API rate limits...")
        time.sleep(2)  # Delay to avoid hitting rate limits
        
        # Generate the response
        response = gemini_model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        if not response.text:
            print("❌ Empty response from Gemini")
            return None
        
        print(f"✅ Gemini responded with {len(response.text)} characters")
        print(f"🔍 Debug: Raw response (first 200 chars): {response.text[:200]}...")
        
        # Parse JSON response
        try:
            clean_content = response.text.strip()
            
            # Remove markdown code blocks if present
            if clean_content.startswith('```json'):
                clean_content = clean_content[7:]
            elif clean_content.startswith('```'):
                clean_content = clean_content[3:]
            
            if clean_content.endswith('```'):
                clean_content = clean_content[:-3]
            
            clean_content = clean_content.strip()
            
            # Try to parse JSON
            summary_json = json.loads(clean_content)
            
            # Validate required keys
            required_keys = [
                "resumen_ejecutivo", "puntos_clave", "conceptos_importantes",
                "preguntas_dudas", "tareas_acciones", "detalles_adicionales", 
                "estructura_contenido"
            ]
            
            for key in required_keys:
                if key not in summary_json:
                    summary_json[key] = []
            
            print(f"✅ Google Gemini summary generated successfully with {model}")
            print(f"🔍 Debug: JSON keys found: {list(summary_json.keys())}")
            return summary_json
            
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parsing failed: {e}")
            print(f"🔍 Debug: Attempting to fix content...")
            print(f"🔍 Debug: Content preview: {clean_content[:300]}...")
            
            # Try to extract JSON from the response if it's mixed with other text
            import re
            json_match = re.search(r'\{.*\}', clean_content, re.DOTALL)
            if json_match:
                try:
                    json_str = json_match.group()
                    summary_json = json.loads(json_str)
                    print("✅ Successfully extracted JSON from mixed content")
                    return summary_json
                except:
                    pass
            
            # Return fallback structure with raw content processed
            return {
                "resumen_ejecutivo": response.text[:800] + "..." if len(response.text) > 800 else response.text,
                "puntos_clave": ["Contenido procesado por Gemini", "Revisar formato de respuesta"],
                "conceptos_importantes": ["Respuesta sin formato JSON válido"],
                "preguntas_dudas": [],
                "tareas_acciones": ["Revisar configuración de prompt"],
                "detalles_adicionales": ["Contenido generado pero formato incorrecto"],
                "estructura_contenido": ["Gemini respondió correctamente", "Formato de JSON necesita ajuste"]
            }
        
    except Exception as e:
        print(f"❌ Error calling Google Gemini: {e}")
        print(f"🔍 Debug: Exception type: {type(e).__name__}")
        return None

def create_obsidian_summary_only(gemini_summary, original_filename, output_path, gemini_model="gemini-1.5-flash"):
    """
    Create a summary-only markdown file for Obsidian (no transcription)
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M")
    
    # Get model description
    model_info = get_available_gemini_models().get(gemini_model, {})
    model_description = model_info.get('description', gemini_model)
    
    # Generate summary-only markdown content
    markdown_content = f"""# Resumen de Clase - {Path(original_filename).stem}

## Metadatos
- **Fecha:** {current_date}
- **Hora:** {current_time}
- **Archivo original:** {original_filename}
- **Procesado con:** Whisper (OpenAI) + Google Gemini
- **Modelo IA:** {gemini_model} ({model_description})
- **Tipo:** Resumen detallado (sin transcripción)

## Resumen Ejecutivo
{gemini_summary.get('resumen_ejecutivo', 'No disponible')}

"""
    
    # Add all Gemini-generated sections
    if gemini_summary.get('puntos_clave') and len(gemini_summary['puntos_clave']) > 0:
        markdown_content += "## Puntos Clave Principales\n"
        for i, punto in enumerate(gemini_summary['puntos_clave'], 1):
            markdown_content += f"{i}. {punto}\n"
        markdown_content += "\n"
    
    if gemini_summary.get('conceptos_importantes') and len(gemini_summary['conceptos_importantes']) > 0:
        markdown_content += "## Conceptos Importantes\n"
        for concepto in gemini_summary['conceptos_importantes']:
            if ':' in concepto:
                concepto_name, concepto_desc = concepto.split(':', 1)
                markdown_content += f"- **{concepto_name.strip()}:** {concepto_desc.strip()}\n"
            else:
                markdown_content += f"- **{concepto}**\n"
        markdown_content += "\n"
    
    if gemini_summary.get('preguntas_dudas') and len(gemini_summary['preguntas_dudas']) > 0:
        markdown_content += "## Preguntas y Dudas\n"
        for pregunta in gemini_summary['preguntas_dudas']:
            markdown_content += f"❓ {pregunta}\n"
        markdown_content += "\n"
    
    if gemini_summary.get('tareas_acciones') and len(gemini_summary['tareas_acciones']) > 0:
        markdown_content += "## Tareas y Acciones\n"
        for tarea in gemini_summary['tareas_acciones']:
            markdown_content += f"- [ ] {tarea}\n"
        markdown_content += "\n"
    
    if gemini_summary.get('detalles_adicionales') and len(gemini_summary['detalles_adicionales']) > 0:
        markdown_content += "## Detalles Adicionales\n"
        for detalle in gemini_summary['detalles_adicionales']:
            markdown_content += f"💡 {detalle}\n"
        markdown_content += "\n"
    
    if gemini_summary.get('estructura_contenido') and len(gemini_summary['estructura_contenido']) > 0:
        markdown_content += "## Estructura del Contenido\n"
        for i, tema in enumerate(gemini_summary['estructura_contenido'], 1):
            if ':' in tema:
                tema_name, tema_desc = tema.split(':', 1)
                markdown_content += f"{i}. **{tema_name.strip()}:** {tema_desc.strip()}\n"
            else:
                markdown_content += f"{i}. {tema}\n"
        markdown_content += "\n"
    
    # Add tags and metadata
    markdown_content += f"""---

## Tags
#resumen #clase #notas #audio #whisper #google-gemini #ai-summary #{gemini_model.replace('-', '')}

## Notas Adicionales
- [ ] Revisar y ampliar puntos clave
- [ ] Agregar enlaces a conceptos relacionados usando [[concepto]]
- [ ] Crear mapas conceptuales basados en la estructura
- [ ] Verificar tareas y fechas importantes
- [ ] Conectar con notas de clases anteriores
- [ ] Consultar transcripción completa si es necesario

## Referencias y Seguimiento
- [ ] Buscar material complementario sobre conceptos mencionados
- [ ] Preparar preguntas para próxima clase basadas en dudas identificadas
- [ ] Revisar bibliografía relacionada con los temas tratados
- [ ] Actualizar cronograma de estudios con las tareas identificadas

---
*Resumen generado automáticamente con Voice Note Processor + Google Gemini*
*Modelo usado: {gemini_model} ({model_description})*
*Procesado el {current_date} a las {current_time}*
"""
    
    # Write to file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"✅ Summary-only markdown created: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Error creating summary markdown file: {e}")
        return False

def create_obsidian_transcription_only(text_content, original_filename, output_path):
    """
    Create a transcription-only markdown file for Obsidian (no summary)
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M")
    
    # Split text into paragraphs
    paragraphs = [p.strip() for p in text_content.split('\n') if p.strip()]
    
    # Generate transcription-only markdown content
    markdown_content = f"""# Transcripción de Clase - {Path(original_filename).stem}

## Metadatos
- **Fecha:** {current_date}
- **Hora:** {current_time}
- **Archivo original:** {original_filename}
- **Procesado con:** Whisper (OpenAI)
- **Tipo:** Transcripción completa (sin resumen)
- **Longitud:** {len(text_content)} caracteres
- **Párrafos:** {len(paragraphs)} secciones

## Transcripción Completa

"""
    
    # Add transcription organized by sections
    for i, paragraph in enumerate(paragraphs, 1):
        if len(paragraph) > 30:  # Only include meaningful paragraphs
            markdown_content += f"### Sección {i}\n\n{paragraph}\n\n"
    
    # Add tags and metadata
    markdown_content += f"""---

## Tags
#transcripcion #clase #notas #audio #whisper #texto-completo

## Notas para Edición
- [ ] Revisar y corregir errores de transcripción
- [ ] Añadir puntuación donde sea necesario
- [ ] Identificar términos técnicos para crear enlaces [[concepto]]
- [ ] Marcar secciones importantes con **texto en negrita**
- [ ] Agregar > citas donde sea relevante
- [ ] Crear índice de temas si es necesario

## Sugerencias de Uso
- [ ] Usar esta transcripción junto con el resumen generado
- [ ] Buscar términos específicos con Cmd+F / Ctrl+F
- [ ] Extraer citas textuales importantes
- [ ] Identificar ejemplos específicos mencionados

---
*Transcripción generada automáticamente con Voice Note Processor*
*Procesado el {current_date} a las {current_time}*
"""
    
    # Write to file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"✅ Transcription-only markdown created: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Error creating transcription markdown file: {e}")
        return False

def process_voice_note_gemini(audio_file, whisper_model="medium", output_dir=".", gemini_model="gemini-1.5-flash"):
    """
    Complete workflow to process a voice note with Google Gemini summarization
    Generates 3 outputs: summary-only MD, transcription-only MD, and plain text
    """
    if not os.path.exists(audio_file):
        print(f"❌ Error: Audio file not found: {audio_file}")
        return False
    
    print("🎙️🤖 Voice Note Processor with Google Gemini")
    print("=" * 60)
    print(f"🎙️ Processing: {audio_file}")
    print(f"🎯 Whisper model: {whisper_model}")
    print(f"🤖 Gemini model: {gemini_model}")
    print(f"📁 Output directory: {output_dir}")
    print(f"📊 Generating 3 output files...")
    print("=" * 60)
    
    # Step 1: Transcribe audio
    txt_file = transcribe_audio(audio_file, whisper_model, output_dir)
    if not txt_file:
        return False
    
    # Step 2: Read transcription
    try:
        with open(txt_file, 'r', encoding='utf-8') as f:
            text_content = f.read()
        print(f"📝 Transcription loaded: {len(text_content)} characters")
    except Exception as e:
        print(f"❌ Error reading transcription file: {e}")
        return False
    
    # Step 3: Generate AI summary
    print(f"🎯 Using model: {gemini_model}")
    
    # Check Gemini access first
    if check_gemini_access():
        gemini_summary = generate_gemini_summary(text_content, gemini_model)
    else:
        print("⚠️ Gemini access check failed, using basic method")
        gemini_summary = None
    
    if not gemini_summary:
        print("⚠️ Gemini summary failed, using basic method")
        gemini_summary = generate_basic_summary(text_content)
    
    # Step 4: Generate output files
    audio_name = Path(audio_file).stem
    success_count = 0
    
    # 4.1: Create summary-only markdown
    summary_file = os.path.join(output_dir, f"{audio_name}_resumen.md")
    if create_obsidian_summary_only(gemini_summary, audio_file, summary_file, gemini_model):
        success_count += 1
    
    # 4.2: Create transcription-only markdown
    transcription_file = os.path.join(output_dir, f"{audio_name}_transcripcion.md")
    if create_obsidian_transcription_only(text_content, audio_file, transcription_file):
        success_count += 1
    
    # 4.3: Plain text transcription already exists from Step 1
    print(f"✅ Plain text transcription: {txt_file}")
    success_count += 1
    
    # Final results
    if success_count >= 2:  # At least 2 out of 3 files created successfully
        print("\n" + "=" * 60)
        print("🎉 ¡Procesamiento completado exitosamente!")
        print(f"📄 Transcripción (texto plano): {txt_file}")
        print(f"📝 Transcripción (Obsidian): {transcription_file}")
        print(f"🤖 Resumen detallado (Obsidian): {summary_file}")
        print(f"📊 {success_count}/3 archivos generados correctamente")
        print(f"🔥 Archivos listos para importar a Obsidian")
        print("=" * 60)
        return True
    else:
        print("\n❌ Error en el procesamiento - Archivos insuficientes generados")
        return False

def list_available_models():
    """
    Display available Gemini models
    """
    print("🤖 Modelos disponibles en Google Gemini:")
    print("=" * 50)
    models = get_available_gemini_models()
    for model_name, config in models.items():
        print(f"📋 {model_name}")
        print(f"   {config['description']}")
        print(f"   Max tokens: {config['max_tokens']}, Temperature: {config['temperature']}")
        print()
    
    print("💡 Modelos recomendados:")
    print("   • gemini-1.5-flash: Mejor opción general (recomendado)")
    print("   • gemini-1.5-pro: Para análisis más complejos")
    print("   • gemini-2.0-flash: Más reciente (experimental)")
    print()

def main():
    parser = argparse.ArgumentParser(description="Process voice notes for Obsidian with Google Gemini. Generates 3 outputs: detailed summary (MD), transcription (MD), and plain text.")
    parser.add_argument("audio_file", nargs='?', help="Path to the audio file")
    parser.add_argument("--model", default="medium", 
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper model to use (default: medium)")
    parser.add_argument("--output-dir", default=".", 
                       help="Output directory (default: current directory)")
    parser.add_argument("--gemini-api-key", help="Google Gemini API Key (or set GEMINI_API_KEY env var)")
    parser.add_argument("--gemini-model", default="gemini-1.5-flash",
                       help="Google Gemini model to use (default: gemini-1.5-flash)")
    parser.add_argument("--list-models", action="store_true",
                       help="List available Gemini models")
    parser.add_argument("--check-gemini", action="store_true",
                       help="Check Google Gemini access and configuration")
    parser.add_argument("--debug", action="store_true",
                       help="Enable debug output")
    
    args = parser.parse_args()
    
    if args.list_models:
        list_available_models()
        return
    
    if args.check_gemini:
        print("🔍 Checking Google Gemini configuration...")
        if check_gemini_access():
            print("✅ Google Gemini is properly configured!")
        else:
            print("❌ Google Gemini configuration issues detected")
            print("\n🛠️ Suggested fixes:")
            print("1. Get API key from: https://makersuite.google.com/app/apikey")
            print("2. Set environment variable: export GEMINI_API_KEY='your_api_key'")
            print("3. Or use --gemini-api-key argument")
        return
    
    if not args.audio_file:
        print("❌ Error: audio_file is required unless using --list-models or --check-gemini")
        parser.print_help()
        sys.exit(1)
    
    # Set API key if provided
    if args.gemini_api_key:
        import os
        os.environ['GEMINI_API_KEY'] = args.gemini_api_key
    
    success = process_voice_note_gemini(
        args.audio_file, 
        args.model, 
        args.output_dir, 
        args.gemini_model
    )
    
    if success:
        print("\n🚀 ¡Tus 3 archivos están listos para Obsidian!")
        print("   📄 Archivo de texto plano para búsquedas")
        print("   📝 Transcripción en markdown para edición")
        print("   🤖 Resumen detallado con análisis de IA")
    else:
        print("\n💥 Error en el procesamiento")
        sys.exit(1)

if __name__ == "__main__":
    main()
