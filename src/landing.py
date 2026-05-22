import os
import streamlit as st
import streamlit.components.v1 as components

def render_step_0():
    # 1. RESOLUSI PATH DINAMIS
    # Mencari tahu direktori saat ini (src/) dan naik satu tingkat ke direktori utama (root)
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) 
    BASE_DIR = os.path.dirname(CURRENT_DIR) 

    # Asumsi code.html ada di dalam sub-folder anchor_landing di root directory
    # Ubah "anchor_landing" jika nama foldernya berbeda di struktur Anda
    html_path = os.path.join(BASE_DIR, "anchor_landing", "code.html") 

    # Fallback jika code.html ada di root directory utama
    fallback_path = os.path.join(BASE_DIR, "code.html")

    # 2. BACA FILE HTML
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        try:
            with open(fallback_path, "r", encoding="utf-8") as f:
                html_content = f.read()
        except FileNotFoundError:
            st.error(f"Gagal memuat UI. File HTML tidak ditemukan di {html_path} ataupun {fallback_path}")
            return

    # 3. RENDER BACKGROUND & HERO VISUAL
    # Dipotong tinggi renderingnya agar tombol CTA bisa dihandle native oleh Streamlit
    components.html(html_content, height=720, scrolling=True)

    # 4. INTERAKSI TOMBOL (CTA BUTTON NATIVE STREAMLIT)
    st.markdown('<div style="margin-top: -80px; position: relative; z-index: 999;">', unsafe_allow_html=True)
    if st.button("Enter Anchor Mode →", key="start_anchor_btn"):
        st.session_state.step = 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # 5. SUBTEXT HINT
    st.markdown("""
        <p style="text-align: center; margin-top: 2rem; font-family: 'DM Sans', sans-serif; 
                   font-size: 12px; color: rgba(226, 226, 239, 0.4); tracking-spacing: 0.2em; text-transform: uppercase;">
            Tap to silence the day — Est. ~3 mins
        </p>
    """, unsafe_allow_html=True)