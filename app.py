"""
Anchor - The Day Closing Signal System
MVP untuk mengatasi Brain Shutdown Failure pada mahasiswa perantau ITS.

Arsitektur: Linear 4-Step Flow menggunakan st.session_state
Step 0: Landing & Trigger
Step 1: The Mental Vault
Step 2: Sensory Signals
Step 3: The Anchor Ritual (Timer)
"""

import streamlit as st
import time

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
# CUSTOM CSS — Warm Dark Mode
# Target: mereduksi blue light, feel tenang & intimate
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Import Font ── */
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root Variables ── */
:root {
    --bg-deep:       #0f0d0b;
    --bg-card:       #1c1915;
    --bg-input:      #231f1a;
    --amber:         #e8923a;
    --amber-soft:    #c97d30;
    --amber-glow:    rgba(232, 146, 58, 0.12);
    --amber-border:  rgba(232, 146, 58, 0.25);
    --text-primary:  #f2e8d9;
    --text-muted:    #9e8e7a;
    --text-dim:      #5c5040;
    --success-bg:    rgba(94, 148, 94, 0.15);
    --success-border:rgba(94, 148, 94, 0.35);
    --success-text:  #a8d5a8;
}

/* ── Reset & Global ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg-deep) !important;
    color: var(--text-primary) !important;
}

/* Hilangkan default Streamlit padding */
.main .block-container {
    padding: 2rem 1.5rem 4rem !important;
    max-width: 600px !important;
    margin: 0 auto !important;
}

/* ── Hide Streamlit Chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Progress Bar Ritual ── */
.progress-bar-container {
    display: flex;
    gap: 8px;
    margin-bottom: 2.5rem;
    padding: 0 4px;
}
.progress-step {
    flex: 1;
    height: 3px;
    border-radius: 99px;
    background: var(--text-dim);
    transition: background 0.5s ease;
}
.progress-step.active {
    background: var(--amber);
    box-shadow: 0 0 8px var(--amber);
}

