# ==========================================================================
# app.py - Main Router & State Management 
# ==========================================================================
import os
import sys
import streamlit as st  # <-- WAJIB: Kamu lupa mengimpor streamlit!

# Menambahkan root project dan sub-folder src ke sys.path agar Streamlit Cloud tidak bingung
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)
    sys.path.append(os.path.join(current_dir, "src"))

# Impor halaman/modul dari sub-folder src
try:
    from src.landing import render_step_0
except ModuleNotFoundError:
    # Fallback jika Streamlit Cloud menganggap root-nya adalah folder 'src' itu sendiri
    from landing import render_step_0

# 1. KONFIGURASI HALAMAN UTAMA
st.set_page_config(
    page_title="Anchor — Day Closing Signal System",
    page_icon="⚓",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 2. LOAD GLOBAL CSS (Membaca file style.css)
def load_global_css(file_name):
    try:
        with open(file_name, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Berkas style.css belum ditemukan di root folder. Menggunakan tema default.")

load_global_css("style.css")

# 3. INITIALIZATION SESSION STATE
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'vault_submitted' not in st.session_state:
    st.session_state.vault_submitted = False
if 'vault_thought' not in st.session_state:
    st.session_state.vault_thought = ''
if 'timer_done' not in st.session_state:
    st.session_state.timer_done = False
if 'ritual_started' not in st.session_state:
    st.session_state.ritual_started = False

# 4. ROUTER UTAMA
if st.session_state.step == 0:
    render_step_0()

elif st.session_state.step == 1:
    st.subheader("Step 1: The Mental Vault 🔒")
    st.write("UI sedang dalam pematangan oleh tim desainer. Fitur fungsional tetap aktif.")
    
    thought = st.text_area("Apa yang paling mengganggumu malam ini?", placeholder="Tulis di sini...")
    if st.button("🔒 Titipkan ke Vault"):
        if thought.strip():
            st.session_state.vault_thought = thought
            st.session_state.step = 2
            st.rerun()

elif st.session_state.step == 2:
    st.subheader("Step 2: Sensory Signals 🌙")
    st.write("Redupkan lampu kamarmu dan dengarkan sinyal audio di bawah ini:")
    st.audio("https://upload.wikimedia.org/wikipedia/commons/transcoded/3/36/Thunderstorm_in_the_night.ogg/Thunderstorm_in_the_night.ogg.mp3", format="audio/mp3")
    
    if st.button("Saya Siap — Mulai Ritual Fisik →"):
        st.session_state.step = 3
        st.rerun()

elif st.session_state.step == 3:
    st.subheader("Step 3: The Anchor Ritual 🌿")
    if not st.session_state.timer_done:
        st.write("Lakukan pernapasan kotak sejenak...")
        if st.button("Selesaikan Ritual"):
            st.session_state.timer_done = True
            st.rerun()
    else:
        st.success("Ritual Selesai. Silakan letakkan perangkat ini.")
        if st.button("↩ Mulai Dari Awal"):
            for key in ['step', 'vault_submitted', 'vault_thought', 'timer_done', 'ritual_started']:
                del st.session_state[key]
            st.rerun()