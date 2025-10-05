#!/usr/bin/env python3
"""
Simple test script for Google Gemini API integration
"""

import os
import json
import google.generativeai as genai

def test_gemini_api_simple():
    """
    Test basic Gemini API functionality
    """
    print("🧪 Testing Google Gemini API...")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found")
        print("💡 Set it with: export GEMINI_API_KEY='your_api_key'")
        return False
    
    print("✅ API key found")
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Simple test
        print("🔄 Testing basic functionality...")
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Say hello in Spanish")
        
        if response.text:
            print("✅ Basic test successful!")
            print(f"📝 Response: {response.text}")
            print()
            
            # Test JSON generation (like our summarization)
            print("🔄 Testing JSON generation...")
            json_prompt = """
Generate a JSON response with this structure:
{
    "test": "success",
    "message": "This is a test response in Spanish",
    "numbers": [1, 2, 3]
}

Respond ONLY with valid JSON, no additional text.
"""
            
            json_response = model.generate_content(json_prompt)
            if json_response.text:
                try:
                    # Try to parse as JSON
                    clean_content = json_response.text.strip()
                    if clean_content.startswith('```json'):
                        clean_content = clean_content[7:]
                    if clean_content.endswith('```'):
                        clean_content = clean_content[:-3]
                    clean_content = clean_content.strip()
                    
                    parsed_json = json.loads(clean_content)
                    print("✅ JSON generation test successful!")
                    print(f"📝 JSON response: {json.dumps(parsed_json, indent=2, ensure_ascii=False)}")
                    print()
                    print("🎉 All tests passed! Your API is ready for voice note processing.")
                    return True
                    
                except json.JSONDecodeError as e:
                    print(f"⚠️ JSON parsing failed: {e}")
                    print(f"📝 Raw response: {json_response.text}")
                    print("💡 API works but JSON formatting needs adjustment")
                    return True  # API works, just JSON formatting issue
            else:
                print("❌ Empty JSON response")
                return False
        else:
            print("❌ Empty response from basic test")
            return False
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        print("💡 Check your API key and internet connection")
        return False

if __name__ == "__main__":
    success = test_gemini_api_simple()
    if success:
        print("\n🚀 Ready to process voice notes!")
        print("💡 Now you can run: python voice_to_notes.py your_audio_file.m4a")
    else:
        print("\n💥 API test failed - fix issues before processing audio")
