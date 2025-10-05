# Requisitos Técnicos - Voice Note Processor

## 🖥️ Requisitos del Sistema

### **Sistema Operativo**
- ✅ **macOS** 10.14+ (Mojave o superior)
- ✅ **Linux** (Ubuntu 18.04+, CentOS 7+, Debian 10+)
- ✅ **Windows** 10/11 (con WSL recomendado)

### **Python**
- **Versión mínima:** Python 3.7
- **Versión recomendada:** Python 3.9 o superior
- **Verificar versión:** `python3 --version`

### **Memoria RAM**
- **Mínimo:** 4GB RAM
- **Recomendado:** 8GB+ RAM (para modelos de Whisper grandes)

### **Espacio en Disco**
- **Instalación básica:** 2GB
- **Con modelo `large`:** 4GB
- **Recomendado:** 5GB libres

### **Conectividad**
- **Internet requerido** para:
  - Descargar modelos de Whisper (primera vez)
  - Acceder a Google Gemini API
  - Instalar dependencias de Python

---

## 📦 Dependencias de Python

### **Dependencias Principales**
```txt
openai-whisper>=20231117
google-generativeai>=0.3.0
```

### **Dependencias del Sistema (Automáticas)**
```txt
torch>=1.9.0
torchaudio>=0.9.0
numpy>=1.21.0
scipy>=1.7.0
transformers>=4.19.0
ffmpeg-python>=0.2.0
```

### **Dependencias de Desarrollo (Opcionales)**
```txt
pytest>=7.0.0
black>=22.0.0
flake8>=4.0.0
```

---

## 🛠️ Software Externo Requerido

### **FFmpeg** (Crítico)
FFmpeg es necesario para el procesamiento de audio por Whisper.

#### **macOS (con Homebrew)**
```bash
brew install ffmpeg
```

#### **Ubuntu/Debian**
```bash
sudo apt update
sudo apt install ffmpeg
```

#### **CentOS/RHEL**
```bash
sudo yum install epel-release
sudo yum install ffmpeg
```

