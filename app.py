# ==========================================================================
# app.py - Main Router & State Management (Anchor Cosmic Deep Space)
# ==========================================================================
import streamlit as st

# 1. KONFIGURASI HALAMAN UTAMA
st.set_page_config(
    page_title="Anchor — Day Closing Signal System",
    page_icon="⚓",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 2. LOAD GLOBAL CSS (Membaca file style.css yang sudah kita buat dari DESIGN.md)
def load_global_css(file_name):
    try:
        with open(file_name, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Berkas style.css belum ditemukan di root folder. Menggunakan tema default.")

load_global_css("style.css")

# 3. INITIALIZATION SESSION STATE (Otak Logika Aliran Linier)
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

# 4. ROUTER UTAMA (Memanggil modul halaman secara dinamis)
if st.session_state.step == 0:
    # Memanggil file landing.py yang sudah membaca code.html Stitch
    from src.landing import render_step_0
    render_step_0()

elif st.session_state.step == 1:
    # Sementara pakai logika fungsional dasar kita kemarin sambil nunggu HTML Vault selesai
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
    # Logika timer sederhana untuk pengujian state
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