/* ── Logo / Brand ── */
.anchor-logo {
    text-align: center;
    margin-bottom: 2.5rem;
}
.anchor-logo .icon {
    font-size: 2.8rem;
    display: block;
    margin-bottom: 0.3rem;
    filter: drop-shadow(0 0 14px rgba(232,146,58,0.5));
}
.anchor-logo .brand {
    font-family: 'Lora', serif;
    font-size: 1.6rem;
    color: var(--amber);
    letter-spacing: 0.08em;
    font-weight: 600;
}
.anchor-logo .tagline {
    font-size: 0.78rem;
    color: var(--text-muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ── Step Header ── */
.step-header {
    text-align: center;
    margin-bottom: 1.8rem;
}
.step-label {
    font-size: 0.7rem;
    color: var(--amber);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    font-weight: 500;
    margin-bottom: 0.5rem;
}
.step-title {
    font-family: 'Lora', serif;
    font-size: 1.5rem;
    color: var(--text-primary);
    font-weight: 600;
    line-height: 1.3;
}
.step-subtitle {
    font-size: 0.88rem;
    color: var(--text-muted);
    margin-top: 0.5rem;
    line-height: 1.6;
}

/* ── Card ── */
.card {
    background: var(--bg-card);
    border: 1px solid var(--amber-border);
    border-radius: 14px;
    padding: 1.5rem 1.6rem;
    margin-bottom: 1.2rem;
}
.card-amber-glow {
    box-shadow: 0 0 30px var(--amber-glow), inset 0 1px 0 rgba(255,255,255,0.03);
}

/* ── Urgency Banner (Step 0) ── */
.urgency-card {
    background: linear-gradient(135deg, #1c1510 0%, #1a1208 100%);
    border: 1px solid var(--amber-border);
    border-radius: 14px;
    padding: 1.6rem;
    margin-bottom: 1.6rem;
    text-align: center;
}
.urgency-title {
    font-family: 'Lora', serif;
    font-size: 1.1rem;
    color: var(--amber);
    margin-bottom: 0.6rem;
}
.urgency-body {
    font-size: 0.85rem;
    color: var(--text-muted);
    line-height: 1.7;
}
.symptom-list {
    text-align: left;
    margin: 1rem 0 0 0;
    padding: 0;
    list-style: none;
}
.symptom-list li {
    font-size: 0.82rem;
    color: var(--text-muted);
    padding: 4px 0;
    display: flex;
    align-items: flex-start;
    gap: 8px;
    line-height: 1.5;
}
.symptom-list li::before {
    content: "·";
    color: var(--amber);
    font-size: 1.2rem;
    line-height: 1.1;
    flex-shrink: 0;
}

/* ── Buttons ── */
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

/* Secondary button style */
div[data-testid="column"]:last-child div.stButton > button {
    background: var(--bg-card) !important;
    color: var(--text-muted) !important;
    border: 1px solid var(--amber-border) !important;
    box-shadow: none !important;
}

/* ── Text Area ── */
div.stTextArea > label {
    font-size: 0.88rem !important;
    color: var(--text-muted) !important;
    font-family: 'DM Sans', sans-serif !important;
}
div.stTextArea textarea {
    background-color: var(--bg-input) !important;
    border: 1px solid var(--amber-border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'Lora', serif !important;
    font-size: 0.95rem !important;
    line-height: 1.7 !important;
    caret-color: var(--amber) !important;
}
div.stTextArea textarea:focus {
    border-color: var(--amber) !important;
    box-shadow: 0 0 0 2px var(--amber-glow) !important;
}

/* ── Vault Confirmation ── */
.vault-confirm {
    background: var(--success-bg);
    border: 1px solid var(--success-border);
    border-radius: 12px;
    padding: 1.4rem 1.5rem;
    text-align: center;
    margin: 1rem 0;
}
.vault-confirm .vault-icon {
    font-size: 2rem;
    margin-bottom: 0.6rem;
    display: block;
}
.vault-confirm .vault-title {
    font-family: 'Lora', serif;
    color: var(--success-text);
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}
.vault-confirm .vault-msg {
    font-size: 0.82rem;
    color: #88bb88;
    line-height: 1.65;
}

/* ── Sensory Instructions ── */
.instruction-row {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 0.9rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.instruction-row:last-child { border-bottom: none; }
.instruction-num {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: var(--amber-glow);
    border: 1px solid var(--amber-border);
    color: var(--amber);
    font-size: 0.75rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 1px;
}
.instruction-text {
    font-size: 0.87rem;
    color: var(--text-muted);
    line-height: 1.6;
}
.instruction-text strong {
    color: var(--text-primary);
    font-weight: 500;
}

/* ── Timer Display ── */
.timer-container {
    text-align: center;
    padding: 2rem 1rem;
}
.timer-ring {
    width: 160px;
    height: 160px;
    border-radius: 50%;
    border: 3px solid var(--amber-border);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1.2rem;
    background: var(--amber-glow);
    box-shadow: 0 0 40px var(--amber-glow), inset 0 0 30px rgba(0,0,0,0.3);
}
.timer-seconds {
    font-family: 'Lora', serif;
    font-size: 3rem;
    color: var(--amber);
    line-height: 1;
    font-weight: 600;
}
.timer-label {
    font-size: 0.72rem;
    color: var(--text-muted);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 2px;
}
.breathing-guide {
    font-size: 0.82rem;
    color: var(--text-muted);
    font-style: italic;
}

/* ── Ritual Steps ── */
.ritual-step {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 0.7rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.ritual-step:last-child { border-bottom: none; }
.ritual-icon {
    font-size: 1.1rem;
    flex-shrink: 0;
    margin-top: 1px;
}
.ritual-text {
    font-size: 0.84rem;
    color: var(--text-muted);
    line-height: 1.6;
}

/* ── Divider ── */
.soft-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--amber-border), transparent);
    margin: 1.5rem 0;
}

/* ── Completion Screen ── */
.completion-screen {
    text-align: center;
    padding: 1rem 0;
}
.completion-icon {
    font-size: 3.5rem;
    display: block;
    margin-bottom: 1rem;
    animation: fadeIn 1s ease;
}
.completion-title {
    font-family: 'Lora', serif;
    font-size: 1.4rem;
    color: var(--amber);
    margin-bottom: 0.8rem;
}
.completion-msg {
    font-size: 0.88rem;
    color: var(--text-muted);
    line-height: 1.7;
    max-width: 340px;
    margin: 0 auto 1.5rem;
}

/* ── Animations ── */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.fade-in {
    animation: fadeIn 0.6s ease forwards;
}

/* ── Streamlit info/warning overrides ── */
div[data-testid="stAlert"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--amber-border) !important;
    border-radius: 10px !important;
    color: var(--text-muted) !important;
}

/* ── Audio Player ── */
audio {
    width: 100%;
    margin-top: 0.5rem;
    filter: sepia(0.5) hue-rotate(20deg);
}

/* ── Metric overrides ── */
div[data-testid="stMetric"] {
    background: transparent !important;
    text-align: center !important;
}
div[data-testid="stMetricValue"] {
    font-family: 'Lora', serif !important;
    color: var(--amber) !important;
    font-size: 2.2rem !important;
}

/* ── Mobile responsiveness ── */
@media (max-width: 640px) {
    .main .block-container { padding: 1.5rem 1rem 3rem !important; }
    .anchor-logo .brand { font-size: 1.4rem; }
    .step-title { font-size: 1.3rem; }
    .timer-ring { width: 140px; height: 140px; }
    .timer-seconds { font-size: 2.6rem; }
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SESSION STATE INITIALIZATION
# ─────────────────────────────────────────────
def init_state():
    """Inisialisasi semua state yang diperlukan."""
    defaults = {
        'step': 0,              # Step saat ini: 0-3 (+ 4 = complete)
        'vault_submitted': False,  # Apakah user sudah submit vault
        'vault_thought': '',    # Isi thought di vault
        'timer_started': False, # Apakah timer sudah dimulai
        'timer_done': False,    # Apakah timer sudah selesai
        'ritual_started': False,# Apakah ritual sudah dimulai (untuk cegah timer ulang)
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_state()


# ─────────────────────────────────────────────
# HELPER: Render Progress Bar
# ─────────────────────────────────────────────
def render_progress(current_step: int):
    """Render progress indicator 4-step di atas halaman."""
    steps = current_step  # steps 0-3, active = steps yang sudah lewat
    html = '<div class="progress-bar-container">'
    for i in range(1, 4):  # 3 bar untuk step 1, 2, 3
        css_class = "progress-step active" if i <= steps else "progress-step"
        html += f'<div class="{css_class}"></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPER: Render Logo
# ─────────────────────────────────────────────
def render_logo():
    """Render brand header Anchor."""
    st.markdown("""
    <div class="anchor-logo fade-in">
        <span class="icon">⚓</span>
        <div class="brand">ANCHOR</div>
        <div class="tagline">Day Closing Signal System</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STEP 0: Landing & Trigger
# ─────────────────────────────────────────────
def render_step_0():
    render_logo()

    # Urgency card — menjelaskan masalah
    st.markdown("""
    <div class="urgency-card fade-in">
        <div class="urgency-title">Brain Shutdown Failure</div>
        <div class="urgency-body">
            Tanpa penanda waktu yang jelas, otakmu sulit membedakan kapan "mode kerja" 
            berakhir dan istirahat dimulai. Hasilnya?
        </div>
        <ul class="symptom-list">
            <li>Scrolling tanpa tujuan hingga larut malam</li>
            <li>Pikiran racing saat berbaring — tugas, deadline, kekhawatiran</li>
            <li>Bangun pagi dengan energi habis sebelum hari dimulai</li>
            <li>Perasaan bersalah yang menempel sepanjang malam</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Penjelasan solusi
    st.markdown("""
    <div class="card fade-in">
        <div class="step-label" style="margin-bottom:0.6rem;">Solusinya?</div>
        <div style="font-size:0.88rem; color: var(--text-muted); line-height:1.7;">
            <strong style="color:var(--text-primary);">Anchor</strong> adalah ritual 3-langkah 
            yang menciptakan sinyal penutup hari yang konsisten. Seperti lampu merah yang 
            memberi tahu otak: <em style="color:var(--amber);">"Hari ini selesai. Aman untuk istirahat."</em>
        </div>
        <div class="soft-divider"></div>
        <div style="display:flex; gap:1rem; font-size:0.78rem; color:var(--text-dim);">
            <span>🔒 Mental Vault</span>
            <span>🎵 Sensory Signal</span>
            <span>🌿 Anchor Ritual</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # CTA Button
    if st.button("⚓ Aktifkan Anchor Mode", key="start_btn"):
        st.session_state.step = 1
        st.rerun()

    st.markdown("""
    <div style="text-align:center; margin-top:1rem; font-size:0.75rem; color:var(--text-dim);">
        Estimasi waktu: ~3 menit
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STEP 1: The Mental Vault
# ─────────────────────────────────────────────
def render_step_1():
    render_progress(1)

    st.markdown("""
    <div class="step-header fade-in">
        <div class="step-label">Langkah 1 dari 3</div>
        <div class="step-title">The Mental Vault 🔒</div>
        <div class="step-subtitle">
            Pikiran yang tidak ditulis akan terus berputar. 
            Titipkan satu beban ke sistem — bukan untuk dilupakan, 
            tapi agar otakmu bisa berhenti menjaganya.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Jika belum submit → tampilkan form
    if not st.session_state.vault_submitted:
        st.markdown('<div class="card card-amber-glow fade-in">', unsafe_allow_html=True)

        thought = st.text_area(
            label="Apa yang paling mengganggumu malam ini?",
            placeholder="Contoh: Besok ada ujian Kalkulus dan aku belum baca bab 4...\n\nTuliskan apa saja. Tidak ada yang menghakimi.",
            height=130,
            key="vault_input",
            help="Satu pikiran, tugas, atau kekhawatiran. Singkat atau panjang, terserahmu."
        )

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("🔒 Titipkan ke Vault", key="vault_btn"):
                if thought.strip():
                    # Simpan thought ke session state
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

    # Jika sudah submit → tampilkan konfirmasi
    else:
        # Preview pikiran yang disubmit
        if st.session_state.vault_thought and not st.session_state.vault_thought.startswith("("):
            st.markdown(f"""
            <div class="card fade-in" style="border-color: rgba(100,100,80,0.3);">
                <div style="font-size:0.72rem; color:var(--text-dim); margin-bottom:0.5rem; letter-spacing:0.1em; text-transform:uppercase;">Yang tersimpan:</div>
                <div style="font-family:'Lora',serif; font-size:0.9rem; color:var(--text-muted); font-style:italic; line-height:1.6;">
                    "{st.session_state.vault_thought[:120]}{'...' if len(st.session_state.vault_thought) > 120 else ''}"
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Pesan validasi psikologis
        st.markdown("""
        <div class="vault-confirm fade-in">
            <span class="vault-icon">✅</span>
            <div class="vault-title">Tersimpan dengan Aman</div>
            <div class="vault-msg">
                Beban ini sudah tercatat dan aman di sistem.<br>
                <strong style="color:var(--success-text);">Kamu punya izin untuk tidak memikirkannya malam ini.</strong><br><br>
                Besok pagi, kamu bisa kembali ke sini dengan pikiran yang segar. 
                Otak yang istirahat selalu berpikir lebih jernih dari otak yang kelelahan.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Lanjut ke Sinyal Sensorik →", key="to_step2"):
            st.session_state.step = 2
            st.rerun()


# ─────────────────────────────────────────────
# STEP 2: Sensory Signals
# ─────────────────────────────────────────────
def render_step_2():
    render_progress(2)

    st.markdown("""
    <div class="step-header fade-in">
        <div class="step-label">Langkah 2 dari 3</div>
        <div class="step-title">Sensory Signals 🌙</div>
        <div class="step-subtitle">
            Ubah lingkunganmu. Sinyal fisik memberi tahu sistem saraf 
            bahwa hari sudah berakhir — jauh lebih kuat dari tekad semata.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Instruksi lingkungan
    st.markdown("""
    <div class="card fade-in">
        <div style="font-size:0.8rem; color:var(--amber); letter-spacing:0.12em; text-transform:uppercase; margin-bottom:0.8rem;">Lakukan sekarang</div>
        
        <div class="instruction-row">
            <div class="instruction-num">1</div>
            <div class="instruction-text">
                <strong>Redupkan atau matikan lampu utama.</strong> Cahaya terang 
                menghambat produksi melatonin. Gunakan lampu kuning/redup jika ada.
            </div>
        </div>
        
        <div class="instruction-row">
            <div class="instruction-num">2</div>
            <div class="instruction-text">
                <strong>Letakkan ponsel menghadap ke bawah</strong> setelah memulai audio. 
                Kamu tidak perlu melihat layar ini untuk mendengarkan.
            </div>
        </div>
        
        <div class="instruction-row">
            <div class="instruction-num">3</div>
            <div class="instruction-text">
                <strong>Putar audio di bawah.</strong> Biarkan suara ini menggantikan 
                kebisingan pikiran dengan sinyal yang menenangkan.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Audio Player
    st.markdown("""
    <div class="card fade-in" style="padding:1.2rem 1.5rem;">
        <div style="font-size:0.8rem; color:var(--text-dim); margin-bottom:0.6rem; letter-spacing:0.08em;">
            🎵 Ambient Sound — Hujan Malam
        </div>
    """, unsafe_allow_html=True)

    # Audio dari sumber publik domain yang reliabel
    # Menggunakan freesound-compatible / public domain URL
    st.audio(
        "https://upload.wikimedia.org/wikipedia/commons/transcoded/3/36/Thunderstorm_in_the_night.ogg/Thunderstorm_in_the_night.ogg.mp3",
        format="audio/mp3"
    )

    st.markdown("""
        <div style="font-size:0.75rem; color:var(--text-dim); margin-top:0.5rem;">
            Tidak ada audio? Tenang — lanjutkan saja ke ritual berikutnya. 
            Atau nyalakan musik instrumental favoritmu dengan volume rendah.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Saya Siap — Mulai Ritual Fisik →", key="to_step3"):
        st.session_state.step = 3
        st.rerun()


# ─────────────────────────────────────────────
# STEP 3: The Anchor Ritual (Timer)
# ─────────────────────────────────────────────
def render_step_3():
    render_progress(3)

    # Jika timer sudah selesai → tampilkan completion screen
    if st.session_state.timer_done:
        render_completion()
        return

    st.markdown("""
    <div class="step-header fade-in">
        <div class="step-label">Langkah 3 dari 3</div>
        <div class="step-title">The Anchor Ritual 🌿</div>
        <div class="step-subtitle">
            Satu menit. Gerakan fisik ringan untuk memutus siklus 
            pikiran dan memberi sinyal pada tubuh bahwa sudah waktunya berhenti.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Pilihan ritual
    st.markdown("""
    <div class="card fade-in">
        <div style="font-size:0.8rem; color:var(--amber); letter-spacing:0.12em; text-transform:uppercase; margin-bottom:0.8rem;">
            Pilih satu ritual (lakukan selama timer berjalan)
        </div>
        
        <div class="ritual-step">
            <span class="ritual-icon">🫁</span>
            <div class="ritual-text">
                <strong style="color:var(--text-primary);">Pernapasan Kotak (Box Breathing)</strong><br>
                Tarik napas 4 hitungan → tahan 4 hitungan → buang 4 hitungan → tahan 4 hitungan. 
                Ulangi terus.
            </div>
        </div>
        
        <div class="ritual-step">
            <span class="ritual-icon">🧘</span>
            <div class="ritual-text">
                <strong style="color:var(--text-primary);">Peregangan Leher & Bahu</strong><br>
                Miringkan kepala ke kanan, tahan 8 detik. Ke kiri, tahan 8 detik. 
                Putar bahu ke belakang perlahan. Ulangi.
            </div>
        </div>
        
        <div class="ritual-step">
            <span class="ritual-icon">🤲</span>
            <div class="ritual-text">
                <strong style="color:var(--text-primary);">Progressive Muscle Relaxation</strong><br>
                Kencangkan seluruh otot tubuh selama 5 detik, lalu lepaskan. 
                Rasakan perbedaan antara tegang dan rileks.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Timer Section
    if not st.session_state.ritual_started:
        if st.button("▶ Mulai Timer 60 Detik", key="start_timer"):
            st.session_state.ritual_started = True
            st.rerun()
    else:
        # Render timer countdown
        st.markdown('<div class="card card-amber-glow fade-in">', unsafe_allow_html=True)

        timer_placeholder = st.empty()
        breathing_placeholder = st.empty()

        # Breathing cues yang berganti setiap beberapa detik
        breathing_phases = [
            ("🫁", "Tarik napas..."),
            ("⏸", "Tahan..."),
            ("💨", "Buang napas..."),
            ("⏸", "Tahan..."),
        ]

        for i in range(60, -1, -1):
            # Tentukan fase pernapasan (siklus 16 detik: 4+4+4+4)
            phase_idx = ((60 - i) // 4) % 4
            phase_icon, phase_text = breathing_phases[phase_idx]

            # Render lingkaran timer
            timer_placeholder.markdown(f"""
            <div class="timer-container">
                <div class="timer-ring">
                    <div class="timer-seconds">{i}</div>
                    <div class="timer-label">detik</div>
                </div>
                <div class="breathing-guide">{phase_icon} {phase_text}</div>
            </div>
            """, unsafe_allow_html=True)

            time.sleep(1)

        st.markdown('</div>', unsafe_allow_html=True)

        # Timer selesai
        st.session_state.timer_done = True
        st.rerun()


# ─────────────────────────────────────────────
# COMPLETION SCREEN (setelah Step 3)
# ─────────────────────────────────────────────
def render_completion():
    """Layar penutup setelah semua ritual selesai."""

    st.markdown("""
    <div class="completion-screen fade-in">
        <span class="completion-icon">🌙</span>
        <div class="completion-title">Ritual Selesai</div>
        <div class="completion-msg">
            Otak siap <em>shutdown</em>.<br><br>
            Kamu telah menutup hari ini dengan benar — 
            pikiran tersimpan, tubuh rileks, lingkungan mendukung.<br><br>
            <strong style="color:var(--amber);">Silakan letakkan perangkat ini.</strong><br>
            Besok pagi menantimu dengan energi yang baru.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="text-align:center; padding:1.2rem;">
        <div style="font-size:0.75rem; color:var(--text-dim); line-height:1.6;">
            "Rest is not idle; it is the work that makes all other work possible."<br>
            <span style="color:var(--text-dim); font-size:0.7rem;">— Alex Soojung-Kim Pang</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Reset button (untuk uji coba / esok hari)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("↩ Mulai Dari Awal", key="restart"):
            # Reset semua state
            for key in ['step', 'vault_submitted', 'vault_thought',
                        'timer_started', 'timer_done', 'ritual_started']:
                if key in st.session_state:
                    del st.session_state[key]
            init_state()
            st.rerun()


# ─────────────────────────────────────────────
# MAIN ROUTER — Linear Navigation
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
        # Fallback ke step 0 jika state tidak valid
        st.session_state.step = 0
        st.rerun()


if __name__ == "__main__" or True:
    main()