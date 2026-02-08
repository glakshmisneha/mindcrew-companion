import streamlit as st
import google.generativeai as genai
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="MindCrew Companion", layout="wide", page_icon="🧠")

# --- GLASSMORPHISM CSS ---
st.markdown('''
<style>
    .stApp {
        background: linear-gradient(-45deg, #050505, #1a1a2e, #16213e, #0f3460);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: white;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .main-title {
        text-align: center; font-size: 3.5rem; font-weight: 900;
        background: -webkit-linear-gradient(#00d2ff, #92fe9d);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        padding: 30px; border-radius: 25px; text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    .card:hover { transform: translateY(-5px); background: rgba(255, 255, 255, 0.08); }
    .advice-box {
        background: rgba(99, 102, 241, 0.15);
        padding: 20px; border-radius: 15px; border-left: 5px solid #6366f1;
        margin-top: 20px; line-height: 1.6;
    }
</style>
''', unsafe_allow_html=True)

# --- AI CONFIG ---
# This looks for the key in Streamlit Secrets or Environment Variables
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
else:
    st.error("Missing API Key! Please set GEMINI_API_KEY in your Secrets.")
    st.stop()

def get_ai_response(prompt):
    try:
        # Auto-detect the best available flash model
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target = next((m for m in models if "flash" in m.lower()), models[0])
        model = genai.GenerativeModel(target)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Connection Error: {str(e)}"

# --- ROUTING ---
if 'page' not in st.session_state: 
    st.session_state.page = 'dashboard'

# --- DASHBOARD ---
if st.session_state.page == 'dashboard':
    st.markdown('<p class="main-title">MindCrew Companion</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; opacity:0.8;">Your AI Wellness Space</p>', unsafe_allow_html=True)
    
    st.write("##")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card"><h1>🧠</h1><h3>Mood Advisor</h3><p>Insightful wellness tips.</p></div>', unsafe_allow_html=True)
        if st.button("Open Advisor", use_container_width=True): 
            st.session_state.page = 'mood'
            st.rerun()

    with col2:
        st.markdown('<div class="card"><h1>💬</h1><h3>Chat Support</h3><p>Empathetic AI talk.</p></div>', unsafe_allow_html=True)
        if st.button("Start Chatting", use_container_width=True): 
            st.session_state.page = 'chat'
            st.rerun()

# --- MOOD ADVISOR ---
elif st.session_state.page == 'mood':
    st.button("⬅ Back", on_click=lambda: st.session_state.update({"page": "dashboard"}))
    st.title("🧠 Mood Advisor")
    user_input = st.text_area("How are you feeling today?", placeholder="e.g., I'm feeling a bit overwhelmed with work...")
    
    if st.button("Get Support"):
        if user_input:
            with st.spinner("Thinking..."):
                res = get_ai_response(f"Give a short, supportive response and one wellness tip for: {user_input}")
                st.markdown(f'<div class="advice-box">{res}</div>', unsafe_allow_html=True)

# --- CHAT SUPPORT ---
elif st.session_state.page == 'chat':
    st.button("⬅ Back", on_click=lambda: st.session_state.update({"page": "dashboard"}))
    st.title("💬 Chat Support")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Message MindCrew..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        with st.chat_message("assistant"):
            response = get_ai_response(f"Act as a kind mental health AI. User says: {prompt}")
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
