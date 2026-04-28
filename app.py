import streamlit as st
import random

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Rock Paper Scissors",
    page_icon="🪨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Inject CSS + JS animations ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Mono:wght@400;700&display=swap');

/* ── Reset & base ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #fff8f0 !important;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 30% 10%, #ffe0b2 0%, #fff8f0 60%) !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="block-container"] { padding-top: 2rem !important; }

/* ── Typography ── */
* { font-family: 'Space Mono', monospace; color: #1a1a2e; }

.title-wrap {
    text-align: center;
    margin-bottom: 0.5rem;
}
.game-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3rem, 8vw, 5.5rem);
    letter-spacing: 0.12em;
    background: linear-gradient(135deg, #ff6b35 0%, #f7c948 50%, #00b4d8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin: 0;
    animation: shimmer 4s ease-in-out infinite alternate;
    background-size: 200% 200%;
}
@keyframes shimmer {
    0%   { background-position: 0% 50%; }
    100% { background-position: 100% 50%; }
}
.subtitle {
    font-size: 0.7rem;
    letter-spacing: 0.4em;
    color: #ff6b35;
    text-transform: uppercase;
    margin-top: 0.2rem;
    font-weight: 700;
}

/* ── Score board ── */
.scoreboard {
    display: flex;
    justify-content: center;
    gap: 1.2rem;
    margin: 1.2rem 0;
}
.score-cell {
    background: #ffffff;
    border: 2px solid #ffe0b2;
    border-radius: 12px;
    padding: 0.7rem 1.6rem;
    text-align: center;
    box-shadow: 0 4px 16px rgba(255,107,53,0.1);
    transition: transform 0.2s;
    min-width: 80px;
}
.score-cell:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(255,107,53,0.18); }
.score-label {
    font-size: 0.6rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #ff6b35;
    margin-bottom: 0.2rem;
    font-weight: 700;
}
.score-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.4rem;
    line-height: 1;
}
.score-num.wins   { color: #06a77d; }
.score-num.losses { color: #e63946; }
.score-num.ties   { color: #f7c948; }

/* ── Battle arena ── */
.arena {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2rem;
    margin: 1.5rem 0;
    padding: 1.5rem;
    background: #ffffff;
    border: 2px solid #ffe0b2;
    border-radius: 24px;
    box-shadow: 0 6px 24px rgba(255,107,53,0.1);
}
.arena-side { text-align: center; flex: 1; }
.arena-label {
    font-size: 0.6rem;
    letter-spacing: 0.4em;
    color: #ff6b35;
    margin-bottom: 0.5rem;
    text-transform: uppercase;
    font-weight: 700;
}
.arena-emoji {
    font-size: 4rem;
    display: block;
    line-height: 1.2;
    animation: popIn 0.5s cubic-bezier(.34,1.56,.64,1) both;
}
@keyframes popIn {
    0%   { transform: scale(0) rotate(-15deg); opacity: 0; }
    100% { transform: scale(1) rotate(0deg);   opacity: 1; }
}
.arena-name {
    font-size: 0.75rem;
    color: #444;
    margin-top: 0.3rem;
    letter-spacing: 0.1em;
    font-weight: 700;
}
.vs-badge {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem;
    color: #ff6b35;
    letter-spacing: 0.1em;
}

/* ── Result banner ── */
.result-banner {
    text-align: center;
    padding: 1rem 2rem;
    border-radius: 16px;
    margin: 1rem 0;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    letter-spacing: 0.15em;
}
.result-win {
    background: #d8f3eb;
    border: 2px solid #06a77d;
    color: #065f46;
    animation: winPop 0.6s cubic-bezier(.34,1.56,.64,1) both;
}
.result-loss {
    background: #fde8ea;
    border: 2px solid #e63946;
    color: #9b1c27;
    animation: lossShake 0.6s ease both;
}
.result-tie {
    background: #fef9c3;
    border: 2px solid #f7c948;
    color: #7a5a00;
    animation: slideUp 0.5s cubic-bezier(.34,1.56,.64,1) both;
}

@keyframes winPop {
    0%   { transform: scale(0.5); opacity: 0; }
    60%  { transform: scale(1.08); }
    100% { transform: scale(1); opacity: 1; }
}
@keyframes lossShake {
    0%   { transform: translateX(0); opacity: 0; }
    15%  { transform: translateX(-10px); opacity: 1; }
    30%  { transform: translateX(10px); }
    45%  { transform: translateX(-8px); }
    60%  { transform: translateX(8px); }
    75%  { transform: translateX(-4px); }
    100% { transform: translateX(0); }
}
@keyframes slideUp {
    0%   { transform: translateY(20px); opacity: 0; }
    100% { transform: translateY(0);    opacity: 1; }
}

/* ── History table ── */
.history-wrap {
    margin-top: 1.5rem;
    border-top: 2px solid #ffe0b2;
    padding-top: 1rem;
}
.history-title {
    font-size: 0.6rem;
    letter-spacing: 0.4em;
    color: #ff6b35;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
    text-align: center;
    font-weight: 700;
}
.history-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.4rem 0.8rem;
    border-radius: 8px;
    font-size: 0.75rem;
    transition: background 0.2s;
    gap: 0.5rem;
    color: #1a1a2e;
}
.history-row:hover { background: #fff0e6; }
.h-win  { border-left: 3px solid #06a77d; }
.h-loss { border-left: 3px solid #e63946; }
.h-tie  { border-left: 3px solid #f7c948; }
.h-badge {
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    padding: 2px 8px;
    border-radius: 6px;
}
.h-badge.win  { background: #d8f3eb; color: #065f46; }
.h-badge.loss { background: #fde8ea; color: #9b1c27; }
.h-badge.tie  { background: #fef9c3; color: #7a5a00; }

/* ── Streamlit button override ── */
.stButton > button {
    background: #ff6b35 !important;
    border: 2px solid #ff6b35 !important;
    color: #ffffff !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.15em !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #e85520 !important;
    border-color: #e85520 !important;
    color: #ffffff !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(255,107,53,0.35) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Confetti canvas ── */
#confetti-canvas {
    position: fixed; top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 9999;
}
</style>

<canvas id="confetti-canvas"></canvas>
<script>
// ── Confetti on WIN ────────────────────────────────────────────────────────────
function launchConfetti() {
    const canvas = document.getElementById('confetti-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const colors = ['#ff6b35','#f7c948','#00b4d8','#06a77d','#e63946','#ff9f1c'];
    const pieces = Array.from({length: 120}, () => ({
        x: Math.random() * canvas.width,
        y: -10 - Math.random() * 200,
        w: 8 + Math.random() * 8,
        h: 4 + Math.random() * 4,
        color: colors[Math.floor(Math.random() * colors.length)],
        rot: Math.random() * Math.PI * 2,
        rotSpeed: (Math.random() - 0.5) * 0.15,
        dx: (Math.random() - 0.5) * 3,
        dy: 3 + Math.random() * 4,
        alpha: 1
    }));

    let frame = 0;
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        pieces.forEach(p => {
            ctx.save();
            ctx.globalAlpha = p.alpha;
            ctx.translate(p.x, p.y);
            ctx.rotate(p.rot);
            ctx.fillStyle = p.color;
            ctx.fillRect(-p.w/2, -p.h/2, p.w, p.h);
            ctx.restore();
            p.x += p.dx; p.y += p.dy; p.rot += p.rotSpeed;
            if (frame > 60) p.alpha -= 0.012;
        });
        frame++;
        if (pieces.some(p => p.alpha > 0)) requestAnimationFrame(draw);
        else ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
    draw();
}

// ── Trigger based on result banner class ──────────────────────────────────────
function checkResult() {
    const banner = document.querySelector('.result-win');
    if (banner) launchConfetti();
}
// Poll after Streamlit re-renders
setTimeout(checkResult, 300);
setTimeout(checkResult, 700);
</script>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
for key, default in [('wins',0),('losses',0),('ties',0),('history',[]),('last_result',None)]:
    if key not in st.session_state:
        st.session_state[key] = default

LABELS = {'R': 'Rock', 'P': 'Paper', 'S': 'Scissors'}
EMOJIS = {'R': '🪨',   'P': '📄',   'S': '✂️'}
BEATS  = {'R': 'S', 'S': 'P', 'P': 'R'}

def play(user_choice: str):
    computer_choice = random.choice(['R', 'P', 'S'])
    if computer_choice == user_choice:
        result, msg = 'tie', "It's a tie!"
        st.session_state.ties += 1
    elif BEATS[user_choice] == computer_choice:
        result = 'win'
        msg = f"{LABELS[user_choice]} beats {LABELS[computer_choice]} — you win! 🎉"
        st.session_state.wins += 1
    else:
        result = 'loss'
        msg = f"{LABELS[computer_choice]} beats {LABELS[user_choice]} — computer wins! 💀"
        st.session_state.losses += 1

    st.session_state.last_result = {
        'user': user_choice, 'cpu': computer_choice,
        'result': result, 'msg': msg
    }
    st.session_state.history.insert(0, st.session_state.last_result)
    if len(st.session_state.history) > 10:
        st.session_state.history = st.session_state.history[:10]

# ── UI ─────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="title-wrap">
  <p class="game-title">ROCK PAPER SCISSORS</p>
  <p class="subtitle">Challenge the machine</p>
</div>
""", unsafe_allow_html=True)

# Score board
w = st.session_state.wins
l = st.session_state.losses
t = st.session_state.ties
st.markdown(f"""
<div class="scoreboard">
  <div class="score-cell">
    <div class="score-label">Wins</div>
    <div class="score-num wins">{w}</div>
  </div>
  <div class="score-cell">
    <div class="score-label">Losses</div>
    <div class="score-num losses">{l}</div>
  </div>
  <div class="score-cell">
    <div class="score-label">Ties</div>
    <div class="score-num ties">{t}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Choice buttons
st.markdown('<div style="text-align:center;font-size:0.65rem;letter-spacing:0.3em;color:#ff6b35;text-transform:uppercase;margin-bottom:0.5rem;font-weight:700;">Make your move</div>', unsafe_allow_html=True)

col1, col2, col3, col_gap = st.columns([1, 1, 1, 0.01])
with col1:
    if st.button("🪨\nRock", key="btn_rock", use_container_width=True):
        play('R'); st.rerun()
with col2:
    if st.button("📄\nPaper", key="btn_paper", use_container_width=True):
        play('P'); st.rerun()
with col3:
    if st.button("✂️\nScissors", key="btn_scissors", use_container_width=True):
        play('S'); st.rerun()

# Battle arena + result
lr = st.session_state.last_result
if lr:
    user_e = EMOJIS[lr['user']]
    cpu_e  = EMOJIS[lr['cpu']]
    user_l = LABELS[lr['user']]
    cpu_l  = LABELS[lr['cpu']]
    res    = lr['result']
    msg    = lr['msg']

    st.markdown(f"""
<div class="arena">
  <div class="arena-side">
    <div class="arena-label">You</div>
    <span class="arena-emoji">{user_e}</span>
    <div class="arena-name">{user_l}</div>
  </div>
  <div class="vs-badge">VS</div>
  <div class="arena-side">
    <div class="arena-label">CPU</div>
    <span class="arena-emoji">{cpu_e}</span>
    <div class="arena-name">{cpu_l}</div>
  </div>
</div>
<div class="result-banner result-{res}">{msg}</div>
""", unsafe_allow_html=True)

# Reset button
_, mid, _ = st.columns([2, 1, 2])
with mid:
    if st.button("↺  Reset Score", key="btn_reset", use_container_width=True):
        for k in ['wins','losses','ties','history','last_result']:
            st.session_state[k] = 0 if k in ('wins','losses','ties') else ([] if k=='history' else None)
        st.rerun()

# History
if st.session_state.history:
    rows_html = ""
    for h in st.session_state.history:
        badge_cls = h['result']
        badge_txt = h['result'].upper()
        row_cls   = f"h-{h['result']}"
        rows_html += f"""
<div class="history-row {row_cls}">
  <span>{EMOJIS[h['user']]} {LABELS[h['user']]}</span>
  <span class="h-badge {badge_cls}">{badge_txt}</span>
  <span>{EMOJIS[h['cpu']]} {LABELS[h['cpu']]}</span>
</div>"""

    st.markdown(f"""
<div class="history-wrap">
  <div class="history-title">Last 10 rounds</div>
  {rows_html}
</div>
""", unsafe_allow_html=True)
