import streamlit as st
import streamlit.components.v1 as components

def render_step_0():
    # 1. BACA FILE HTML asli dari Stitch
    try:
        with open("stitch_anchor_sleep_transition_system/anchor_landing/code.html", "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        # Fallback jika struktur foldermu ditaruh di root utama langsung
        with open("anchor_landing/code.html", "r", encoding="utf-8") as f:
            html_content = f.read()

    # 2. RENDER BACKGROUND & HERO VISUAL (Mencakup ornamen kosmik, bento card, dan nav bar bawah)
    # Kita potong tinggi renderingnya agar tombol CTA di bawah bisa dihandle native oleh Streamlit
    components.html(html_content, height=720, scrolling=True)

    # 3. INTERAKSI TOMBOL (CTA BUTTON NATIVE STREAMLIT)
    # Tombol ini otomatis memakai desain pil gradasi karena sudah di-override oleh style.css
    st.markdown('<div style="margin-top: -80px; position: relative; z-index: 999;">', unsafe_allow_html=True)
    if st.button("Enter Anchor Mode →", key="start_anchor_btn"):
        st.session_state.step = 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. SUBTEXT HINT
    st.markdown("""
        <p style="text-align: center; margin-top: 2rem; font-family: 'DM Sans', sans-serif; 
                  font-size: 12px; color: rgba(226, 226, 239, 0.4); tracking-spacing: 0.2em; text-transform: uppercase;">
            Tap to silence the day — Est. ~3 mins
        </p>
    """, unsafe_allow_html=True)

    