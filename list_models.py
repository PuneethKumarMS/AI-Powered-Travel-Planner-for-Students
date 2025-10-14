import google.generativeai as genai
import streamlit as st

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    print("Gemini API Key not found. Please set it in .streamlit/secrets.toml")
    exit()

for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)