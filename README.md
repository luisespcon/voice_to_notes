# Voice Note Processor 🎙️🤖

**Transforma archivos de audio en notas académicas estructuradas usando IA**

Automatiza completamente el proceso de convertir grabaciones de clases, conferencias, reuniones o cualquier audio en documentos Markdown optimizados para Obsidian, con transcripción por Whisper y análisis inteligente por Google Gemini.

---

## 🚀 Características

### ✨ **Procesamiento Completo**
- 🎙️ **Transcripción precisa** con OpenAI Whisper (5 modelos disponibles)
- 🤖 **Análisis inteligente** con Google Gemini (4 modelos, gratis hasta 15 req/min)
- 📝 **3 archivos de salida** por cada audio procesado

### 📄 **Formatos de Salida**
1. **`archivo_resumen.md`** - Resumen académico estructurado con IA
2. **`archivo_transcripcion.md`** - Transcripción completa organizada por secciones  
3. **`archivo.txt`** - Transcripción en texto plano para búsquedas

### 🎯 **Optimizado para Obsidian**
- ✅ Tags automáticos (`#resumen`, `#transcripcion`, `#audio`, etc.)
- ✅ Metadatos estructurados (fecha, hora, modelo usado)
- ✅ Enlaces internos preparados (`[[concepto]]`)
- ✅ Checkboxes para seguimiento de tareas
- ✅ Formato académico profesional

### 🌐 **Soporte Amplio**
- **Formatos de audio:** M4A, MP3, WAV, FLAC, AAC, OGG
- **Idiomas:** Español, Inglés, y 90+ idiomas más
- **Sistemas:** macOS, Linux, Windows

---

## 📋 Requisitos del Sistema

### **Software Requerido**
- **Python 3.7+** (recomendado 3.9+)
- **FFmpeg** (para procesamiento de audio)
- **Conexión a Internet** (para APIs de Whisper y Gemini)

