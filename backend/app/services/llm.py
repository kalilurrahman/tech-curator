import os
import google.generativeai as genai

API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

def summarize_text(text: str, source: str) -> str:
    if not API_KEY: return "Summary unavailable (No API Key)."
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        prompt = f"Summarize this tech news in under 50 words. Be direct. Text: {text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except:
        return text[:100] + "..."

def generate_topic_label(title: str) -> str:
    if not API_KEY: return "TECH"
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        prompt = f"Give me a 2-word category label for this headline: '{title}'. UPPERCASE only."
        response = model.generate_content(prompt)
        return response.text.strip().replace("\n", "")
    except:
        return "NEWS"
