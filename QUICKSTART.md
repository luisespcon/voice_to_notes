# 🚀 Guía de Inicio Rápido

**¡Procesa tu primer archivo de audio en 5 minutos!**

---

## ⚡ Pasos Básicos

### **1️⃣ Instalación Automática**
```bash
# Ejecutar el instalador
./install.sh
```

### **2️⃣ Activar Entorno Virtual**
```bash
# ⚠️ IMPORTANTE: Siempre activar antes de usar
source voice_notes_env/bin/activate

# Verificar que está activo (debe aparecer el nombre entre paréntesis)
# (voice_notes_env) usuario@mac:~/Desktop$
```

### **3️⃣ Configurar API Key**
```bash
# Obtener gratis en: https://aistudio.google.com/app/apikey
export GEMINI_API_KEY='tu_api_key_aqui'
```

### **4️⃣ Probar el Sistema**
```bash
# Verificar que todo funciona
python voice_to_notes.py --check-gemini
```

### **5️⃣ Procesar Audio**
```bash
# ¡Listo! Procesa tu archivo
python voice_to_notes.py mi_audio.m4a
```

---

## 📁 Estructura de Archivos Generados

Después de procesar `mi_clase.m4a`, obtienes:

```
📄 mi_clase.txt               # Transcripción texto plano
📝 mi_clase_transcripcion.md  # Transcripción para Obsidian  
🤖 mi_clase_resumen.md        # Resumen inteligente con IA
```

---

## 🎯 Comandos Más Usados

```bash
# ⚠️ SIEMPRE activar entorno virtual primero
source voice_notes_env/bin/activate

# Uso básico
python voice_to_notes.py audio.m4a

# Con modelo específico (más preciso)
python voice_to_notes.py audio.m4a --model large

# Con Gemini avanzado
python voice_to_notes.py audio.m4a --gemini-model gemini-1.5-pro

# Directorio específico
python voice_to_notes.py audio.m4a --output-dir ./mis_notas/

# Ver modelos disponibles
python voice_to_notes.py --list-models
```

---

## 🧪 Archivo de Prueba

Usa el archivo `prueba.m4a` incluido para probar:

```bash
# Activar entorno virtual
source voice_notes_env/bin/activate

# Procesar archivo de ejemplo
python voice_to_notes.py prueba.m4a

# Cerrar entorno virtual cuando termines
deactivate
```

---

## 🔄 Comandos del Entorno Virtual

```bash
# Activar (necesario siempre antes de usar)
source voice_notes_env/bin/activate

# Verificar que está activo
# Debe aparecer: (voice_notes_env) en el prompt

# Desactivar (cuando termines de trabajar)
deactivate
```

---

## ❓ Problemas Comunes

### **❌ "Command not found" o "No module named 'whisper'"**
```bash
# Solución: Activar entorno virtual primero
source voice_notes_env/bin/activate

# Verificar que está activo
# (voice_notes_env) usuario@mac:~/Desktop$
```

### **❌ "API Key not found"**
```bash
# Configurar la API key
export GEMINI_API_KEY='AIzaSyA...'
```

### **❌ "Audio file not found"**
```bash
# Verificar que el archivo existe
ls -la mi_archivo.m4a
```

---

## 🔗 Enlaces Rápidos

- 🔑 [Obtener API Key](https://aistudio.google.com/app/apikey)
- 📖 [Documentación Completa](README.md)
- 🛠️ [Requisitos Técnicos](REQUIREMENTS.md)

---

**¡Ya estás listo para procesar audio con IA! 🎉**