#### **Windows**
1. Descargar desde [ffmpeg.org](https://ffmpeg.org/download.html)
2. Agregar al PATH del sistema
3. O usar chocolatey: `choco install ffmpeg`

#### **Verificar instalación**
```bash
ffmpeg -version
```

---

## 🔑 APIs y Servicios Externos

### **Google Gemini API**
- **Tipo:** Gratuita con límites
- **Límite gratuito:** 15 requests por minuto
- **Obtener:** [Google AI Studio](https://aistudio.google.com/app/apikey)
- **Configuración:** Variable de entorno `GEMINI_API_KEY`

### **Modelos de Whisper (OpenAI)**
- **Descarga:** Automática en primera ejecución
- **Ubicación:** `~/.cache/whisper/`
- **Tamaños:**
  - `tiny`: ~39MB
  - `base`: ~74MB  
  - `small`: ~244MB
  - `medium`: ~769MB
  - `large`: ~1550MB

---

## ⚙️ Configuración del Entorno

### **Variables de Entorno Requeridas**
```bash
# API Key de Google Gemini (OBLIGATORIA)
# Obtener gratis en: https://aistudio.google.com/app/apikey
export GEMINI_API_KEY="tu_api_key_aqui"
```

### **Variables de Entorno Opcionales**
```bash
# Directorio de cache de Whisper (opcional)
export WHISPER_CACHE_DIR="$HOME/.whisper_cache"

# Configuración de proxy (si es necesario)
export HTTP_PROXY="http://proxy.empresa.com:8080"
export HTTPS_PROXY="http://proxy.empresa.com:8080"
```

### **Configuración Permanente**
```bash
# Agregar a ~/.zshrc o ~/.bashrc
echo 'export GEMINI_API_KEY="tu_api_key_aqui"' >> ~/.zshrc
source ~/.zshrc
```

---

## 🧪 Pruebas de Compatibilidad

### **Verificar Python**
```bash
python3 --version
# Debe mostrar: Python 3.7+ 
```

### **Verificar pip**
```bash
pip3 --version
# Debe estar instalado y actualizado
```

### **Verificar FFmpeg**
```bash
ffmpeg -version
# Debe mostrar versión de FFmpeg
```

### **Verificar conexión a Internet**
```bash
curl -I https://api.google.com
# Debe responder con código 200
```

### **Prueba completa del sistema**
```bash
# Ejecutar después de la instalación
python voice_to_notes.py --check-gemini
```

---

## 🚨 Problemas Conocidos y Soluciones

### **macOS**
#### **Problema:** "xcrun: error: invalid active developer path"
```bash
# Solución: Instalar Command Line Tools
xcode-select --install
```

#### **Problema:** Certificados SSL
```bash
# Solución: Actualizar certificados
/Applications/Python\ 3.x/Install\ Certificates.command
```

### **Linux**
#### **Problema:** "No module named '_ssl'"
```bash
# Solución: Instalar dependencias SSL
sudo apt-get install libssl-dev libffi-dev
```

#### **Problema:** Permisos de escritura
```bash
# Solución: Usar entorno virtual (recomendado)
python3 -m venv voice_notes_env
source voice_notes_env/bin/activate
```

### **Windows**
#### **Problema:** "Windows cannot find python"
```bash
# Solución: Agregar Python al PATH o usar:
py -3 voice_to_notes.py
```

#### **Problema:** Encoding issues
```bash
# Solución: Configurar UTF-8
set PYTHONIOENCODING=utf-8
```

---

## 📊 Requisitos de Rendimiento

### **Tiempo de Procesamiento Estimado**
| Duración Audio | Modelo Whisper | Tiempo Aprox. | RAM Usada |
|----------------|----------------|---------------|-----------|
| 10 minutos | tiny | 30 segundos | 1GB |
| 10 minutos | medium | 2 minutos | 2GB |
| 10 minutos | large | 4 minutos | 4GB |
| 60 minutos | medium | 10 minutos | 2GB |
| 60 minutos | large | 20 minutos | 4GB |

### **Uso de Red**
- **Primera instalación:** ~2GB (descarga de modelos)
- **Uso normal:** ~10KB por minuto de audio (API calls)
- **Sin conexión:** Solo transcripción (sin resumen IA)

---

## 🔍 Verificación Post-Instalación

### **Lista de Verificación**
- [ ] Python 3.7+ instalado
- [ ] FFmpeg instalado y en PATH
- [ ] Entorno virtual creado y activado
- [ ] Dependencias de Python instaladas
- [ ] API Key de Gemini configurada
- [ ] Conectividad a Internet funcional
- [ ] Prueba básica exitosa

### **Comando de Verificación Completa**
```bash
#!/bin/bash
echo "🔍 Verificando requisitos del sistema..."

# Verificar Python
python3 --version || echo "❌ Python 3 no encontrado"

# Verificar FFmpeg
ffmpeg -version >/dev/null 2>&1 && echo "✅ FFmpeg OK" || echo "❌ FFmpeg no encontrado"

# Verificar API Key
[ -n "$GEMINI_API_KEY" ] && echo "✅ API Key configurada" || echo "❌ API Key no configurada"

# Verificar dependencias Python
python3 -c "import whisper, google.generativeai" 2>/dev/null && echo "✅ Dependencias OK" || echo "❌ Faltan dependencias"

echo "🚀 Ejecutar: python voice_to_notes.py --check-gemini"
```

---

## 📋 Troubleshooting Rápido

### **El script no ejecuta**
1. ✅ Verificar que el entorno virtual esté activado
2. ✅ Verificar permisos de ejecución: `chmod +x voice_to_notes.py`
3. ✅ Usar `python3` en lugar de `python`

### **Error de importación**
1. ✅ Reinstalar dependencias: `pip install -r requirements.txt`
2. ✅ Verificar versión de Python: `python3 --version`
3. ✅ Limpiar cache: `pip cache purge`

### **API no responde**
1. ✅ Verificar API Key: `echo $GEMINI_API_KEY`
2. ✅ Probar conectividad: `python test_gemini_api.py`
3. ✅ Verificar límites de uso en Google AI Studio

---

*Documento técnico actualizado - Agosto 2025*
