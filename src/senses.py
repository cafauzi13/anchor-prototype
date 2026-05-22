# ==========================================================================
# src/senses.py - Step 2: Sensory Signals (Audio-Visual Signal)
# ==========================================================================
import streamlit as st
import streamlit.components.v1 as components

def render_step_2():
    # 1. Coba baca HTML murni dari Stitch jika desainer sudah mengekspornya
    try:
        with open("anchor_sensory_signals/code.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        components.html(html_content, height=360, scrolling=False)
    except FileNotFoundError:
        # Fallback UI otomatis dengan tema Cosmic Deep Space yang serasi
        st.markdown("""
        <div style="text-align:center; font-family:'Quicksand',sans-serif; margin-bottom:1.5rem;">
            <div style="font-size:0.75rem; color:#d2bcfa; letter-spacing:0.2em; text-transform:uppercase;">Step 2 of 3</div>
            <h2 style="font-size:1.8rem; font-weight:600; margin-top:0.5rem; color:#e2e2e9;">Signal Your Senses.</h2>
            <p style="font-size:0.9rem; color:#cbc4d0; max-width:450px; margin:0.5rem auto; line-height:1.6;">
                Ubah lingkungan fisikmu. Sinyal sensorik memberi tahu sistem saraf bahwa hari telah usai dengan jauh lebih kuat daripada sekadar tekad.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Kartu Instruksi Glassmorphism
        st.markdown("""
        <div class="glass-card" style="font-family:'DM Sans',sans-serif;">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:0.8rem;">
                <span style="color:#ffafd5; font-size:1.2rem;">💡</span>
                <strong style="color:#e2e2e9; font-weight:500;">1. Redupkan Lampu Utama</strong>
            </div>
            <p style="font-size:0.85rem; color:#cbc4d0; margin-left:28px; line-height:1.5;">
                Matikan lampu utama kamarmu. Gunakan lampu sekunder berwarna kuning atau redup untuk merangsang hormon melatonin alami.
            </p>
            <div style="height:1px; background:rgba(226,226,233,0.05); margin:1rem 0;"></div>
            <div style="display:flex; align-items:center; gap:12px;">
                <span style="color:#d2bcfa; font-size:1.2rem;">📱</span>
                <strong style="color:#e2e2e9; font-weight:500;">2. Balikkan Layar Ponsel</strong>
            </div>
            <p style="font-size:0.85rem; color:#cbc4d0; margin-left:28px; line-height:1.5;">
                Setelah menekan tombol putar musik di bawah, posisikan layar perangkat menghadap ke bawah kasur. Lindungi matamu dari cahaya.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # 2. Audio Player Component (Terintegrasi Aman di Luar Iframe)
    st.markdown("""
    <div style="padding: 0.5rem 0; font-family:'DM Sans',sans-serif;">
        <span style="font-size:0.8rem; color:#948e99; letter-spacing:0.05em; text-transform:uppercase;">
            🎵 Ambient Sound — Cosmic Drift / Hujan Kos
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Memutar audio latar belakang dari server publik domain yang andal
    st.audio(
        "https://upload.wikimedia.org/wikipedia/commons/transcoded/3/36/Thunderstorm_in_the_night.ogg/Thunderstorm_in_the_night.ogg.mp3",
        format="audio/mp3"
    )
    
    st.markdown("<br><br>", unsafe_allow_html=True)

    # 3. Tombol Navigasi Utama (Pill-shaped Bergradasi dari style.css)
    if st.button("Proceed to Ritual →", key="go_to_step3_btn"):
        st.session_state.step = 3
        st.rerun()