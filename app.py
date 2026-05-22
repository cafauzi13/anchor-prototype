import os
import streamlit as st
import importlib

# ==========================================
# 1. KONFIGURASI HALAMAN UTAMA
# ==========================================
st.set_page_config(
    page_title="Anchor — Day Closing Signal System",
    page_icon="⚓",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ==========================================
# 2. LOAD GLOBAL CSS (Menggunakan os.path aman)
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_global_css(file_name):
    css_path = os.path.join(BASE_DIR, file_name)
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Berkas {file_name} tidak ditemukan di {css_path}. Menggunakan tema default.")

load_global_css("style.css")

# ==========================================
# 3. INITIALIZATION SESSION STATE
# ==========================================
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

# ==========================================
# 4. HELPER: DYNAMIC ROUTER (Biar Fleksibel)
# ==========================================
def render_step_dynamically(module_name, function_name, fallback_callback):
    """
    Mencoba memuat modul dari folder 'core' secara dinamis.
    Jika file .py belum ada/belum fiks, otomatis pakai fungsi fallback bawaan.
    """
    try:
        # Coba import module secara dynamic, misal: core.landing atau core.vault
        mod = importlib.import_module(f"core.{module_name}")
        func = getattr(mod, function_name)
        func() # Jalankan fungsinya
    except (ModuleNotFoundError, AttributeError):
        # Kalau file/fungsi di folder core blm ada, jalankan codingan sementara di bawah
        fallback_callback()

# ==========================================
# 5. FALLBACK FUNCTIONS (UI Sementara bawaan Streamlit)
# ==========================================
def fallback_vault():
    st.subheader("Step 1: The Mental Vault 🔒")
    st.info("💡 Tip: File 'core/vault.py' belum fix/ditemukan. Menggunakan UI fallback fungsional.")
    thought = st.text_area("Apa yang paling mengganggumu malam ini?", placeholder="Tulis di sini...")
    if st.button("🔒 Titipkan ke Vault"):
        if thought.strip():
            st.session_state.vault_thought = thought
            st.session_state.step = 2
            st.rerun()

def fallback_senses():
    st.subheader("Step 2: Sensory Signals 🌙")
    st.info("💡 Tip: File 'core/senses.py' belum fix/ditemukan. Menggunakan UI fallback fungsional.")
    st.write("Redupkan lampu kamarmu dan dengarkan sinyal audio di bawah ini:")
    st.audio("https://upload.wikimedia.org/wikipedia/commons/transcoded/3/36/Thunderstorm_in_the_night.ogg/Thunderstorm_in_the_night.ogg.mp3", format="audio/mp3")
    if st.button("Saya Siap — Mulai Ritual Fisik →"):
        st.session_state.step = 3
        st.rerun()

def fallback_ritual():
    st.subheader("Step 3: The Anchor Ritual 🌿")
    st.info("💡 Tip: File 'core/ritual.py' belum fix/ditemukan. Menggunakan UI fallback fungsional.")
    if not st.session_state.timer_done:
        st.write("Lakukan pernapasan kotak sejenak...")
        if st.button("Selesaikan Ritual"):
            st.session_state.timer_done = True
            st.rerun()
    else:
        st.success("Ritual Selesai. Silakan letakkan perangkat ini.")
        if st.button("↩ Mulai Dari Awal"):
            for key in ['step', 'vault_submitted', 'vault_thought', 'timer_done', 'ritual_started']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

# ==========================================
# 6. EXECUTIVE ROUTER
# ==========================================
current_step = st.session_state.step

if current_step == 0:
    # Memanggil core/landing.py -> fungsi render_step_0()
    # Kalau crash/gaada, lsg stop kasih pesan error
    try:
        mod = importlib.import_module("core.landing")
        mod.render_step_0()
    except ModuleNotFoundError:
        st.error("Kritis: File 'core/landing.py' tidak ditemukan. Pastikan folder 'core' sudah benar.")

elif current_step == 1:
    # Mancing core/vault.py -> render_step_1(). Gaada? Pake fallback_vault
    render_step_dynamically("vault", "render_step_1", fallback_vault)

elif current_step == 2:
    # Mancing core/senses.py -> render_step_2(). Gaada? Pake fallback_senses
    render_step_dynamically("senses", "render_step_2", fallback_senses)

elif current_step == 3:
    # Mancing core/ritual.py -> render_step_3(). Gaada? Pake fallback_ritual
    render_step_dynamically("ritual", "render_step_3", fallback_ritual)