### **APIs Necesarias**
- **Google Gemini API Key** (gratuita) - [Obtener aquí](https://aistudio.google.com/app/apikey)

### **Espacio en Disco**
- **Mínimo:** 2GB para dependencias
- **Recomendado:** 5GB (incluye modelos de Whisper grandes)

---

## ⚡ Instalación Rápida

### **Opción 1: Instalación Automática (Recomendada)**
```bash
# Clonar/descargar el proyecto y ejecutar:
./install.sh
```

### **Opción 2: Instalación Manual**
```bash
# 1. Crear entorno virtual
python3 -m venv voice_notes_env

# 2. Activar entorno virtual
source voice_notes_env/bin/activate  # macOS/Linux
# voice_notes_env\Scripts\activate  # Windows

# 3. Instalar dependencias
pip install --upgrade pip
pip install openai-whisper google-generativeai

# 4. Configurar API Key
export GEMINI_API_KEY='tu_api_key_aqui'
```

---

## 🔧 Configuración

### **1. Manejo del Entorno Virtual**

**⚠️ IMPORTANTE: Siempre activar el entorno virtual antes de usar el sistema**

#### **Activar entorno virtual:**
```bash
source voice_notes_env/bin/activate  # macOS/Linux
# voice_notes_env\Scripts\activate  # Windows
```

#### **Desactivar entorno virtual:**
```bash
deactivate
```

#### **Verificar que está activo:**
- El prompt debe mostrar `(voice_notes_env)` al principio
- Ejemplo: `(voice_notes_env) usuario@mac:~/Desktop$`

#### **¿Por qué es necesario?**
- 📦 Aísla las dependencias del proyecto
- 🛡️ Evita conflictos con otros proyectos Python
- ✅ Garantiza que Whisper y Gemini funcionen correctamente
- 🔧 Permite usar versiones específicas de librerías

### **2. Obtener API Key de Google Gemini**
1. Visita [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Crea una nueva API Key (gratuita)
3. Configúrala en tu sistema:

```bash
# Temporal (solo para la sesión actual)
export GEMINI_API_KEY='AIzaSyA...'

# Permanente (agregar a ~/.zshrc o ~/.bashrc)
echo 'export GEMINI_API_KEY="AIzaSyA..."' >> ~/.zshrc
source ~/.zshrc
```

### **3. Verificar Instalación**
```bash
# ⚠️ IMPORTANTE: Activar entorno virtual primero
source voice_notes_env/bin/activate

# Probar conectividad con Gemini
python test_gemini_api.py

# Verificar configuración completa
python voice_to_notes.py --check-gemini

# Ver modelos disponibles
python voice_to_notes.py --list-models
```

---

## 🎯 Uso

### **Uso Básico**
```bash
# ⚠️ IMPORTANTE: Activar entorno virtual primero
source voice_notes_env/bin/activate

# Procesar archivo en el directorio actual
python voice_to_notes.py mi_clase.m4a

# Procesar archivo desde cualquier ubicación (ruta absoluta)
python voice_to_notes.py ~/Desktop/mi_clase.m4a
```

### **Uso Avanzado**
```bash
# ⚠️ RECUERDA: Activar entorno virtual
source voice_notes_env/bin/activate

# Especificar modelo de Whisper y Gemini
python voice_to_notes.py clase.mp3 --model large --gemini-model gemini-1.5-pro

# Especificar directorio de salida (relativa)
python voice_to_notes.py audio.wav --output-dir ./mis_notas/

# Especificar directorio de salida (ruta absoluta)
python voice_to_notes.py ~/Desktop/audio.wav --output-dir ~/Desktop/mis_notas/

# Usar API key específica
python voice_to_notes.py audio.m4a --gemini-api-key 'tu_key_aqui'
```

### **Opciones de Línea de Comandos**
```
python voice_to_notes.py [archivo_audio] [opciones]

Argumentos:
  archivo_audio              Ruta al archivo de audio a procesar

Opciones:
  --model {tiny,base,small,medium,large}
                            Modelo de Whisper (default: medium)
  --output-dir DIR          Directorio de salida (rutas relativas o absolutas)
                            Ejemplos: ./notas/, ~/Desktop/, /Users/tu_usuario/Documentos/
  --gemini-model MODEL      Modelo de Gemini (default: gemini-1.5-flash)
  --gemini-api-key KEY      API Key de Gemini (o usar GEMINI_API_KEY)
  --list-models             Listar modelos disponibles
  --check-gemini            Verificar configuración de Gemini
  --debug                   Mostrar información de depuración
```

---

## 📊 Modelos Disponibles

### **Modelos de Whisper (Transcripción)**
| Modelo | Tamaño | Velocidad | Precisión | Uso Recomendado |
|--------|--------|-----------|-----------|-----------------|
| `tiny` | ~39MB | Muy rápida | Básica | Pruebas rápidas |
| `base` | ~74MB | Rápida | Buena | Audio claro |
| `small` | ~244MB | Media | Muy buena | Uso general |
| `medium` | ~769MB | Lenta | Excelente | **Recomendado** |
| `large` | ~1550MB | Muy lenta | Máxima | Audio complejo |

### **Modelos de Gemini (Análisis)**
| Modelo | Contexto | Velocidad | Calidad | Límite Gratuito |
|--------|----------|-----------|---------|-----------------|
| `gemini-1.5-flash` | 8K tokens | Muy rápida | Excelente | **Recomendado** |
| `gemini-1.5-pro` | 8K tokens | Rápida | Máxima | Análisis complejos |
| `gemini-2.0-flash` | 8K tokens | Rápida | Experimental | Experimental |

---

## 📝 Estructura de Salida

### **Archivo de Resumen (`*_resumen.md`)**
```markdown
# Resumen de Clase - mi_audio

## Metadatos
- **Fecha:** 2025-08-05
- **Procesado con:** Whisper + Google Gemini
- **Modelo IA:** gemini-1.5-flash

## Resumen Ejecutivo
[Párrafo generado por IA con esencia de la sesión]

## Puntos Clave Principales
1. [Punto importante con explicación detallada]
2. [Otro punto clave identificado por IA]

## Conceptos Importantes
- **Concepto 1:** Definición y explicación
- **Concepto 2:** Términos técnicos explicados

## Preguntas y Dudas
❓ [Interrogantes identificadas en el audio]

## Tareas y Acciones
- [ ] [Tarea específica mencionada]
- [ ] [Fecha de entrega identificada]

## Tags
#resumen #clase #notas #audio #gemini
```

### **Archivo de Transcripción (`*_transcripcion.md`)**
```markdown
# Transcripción de Clase - mi_audio

## Metadatos
- **Procesado con:** Whisper (OpenAI)
- **Longitud:** X caracteres

## Transcripción Completa

### Sección 1
[Texto transcrito organizado por párrafos]

### Sección 2
[Continuación de la transcripción]

## Tags
#transcripcion #audio #whisper
```

---

## 🔧 Solución de Problemas

### **Problemas Comunes**

#### ❌ "GEMINI_API_KEY not found"
```bash
# Solución: Configurar la API key en el sistema
export GEMINI_API_KEY='tu_api_key_aqui'
```

#### ❌ "whisper: command not found" o "No module named 'whisper'"
```bash
# Solución: Activar el entorno virtual primero
source voice_notes_env/bin/activate
python voice_to_notes.py mi_archivo.m4a
```

#### ❌ "Audio file not found"
```bash
# Verificar que el archivo existe y tiene permisos de lectura
ls -la mi_archivo.m4a
```

#### ❌ "Empty response from Gemini"
```bash
# Verificar conectividad y límites de API
python test_gemini_api.py
```

### **Diagnóstico**
```bash
# ⚠️ Activar entorno virtual primero
source voice_notes_env/bin/activate

# Verificar todo el sistema
python voice_to_notes.py --check-gemini

# Probar solo la API
python test_gemini_api.py

# Modo debug para más información
python voice_to_notes.py archivo.m4a --debug
```

---

## 📈 Optimización y Tips

### **Mejores Prácticas**
- ✅ Usar audio de **buena calidad** (sin ruido de fondo)
- ✅ **Activar siempre** el entorno virtual antes de usar
- ✅ Para audio largo (+30min), usar modelo `large` de Whisper
- ✅ Procesar archivos por **lotes** para eficiencia
- ✅ Revisar y editar las transcripciones antes de archivar

### **Rendimiento**
- **Audio de 60min** ≈ 3-5 minutos de procesamiento (modelo medium)
- **Límite gratuito** de Gemini: 15 requests/minuto
- **Archivos grandes**: El script maneja automáticamente los límites

---

## 🤝 Casos de Uso

### **Estudiantes**
- 📚 Transcribir clases y generar resúmenes automáticos
- 📝 Crear notas estructuradas para Obsidian
- 🎯 Identificar conceptos clave y tareas

### **Profesionales**
- 💼 Procesar reuniones y generar actas automáticas
- 📊 Analizar conferencias y webinars
- 📋 Crear documentación a partir de grabaciones

### **Investigadores**
- 🔬 Transcribir entrevistas cualitativas
- 📖 Analizar contenido de seminarios
- 🎓 Procesar material educativo

---

## 📜 Licencia y Créditos

### **Herramientas Utilizadas**
- **OpenAI Whisper** - Transcripción de audio
- **Google Gemini** - Análisis y resumen con IA
- **Python 3** - Lenguaje de programación

### **Autor**
Desarrollado para optimizar el flujo de trabajo académico con herramientas de IA de última generación.

---

## 🔗 Enlaces Útiles

- [Google AI Studio (API Key)](https://aistudio.google.com/app/apikey)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Obsidian](https://obsidian.md/)
- [Documentación de Gemini](https://ai.google.dev/)

---

*Última actualización: Agosto 2025*
