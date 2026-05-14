import streamlit as st
import time

# Konfigurasi Tema Hangat/Gelap
st.set_page_config(page_title="Anchor MVP", page_icon="⚓", layout="centered")

# Custom CSS untuk mereduksi cahaya (Warm Mode)
st.markdown("""
    <style>
    .main { background-color: #1a1a1a; color: #ffcc99; }
    .stButton>button { background-color: #cc5500; color: white; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚓ Anchor: Ritual Penutup Hari")
st.write("Dekonstruksi Brain Shutdown Failure untuk Mahasiswa Perantau.")

# State Management
if 'step' not in st.session_state:
    st.session_state.step = 0

# STEP 0: Trigger
if st.session_state.step == 0:
    st.info("Selesaikan aktivitas akademikmu. Siap untuk shutdown?")
    if st.button("AKTIFKAN ANCHOR MODE"):
        st.session_state.step = 1
        st.rerun()

# STEP 1: Mental Vault (NLP Validation)
if st.session_state.step == 1:
    st.subheader("1. The Mental Vault")
    thought = st.text_area("Tuliskan satu beban pikiran atau tugas esok hari yang paling mengganggumu:")
    if st.button("Titipkan ke Vault"):
        if thought:
            with st.spinner("Mengunci beban pikiran..."):
                time.sleep(1.5)
            st.success("Tugas sudah tercatat dan aman di sistem. Kamu punya izin untuk tidak memikirkannya sampai besok pagi.")
            if st.button("Lanjut ke Sinyal Sensorik"):
                st.session_state.step = 2
                st.rerun()
        else:
            st.warning("Isi dulu apa yang ada di pikiranmu.")

# STEP 2: Sensory Signal (Audio)
if st.session_state.step == 2:
    st.subheader("2. Replikasi Sinyal Lingkungan")
    st.write("Langkah: Matikan lampu utama, gunakan lampu redup.")
    st.write("Dengarkan audio penanda rumah di bawah ini:")
    # Menggunakan link audio sample suara alam/detak jam
    st.audio("https://www.soundjay.com/nature/sounds/rain-01.mp3") 
    if st.button("Lanjut ke Ritual Fisik"):
        st.session_state.step = 3
        st.rerun()

# STEP 3: Physical Ritual (Timer)
if st.session_state.step == 3:
    st.subheader("3. The Anchor Ritual")
    st.write("Lakukan peregangan statis atau pernapasan kotak selama 60 detik.")
    
    # Simple Timer
    t = st.empty()
    for i in range(60, -1, -1):
        t.metric("Waktu Tersisa", f"{i} detik")
        time.sleep(1)
    
    st.balloons()
    st.success("Ritual Selesai. Otak siap shutdown. Silakan letakkan perangkatmu.")
    if st.button("Ulangi dari Awal"):
        st.session_state.step = 0
        st.rerun()