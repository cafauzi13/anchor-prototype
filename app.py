"""
Anchor - The Day Closing Signal System
MVP untuk mengatasi Brain Shutdown Failure pada mahasiswa perantau ITS.

Arsitektur: Linear 4-Step Flow menggunakan st.session_state
Step 0: Landing & Trigger
Step 1: The Mental Vault
Step 2: Sensory Signals
Step 3: The Anchor Ritual (Timer)

FIX: Semua HTML menggunakan inline styles penuh — tidak bergantung pada CSS class
     eksternal karena Streamlit men-sanitasi nested HTML yang referensi class kustom.
"""

import streamlit as st
import time
import streamlit.components.v1 as components

# ─────────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Anchor — Ritual Penutup Hari",
    page_icon="⚓",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# GLOBAL CSS — Hanya untuk elemen Streamlit native
# Tidak ada class kustom yang dipakai di dalam st.markdown HTML
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg-deep:        #0f0d0b;
    --bg-card:        #1c1915;
    --bg-input:       #231f1a;
    --amber:          #e8923a;
    --amber-soft:     #c97d30;
    --amber-glow:     rgba(232, 146, 58, 0.12);
    --amber-border:   rgba(232, 146, 58, 0.25);
    --text-primary:   #f2e8d9;
    --text-muted:     #9e8e7a;
    --text-dim:       #5c5040;
    --success-bg:     rgba(94, 148, 94, 0.15);
    --success-border: rgba(94, 148, 94, 0.35);
    --success-text:   #a8d5a8;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg-deep) !important;
    color: var(--text-primary) !important;
}

