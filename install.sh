#!/bin/bash

# Voice Notes Processor - Google Gemini Setup Script
# Created for macOS

echo "🎙️🤖 Voice Notes Processor - Google Gemini Setup"
echo "================================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found."
    echo "Please install Python 3 from https://www.python.org/"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv voice_notes_env

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source voice_notes_env/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip

# Check if requirements.txt exists, otherwise install manually
if [ -f "requirements.txt" ]; then
    echo "📋 Installing from requirements.txt..."
    pip install -r requirements.txt
else
    echo "📦 Installing core packages manually..."
    pip install google-generativeai openai-whisper
fi

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "🔐 Next steps:"
echo "1. Get your free Google Gemini API key:"
echo "   👉 https://makersuite.google.com/app/apikey"
echo ""
echo "2. Set up your API key (choose one option):"
echo "   Option A - Environment variable (recommended):"
echo "   export GEMINI_API_KEY='your_api_key_here'"
echo ""
echo "   Option B - Command line argument:"
echo "   python voice_to_notes.py audio.m4a --gemini-api-key 'your_api_key_here'"
echo ""
echo "3. Test the configuration:"
echo "   source voice_notes_env/bin/activate"
echo "   python voice_to_notes.py --check-gemini"
echo ""
echo "4. Process your first voice note:"
echo "   python voice_to_notes.py your_audio_file.m4a"
echo ""
echo "📚 For more help:"
echo "   python voice_to_notes.py --help"
echo "   python voice_to_notes.py --list-models"
echo ""
echo "✨ Ready to transform your voice notes into structured summaries!"