.main .block-container {
    padding: 2rem 1.5rem 4rem !important;
    max-width: 600px !important;
    margin: 0 auto !important;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* Streamlit native: textarea */
div.stTextArea > label {
    font-size: 0.88rem !important;
    color: #9e8e7a !important;
    font-family: 'DM Sans', sans-serif !important;
}
div.stTextArea textarea {
    background-color: #231f1a !important;
    border: 1px solid rgba(232, 146, 58, 0.25) !important;
    border-radius: 10px !important;
    color: #f2e8d9 !important;
    font-family: 'Lora', serif !important;
    font-size: 0.95rem !important;
    line-height: 1.7 !important;
    caret-color: #e8923a !important;
}
div.stTextArea textarea:focus {
    border-color: #e8923a !important;
    box-shadow: 0 0 0 2px rgba(232, 146, 58, 0.12) !important;
}

/* Streamlit native: primary buttons */
div.stButton > button {
    background: linear-gradient(135deg, #e8923a, #c97d30) !important;
    color: #0f0d0b !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 1.5rem !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(232,146,58,0.25) !important;
}
div.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 28px rgba(232,146,58,0.4) !important;
}
div.stButton > button:active {
    transform: translateY(0) !important;
}

/* Streamlit native: secondary button (kolom terakhir) */
div[data-testid="column"]:last-child div.stButton > button {
    background: #1c1915 !important;
    color: #9e8e7a !important;
    border: 1px solid rgba(232, 146, 58, 0.25) !important;
    box-shadow: none !important;
}

/* Streamlit native: alert */
div[data-testid="stAlert"] {
    background: #1c1915 !important;
    border: 1px solid rgba(232, 146, 58, 0.25) !important;
    border-radius: 10px !important;
    color: #9e8e7a !important;
}

/* Audio */
audio {
    width: 100%;
    margin-top: 0.5rem;
    filter: sepia(0.5) hue-rotate(20deg);
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SESSION STATE INITIALIZATION
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        'step': 0,
        'vault_submitted': False,
        'vault_thought': '',
        'timer_started': False,
        'timer_done': False,
        'ritual_started': False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_state()


# ─────────────────────────────────────────────
# HELPER: Render Progress Bar (inline styles)
# ─────────────────────────────────────────────
def render_progress(current_step: int):
    bars = ""
    for i in range(1, 4):
        if i <= current_step:
            bars += (
                '<div style="flex:1; height:3px; border-radius:99px; '
                'background:#e8923a; box-shadow:0 0 8px #e8923a; '
                'transition:background 0.5s ease;"></div>'
            )
        else:
            bars += (
                '<div style="flex:1; height:3px; border-radius:99px; '
                'background:#5c5040; transition:background 0.5s ease;"></div>'
            )
            
    components.html(f"""
    <style>body {{ margin: 0; padding: 0; }}</style>
    <div style="display:flex; gap:8px; margin-bottom:1rem; padding:0 4px;">
        {bars}
    </div>
    """, height=30)


# ─────────────────────────────────────────────
# HELPER: Render Logo (inline styles)
# ─────────────────────────────────────────────
def render_logo():
    components.html("""
    <style>body { margin: 0; padding: 0; }</style>
    <div style="text-align:center; font-family:'DM Sans', sans-serif;">
        <span style="font-size:2.8rem; display:block; margin-bottom:0.3rem;
              filter:drop-shadow(0 0 14px rgba(232,146,58,0.5));">⚓</span>
        <div style="font-family:'Lora',serif; font-size:1.6rem; color:#e8923a;
             letter-spacing:0.08em; font-weight:600;">ANCHOR</div>
        <div style="font-size:0.78rem; color:#9e8e7a; letter-spacing:0.12em;
             text-transform:uppercase; margin-top:4px;">Day Closing Signal System</div>
    </div>
    """, height=160)


# ─────────────────────────────────────────────
# STEP 0: Landing & Trigger
# ─────────────────────────────────────────────
def render_step_0():
    render_logo()

    # Urgency card
    components.html("""
    <style>body { margin: 0; padding: 0; }</style>
    <div style="
        font-family: 'DM Sans', sans-serif;
        background: linear-gradient(135deg, #1c1510 0%, #1a1208 100%);
        border: 1px solid rgba(232,146,58,0.25);
        border-radius: 14px;
        padding: 1.6rem;
        text-align: center;
    ">
        <div style="font-family:'Lora',serif; font-size:1.1rem; color:#e8923a;
             margin-bottom:0.6rem;">Brain Shutdown Failure</div>
        <div style="font-size:0.85rem; color:#9e8e7a; line-height:1.7;">
            Tanpa penanda waktu yang jelas, otakmu sulit membedakan kapan "mode kerja"
            berakhir dan istirahat dimulai. Hasilnya?
        </div>
        <ul style="text-align:left; margin:1rem 0 0 0; padding:0; list-style:none;">
            <li style="font-size:0.82rem; color:#9e8e7a; padding:4px 0;
                display:flex; align-items:flex-start; gap:8px; line-height:1.5;">
                <span style="color:#e8923a; font-size:1.2rem; line-height:1.1;
                      flex-shrink:0;">·</span>
                Scrolling tanpa tujuan hingga larut malam
            </li>
            <li style="font-size:0.82rem; color:#9e8e7a; padding:4px 0;
                display:flex; align-items:flex-start; gap:8px; line-height:1.5;">
                <span style="color:#e8923a; font-size:1.2rem; line-height:1.1;
                      flex-shrink:0;">·</span>
                Pikiran racing saat berbaring — tugas, deadline, kekhawatiran
            </li>
            <li style="font-size:0.82rem; color:#9e8e7a; padding:4px 0;
                display:flex; align-items:flex-start; gap:8px; line-height:1.5;">
                <span style="color:#e8923a; font-size:1.2rem; line-height:1.1;
                      flex-shrink:0;">·</span>
                Bangun pagi dengan energi habis sebelum hari dimulai
            </li>
            <li style="font-size:0.82rem; color:#9e8e7a; padding:4px 0;
                display:flex; align-items:flex-start; gap:8px; line-height:1.5;">
                <span style="color:#e8923a; font-size:1.2rem; line-height:1.1;
                      flex-shrink:0;">·</span>
                Perasaan bersalah yang menempel sepanjang malam
            </li>
        </ul>
    </div>
    """, height=380)

    # Solution card
    components.html("""
    <style>body { margin: 0; padding: 0; }</style>
    <div style="
        font-family: 'DM Sans', sans-serif;
        background: #1c1915;
        border: 1px solid rgba(232,146,58,0.25);
        border-radius: 14px;
        padding: 1.5rem 1.6rem;
    ">
        <div style="font-size:0.7rem; color:#e8923a; letter-spacing:0.2em;
             text-transform:uppercase; font-weight:500; margin-bottom:0.6rem;">Solusinya?</div>
        <div style="font-size:0.88rem; color:#9e8e7a; line-height:1.7;">
            <strong style="color:#f2e8d9;">Anchor</strong> adalah ritual 3-langkah
            yang menciptakan sinyal penutup hari yang konsisten. Seperti lampu merah yang
            memberi tahu otak: <em style="color:#e8923a;">"Hari ini selesai. Aman untuk istirahat."</em>
        </div>
        <div style="height:1px; background:linear-gradient(90deg,transparent,
             rgba(232,146,58,0.25),transparent); margin:1.2rem 0;"></div>
        <div style="display:flex; gap:1rem; font-size:0.78rem; color:#5c5040;">
            <span>🔒 Mental Vault</span>
            <span>🎵 Sensory Signal</span>
            <span>🌿 Anchor Ritual</span>
        </div>
    </div>
    """, height=250)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⚓ Aktifkan Anchor Mode", key="start_btn"):
        st.session_state.step = 1
        st.rerun()

    components.html("""
    <style>body { margin: 0; padding: 0; }</style>
    <div style="font-family: 'DM Sans', sans-serif; text-align:center; margin-top:1rem; font-size:0.75rem; color:#5c5040;">
        Estimasi waktu: ~3 menit
    </div>
    """, height=50)


# ─────────────────────────────────────────────
# STEP 1: The Mental Vault
# ─────────────────────────────────────────────
def render_step_1():
    render_progress(1)

    components.html("""
    <style>body { margin: 0; padding: 0; }</style>
    <div style="font-family: 'DM Sans', sans-serif; text-align:center;">
        <div style="font-size:0.7rem; color:#e8923a; letter-spacing:0.2em;
             text-transform:uppercase; font-weight:500; margin-bottom:0.5rem;">
             Langkah 1 dari 3</div>
        <div style="font-family:'Lora',serif; font-size:1.5rem; color:#f2e8d9;
             font-weight:600; line-height:1.3;">The Mental Vault 🔒</div>
        <div style="font-size:0.88rem; color:#9e8e7a; margin-top:0.5rem; line-height:1.6;">
            Pikiran yang tidak ditulis akan terus berputar.
            Titipkan satu beban ke sistem — bukan untuk dilupakan,
            tapi agar otakmu bisa berhenti menjaganya.
        </div>
    </div>
    """, height=200)

    if not st.session_state.vault_submitted:
        # Native input
        thought = st.text_area(
            label="Apa yang paling mengganggumu malam ini?",
            placeholder="Contoh: Besok ada ujian Kalkulus dan aku belum baca bab 4...\n\nTuliskan apa saja. Tidak ada yang menghakimi.",
            height=130,
            key="vault_input",
            help="Satu pikiran, tugas, atau kekhawatiran. Singkat atau panjang, terserahmu."
        )

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("🔒 Titipkan ke Vault", key="vault_btn"):
                if thought.strip():
                    st.session_state.vault_thought = thought.strip()
                    with st.spinner("Mengunci beban pikiran ke sistem..."):
                        time.sleep(1.8)
                    st.session_state.vault_submitted = True
                    st.rerun()
                else:
                    st.warning("Tuliskan dulu apa yang ada di pikiranmu — sekecil apapun itu.")
        with col2:
            if st.button("Lewati", key="skip_vault"):
                st.session_state.vault_submitted = True
                st.session_state.vault_thought = "(Kosong — Kamu memilih untuk tidak menulis)"
                st.rerun()

    else:
        # Preview thought yang tersimpan
        if st.session_state.vault_thought and not st.session_state.vault_thought.startswith("("):
            preview = st.session_state.vault_thought[:120]
            suffix = "..." if len(st.session_state.vault_thought) > 120 else ""
            
            components.html(f"""
            <style>body {{ margin: 0; padding: 0; }}</style>
            <div style="
                font-family: 'DM Sans', sans-serif;
                background: #1c1915;
                border: 1px solid rgba(100,100,80,0.3);
                border-radius: 14px;
                padding: 1.2rem 1.4rem;
            ">
                <div style="font-size:0.72rem; color:#5c5040; margin-bottom:0.5rem;
                     letter-spacing:0.1em; text-transform:uppercase;">Yang tersimpan:</div>
                <div style="font-family:'Lora',serif; font-size:0.9rem; color:#9e8e7a;
                     font-style:italic; line-height:1.6;">"{preview}{suffix}"</div>
            </div>
            """, height=160)

        # Konfirmasi vault
        components.html("""
        <style>body { margin: 0; padding: 0; }</style>
        <div style="
            font-family: 'DM Sans', sans-serif;
            background: rgba(94,148,94,0.15);
            border: 1px solid rgba(94,148,94,0.35);
            border-radius: 12px;
            padding: 1.4rem 1.5rem;
            text-align: center;
        ">
            <span style="font-size:2rem; margin-bottom:0.6rem; display:block;">✅</span>
            <div style="font-family:'Lora',serif; color:#a8d5a8; font-size:1rem;
                 font-weight:600; margin-bottom:0.5rem;">Tersimpan dengan Aman</div>
            <div style="font-size:0.82rem; color:#88bb88; line-height:1.65;">
                Beban ini sudah tercatat dan aman di sistem.<br>
                <strong style="color:#a8d5a8;">Kamu punya izin untuk tidak memikirkannya malam ini.</strong><br><br>
                Besok pagi, kamu bisa kembali ke sini dengan pikiran yang segar.
                Otak yang istirahat selalu berpikir lebih jernih dari otak yang kelelahan.
            </div>
        </div>
        """, height=300)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Lanjut ke Sinyal Sensorik →", key="to_step2"):
            st.session_state.step = 2
            st.rerun()


# ─────────────────────────────────────────────
# STEP 2: Sensory Signals
# ─────────────────────────────────────────────
def render_step_2():
    render_progress(2)

    components.html("""
    <style>body { margin: 0; padding: 0; }</style>
    <div style="font-family: 'DM Sans', sans-serif; text-align:center;">
        <div style="font-size:0.7rem; color:#e8923a; letter-spacing:0.2em;
             text-transform:uppercase; font-weight:500; margin-bottom:0.5rem;">
             Langkah 2 dari 3</div>
        <div style="font-family:'Lora',serif; font-size:1.5rem; color:#f2e8d9;
             font-weight:600; line-height:1.3;">Sensory Signals 🌙</div>
        <div style="font-size:0.88rem; color:#9e8e7a; margin-top:0.5rem; line-height:1.6;">
            Ubah lingkunganmu. Sinyal fisik memberi tahu sistem saraf
            bahwa hari sudah berakhir — jauh lebih kuat dari tekad semata.
        </div>
    </div>
    """, height=180)

    # ── Instruction rows — inline styles penuh ──
    def instruction_row(num: str, html_text: str, is_last: bool = False):
        border = "" if is_last else "border-bottom: 1px solid rgba(255,255,255,0.04);"
        return f"""
        <div style="display:flex; align-items:flex-start; gap:14px;
             padding:0.9rem 0; {border}">
            <div style="
                width:28px; height:28px; border-radius:50%;
                background:rgba(232,146,58,0.12);
                border:1px solid rgba(232,146,58,0.25);
                color:#e8923a; font-size:0.75rem; font-weight:500;
                display:flex; align-items:center; justify-content:center;
                flex-shrink:0; margin-top:1px;">{num}</div>
            <div style="font-size:0.87rem; color:#9e8e7a; line-height:1.6;">
                {html_text}
            </div>
        </div>
        """

    rows_html = (
        instruction_row("1",
            "<strong style='color:#f2e8d9;font-weight:500;'>Redupkan atau matikan lampu utama.</strong> "
            "Cahaya terang menghambat produksi melatonin. Gunakan lampu kuning/redup jika ada.")
        + instruction_row("2",
            "<strong style='color:#f2e8d9;font-weight:500;'>Letakkan ponsel menghadap ke bawah</strong> "
            "setelah memulai audio. Kamu tidak perlu melihat layar ini untuk mendengarkan.")
        + instruction_row("3",
            "<strong style='color:#f2e8d9;font-weight:500;'>Putar audio di bawah.</strong> "
            "Biarkan suara ini menggantikan kebisingan pikiran dengan sinyal yang menenangkan.",
            is_last=True)
    )

    components.html(f"""
    <style>body {{ margin: 0; padding: 0; }}</style>
    <div style="
        font-family: 'DM Sans', sans-serif;
        background:#1c1915;
        border:1px solid rgba(232,146,58,0.25);
        border-radius:14px;
        padding:1.5rem 1.6rem;
    ">
        <div style="font-size:0.8rem; color:#e8923a; letter-spacing:0.12em;
             text-transform:uppercase; margin-bottom:0.8rem;">Lakukan sekarang</div>
        {rows_html}
    </div>
    """, height=380)

    # Audio card (Bagian Atas - Header)
    components.html("""
    <style>body { margin: 0; padding: 0; }</style>
    <div style="
        font-family: 'DM Sans', sans-serif;
        background:#1c1915;
        border:1px solid rgba(232,146,58,0.25);
        border-radius:14px;
        padding:1.2rem 1.5rem;
    ">
        <div style="font-size:0.8rem; color:#5c5040; margin-bottom:0.6rem;
             letter-spacing:0.08em;">🎵 Ambient Sound — Hujan Malam</div>
    </div>
    """, height=80)

    # Audio (Native Streamlit)
    st.audio(
        "https://upload.wikimedia.org/wikipedia/commons/transcoded/3/36/"
        "Thunderstorm_in_the_night.ogg/Thunderstorm_in_the_night.ogg.mp3",
        format="audio/mp3",
    )

    # Audio card (Bagian Bawah - Footer)
    components.html("""
    <style>body { margin: 0; padding: 0; }</style>
    <div style="
        font-family: 'DM Sans', sans-serif;
        background:#1c1915;
        border:1px solid rgba(232,146,58,0.25);
        border-radius:14px;
        padding:1.2rem 1.5rem;
    ">
        <div style="font-size:0.75rem; color:#5c5040; line-height:1.5;">
            Tidak ada audio? Tenang — lanjutkan saja ke ritual berikutnya.
            Atau nyalakan musik instrumental favoritmu dengan volume rendah.
        </div>
    </div>
    """, height=120)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Saya Siap — Mulai Ritual Fisik →", key="to_step3"):
        st.session_state.step = 3
        st.rerun()


# ─────────────────────────────────────────────
# STEP 3: The Anchor Ritual (Timer)
# ─────────────────────────────────────────────
def render_step_3():
    render_progress(3)

    if st.session_state.timer_done:
        render_completion()
        return

    components.html("""
    <style>body { margin: 0; padding: 0; }</style>
    <div style="font-family: 'DM Sans', sans-serif; text-align:center;">
        <div style="font-size:0.7rem; color:#e8923a; letter-spacing:0.2em;
             text-transform:uppercase; font-weight:500; margin-bottom:0.5rem;">
             Langkah 3 dari 3</div>
        <div style="font-family:'Lora',serif; font-size:1.5rem; color:#f2e8d9;
             font-weight:600; line-height:1.3;">The Anchor Ritual 🌿</div>
        <div style="font-size:0.88rem; color:#9e8e7a; margin-top:0.5rem; line-height:1.6;">
            Satu menit. Gerakan fisik ringan untuk memutus siklus
            pikiran dan memberi sinyal pada tubuh bahwa sudah waktunya berhenti.
        </div>
    </div>
    """, height=200)

    # ── Ritual options — inline styles penuh ──
    def ritual_row(icon: str, title: str, desc: str, is_last: bool = False):
        border = "" if is_last else "border-bottom:1px solid rgba(255,255,255,0.04);"
        return f"""
        <div style="display:flex; align-items:flex-start; gap:12px;
             padding:0.7rem 0; {border}">
            <span style="font-size:1.1rem; flex-shrink:0; margin-top:1px;">{icon}</span>
            <div style="font-size:0.84rem; color:#9e8e7a; line-height:1.6;">
                <strong style="color:#f2e8d9; font-weight:500;">{title}</strong><br>
                {desc}
            </div>
        </div>
        """

    rituals_html = (
        ritual_row("🫁", "Pernapasan Kotak (Box Breathing)",
            "Tarik napas 4 hitungan → tahan 4 hitungan → buang 4 hitungan → tahan 4 hitungan. "
            "Ulangi terus.")
        + ritual_row("🧘", "Peregangan Leher &amp; Bahu",
            "Miringkan kepala ke kanan, tahan 8 detik. Ke kiri, tahan 8 detik. "
            "Putar bahu ke belakang perlahan. Ulangi.")
        + ritual_row("🤲", "Progressive Muscle Relaxation",
            "Kencangkan seluruh otot tubuh selama 5 detik, lalu lepaskan. "
            "Rasakan perbedaan antara tegang dan rileks.",
            is_last=True)
    )

    components.html(f"""
    <style>body {{ margin: 0; padding: 0; }}</style>
    <div style="
        font-family: 'DM Sans', sans-serif;
        background:#1c1915;
        border:1px solid rgba(232,146,58,0.25);
        border-radius:14px;
        padding:1.5rem 1.6rem;
    ">
        <div style="font-size:0.8rem; color:#e8923a; letter-spacing:0.12em;
             text-transform:uppercase; margin-bottom:0.8rem;">
            Pilih satu ritual (lakukan selama timer berjalan)
        </div>
        {rituals_html}
    </div>
    """, height=380)

    st.markdown("<br>", unsafe_allow_html=True)

    if not st.session_state.ritual_started:
        if st.button("▶ Mulai Timer 60 Detik", key="start_timer"):
            st.session_state.ritual_started = True
            st.rerun()
    else:
        timer_placeholder = st.empty()

        breathing_phases = [
            ("🫁", "Tarik napas..."),
            ("⏸", "Tahan..."),
            ("💨", "Buang napas..."),
            ("⏸", "Tahan..."),
        ]

        # Timer logic via updating the component layout directly
        for i in range(60, -1, -1):
            phase_idx = ((60 - i) // 4) % 4
            phase_icon, phase_text = breathing_phases[phase_idx]

            html_timer = f"""
            <style>body {{ margin: 0; padding: 0; }}</style>
            <div style="
                font-family: 'DM Sans', sans-serif;
                background:#1c1915;
                border:1px solid rgba(232,146,58,0.25);
                border-radius:14px;
                padding:1.5rem 1.6rem;
                box-shadow:0 0 30px rgba(232,146,58,0.12), inset 0 1px 0 rgba(255,255,255,0.03);
            ">
                <div style="text-align:center; padding:2rem 1rem;">
                    <div style="
                        width:160px; height:160px; border-radius:50%;
                        border:3px solid rgba(232,146,58,0.25);
                        display:flex; flex-direction:column;
                        align-items:center; justify-content:center;
                        margin:0 auto 1.2rem;
                        background:rgba(232,146,58,0.12);
                        box-shadow:0 0 40px rgba(232,146,58,0.12),
                                   inset 0 0 30px rgba(0,0,0,0.3);
                    ">
                        <div style="font-family:'Lora',serif; font-size:3rem;
                             color:#e8923a; line-height:1; font-weight:600;">{i}</div>
                        <div style="font-size:0.72rem; color:#9e8e7a;
                             letter-spacing:0.15em; text-transform:uppercase;
                             margin-top:2px;">detik</div>
                    </div>
                    <div style="font-size:0.82rem; color:#9e8e7a; font-style:italic;">
                        {phase_icon} {phase_text}
                    </div>
                </div>
            </div>
            """
            
            with timer_placeholder.container():
                components.html(html_timer, height=380)

            time.sleep(1)

        st.session_state.timer_done = True
        st.rerun()


# ─────────────────────────────────────────────
# COMPLETION SCREEN
# ─────────────────────────────────────────────
def render_completion():
    components.html("""
    <style>body { margin: 0; padding: 0; }</style>
    <div style="font-family: 'DM Sans', sans-serif; text-align:center; padding:1rem 0;">
        <span style="font-size:3.5rem; display:block; margin-bottom:1rem;">🌙</span>
        <div style="font-family:'Lora',serif; font-size:1.4rem; color:#e8923a;
             margin-bottom:0.8rem;">Ritual Selesai</div>
        <div style="font-size:0.88rem; color:#9e8e7a; line-height:1.7;
             max-width:340px; margin:0 auto 1.5rem;">
            Otak siap <em>shutdown</em>.<br><br>
            Kamu telah menutup hari ini dengan benar —
            pikiran tersimpan, tubuh rileks, lingkungan mendukung.<br><br>
            <strong style="color:#e8923a;">Silakan letakkan perangkat ini.</strong><br>
            Besok pagi menantimu dengan energi yang baru.
        </div>
    </div>
    """, height=380)

    components.html("""
    <style>body { margin: 0; padding: 0; }</style>
    <div style="
        font-family: 'DM Sans', sans-serif;
        background:#1c1915;
        border:1px solid rgba(232,146,58,0.25);
        border-radius:14px;
        padding:1.2rem;
        text-align:center;
    ">
        <div style="font-size:0.75rem; color:#5c5040; line-height:1.6;">
            "Rest is not idle; it is the work that makes all other work possible."<br>
            <span style="font-size:0.7rem;">— Alex Soojung-Kim Pang</span>
        </div>
    </div>
    """, height=120)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("↩ Mulai Dari Awal", key="restart"):
            for key in ['step', 'vault_submitted', 'vault_thought',
                        'timer_started', 'timer_done', 'ritual_started']:
                if key in st.session_state:
                    del st.session_state[key]
            init_state()
            st.rerun()


# ─────────────────────────────────────────────
# MAIN ROUTER
# ─────────────────────────────────────────────
def main():
    step = st.session_state.step
    if step == 0:
        render_step_0()
    elif step == 1:
        render_step_1()
    elif step == 2:
        render_step_2()
    elif step == 3:
        render_step_3()
    else:
        st.session_state.step = 0
        st.rerun()


if __name__ == "__main__" or True:
    main()