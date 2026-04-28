import streamlit as st
import random

st.set_page_config(
    page_title="Rock Paper Scissors",
    page_icon="🪨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Mono:wght@400;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #080c14 !important;
}
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #080c14 0%, #0d1526 50%, #080c14 100%) !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="block-container"] { padding-top: 2rem !important; }

* { font-family: 'Space Mono', monospace; color: #e2eeff; }

/* ── Title ── */
.title-wrap { text-align: center; margin-bottom: 0.4rem; }
.game-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3rem, 8vw, 5.5rem);
    letter-spacing: 0.14em;
    background: linear-gradient(90deg, #00f5d4 0%, #00c8ff 40%, #ff2d78 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin: 0;
    background-size: 200% 200%;
    animation: shimmer 5s ease-in-out infinite alternate;
}
@keyframes shimmer {
    0%   { background-position: 0% 50%; }
    100% { background-position: 100% 50%; }
}
.subtitle {
    font-size: 0.65rem;
    letter-spacing: 0.45em;
    color: #00c8ff;
    text-transform: uppercase;
    margin-top: 0.3rem;
}

/* ── Scoreboard ── */
.scoreboard {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin: 1.4rem 0;
}
.score-cell {
    background: rgba(0, 200, 255, 0.06);
    border: 1px solid rgba(0, 200, 255, 0.2);
    border-radius: 14px;
    padding: 0.8rem 1.8rem;
    text-align: center;
    min-width: 84px;
    transition: transform 0.2s, border-color 0.2s;
}
.score-cell:hover {
    transform: translateY(-3px);
    border-color: rgba(0, 200, 255, 0.5);
}
.score-label {
    font-size: 0.55rem;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: #5b8db8;
    margin-bottom: 0.25rem;
}
.score-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.6rem;
    line-height: 1;
}
.score-num.wins   { color: #00f5d4; }
.score-num.losses { color: #ff2d78; }
.score-num.ties   { color: #f5c842; }

/* ── Move label ── */
.move-label {
    text-align: center;
    font-size: 0.6rem;
    letter-spacing: 0.4em;
    color: #5b8db8;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

/* ── Arena ── */
.arena {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2rem;
    margin: 1.4rem 0;
    padding: 1.6rem;
    background: rgba(0, 200, 255, 0.04);
    border: 1px solid rgba(0, 200, 255, 0.15);
    border-radius: 20px;
}
.arena-side { text-align: center; flex: 1; }
.arena-label {
    font-size: 0.55rem;
    letter-spacing: 0.4em;
    color: #00c8ff;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.arena-emoji {
    font-size: 4rem;
    display: block;
    line-height: 1.2;
    animation: popIn 0.45s cubic-bezier(.34,1.56,.64,1) both;
}
@keyframes popIn {
    0%   { transform: scale(0) rotate(-20deg); opacity: 0; }
    100% { transform: scale(1) rotate(0deg);   opacity: 1; }
}
.arena-name {
    font-size: 0.7rem;
    color: #a0c4e8;
    margin-top: 0.35rem;
    letter-spacing: 0.12em;
}
.vs-badge {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.2rem;
    color: #ff2d78;
    letter-spacing: 0.08em;
    text-shadow: 0 0 20px rgba(255, 45, 120, 0.5);
}

/* ── Result banner ── */
.result-banner {
    text-align: center;
    padding: 0.9rem 2rem;
    border-radius: 14px;
    margin: 0.8rem 0;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.7rem;
    letter-spacing: 0.15em;
}
.result-win {
    background: rgba(0, 245, 212, 0.1);
    border: 1px solid rgba(0, 245, 212, 0.4);
    color: #00f5d4;
    animation: winPop 0.55s cubic-bezier(.34,1.56,.64,1) both;
}
.result-loss {
    background: rgba(255, 45, 120, 0.1);
    border: 1px solid rgba(255, 45, 120, 0.4);
    color: #ff2d78;
    animation: lossShake 0.55s ease both;
}
.result-tie {
    background: rgba(245, 200, 66, 0.08);
    border: 1px solid rgba(245, 200, 66, 0.3);
    color: #f5c842;
    animation: slideUp 0.45s cubic-bezier(.34,1.56,.64,1) both;
}

@keyframes winPop {
    0%   { transform: scale(0.6); opacity: 0; }
    65%  { transform: scale(1.07); }
    100% { transform: scale(1); opacity: 1; }
}
@keyframes lossShake {
    0%   { transform: translateX(0); opacity: 0; }
    10%  { opacity: 1; }
    20%  { transform: translateX(-12px); }
    40%  { transform: translateX(12px); }
    55%  { transform: translateX(-7px); }
    70%  { transform: translateX(7px); }
    85%  { transform: translateX(-3px); }
    100% { transform: translateX(0); }
}
@keyframes slideUp {
    0%   { transform: translateY(18px); opacity: 0; }
    100% { transform: translateY(0);    opacity: 1; }
}

/* ── History ── */
.history-wrap {
    margin-top: 1.5rem;
    border-top: 1px solid rgba(0, 200, 255, 0.12);
    padding-top: 1rem;
}
.history-title {
    font-size: 0.55rem;
    letter-spacing: 0.45em;
    color: #5b8db8;
    text-transform: uppercase;
    margin-bottom: 0.7rem;
    text-align: center;
}
.history-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.35rem 0.9rem;
    border-radius: 8px;
    font-size: 0.7rem;
    gap: 0.5rem;
    color: #a0c4e8;
    transition: background 0.15s;
}
.history-row:hover { background: rgba(0, 200, 255, 0.05); }
.h-win  { border-left: 3px solid #00f5d4; }
.h-loss { border-left: 3px solid #ff2d78; }
.h-tie  { border-left: 3px solid #f5c842; }
.h-badge {
    font-size: 0.55rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    padding: 2px 9px;
    border-radius: 5px;
}
.h-badge.win  { background: rgba(0, 245, 212, 0.15); color: #00f5d4; }
.h-badge.loss { background: rgba(255, 45, 120, 0.15); color: #ff2d78; }
.h-badge.tie  { background: rgba(245, 200, 66, 0.12); color: #f5c842; }

/* ── Streamlit buttons ── */
.stButton > button {
    background: rgba(0, 200, 255, 0.08) !important;
    border: 1px solid rgba(0, 200, 255, 0.35) !important;
    color: #00c8ff !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.18em !important;
    border-radius: 10px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: rgba(0, 200, 255, 0.18) !important;
    border-color: #00c8ff !important;
    color: #ffffff !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(0, 200, 255, 0.2) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Confetti canvas ── */
#confetti-canvas {
    position: fixed; top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none; z-index: 9999;
}

/* ── Grid lines background (decorative) ── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(0,200,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,200,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}
</style>

<canvas id="confetti-canvas"></canvas>
<script>
function launchConfetti() {
    const canvas = document.getElementById('confetti-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const colors = ['#00f5d4','#00c8ff','#ff2d78','#f5c842','#a855f7','#ffffff'];
    const pieces = Array.from({length: 140}, () => ({
        x: Math.random() * canvas.width,
        y: -20 - Math.random() * 180,
        w: 7 + Math.random() * 7,
        h: 3 + Math.random() * 5,
        color: colors[Math.floor(Math.random() * colors.length)],
        rot: Math.random() * Math.PI * 2,
        rotSpeed: (Math.random() - 0.5) * 0.18,
        dx: (Math.random() - 0.5) * 2.5,
        dy: 3.5 + Math.random() * 4,
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
            if (frame > 55) p.alpha -= 0.014;
        });
        frame++;
        if (pieces.some(p => p.alpha > 0)) requestAnimationFrame(draw);
        else ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
    draw();
}
function checkResult() {
    if (document.querySelector('.result-win')) launchConfetti();
}
setTimeout(checkResult, 300);
setTimeout(checkResult, 750);
</script>
""", unsafe_allow_html=True)

for key, default in [('wins',0),('losses',0),('ties',0),('history',[]),('last_result',None)]:
    if key not in st.session_state:
        st.session_state[key] = default

LABELS = {'R': 'Rock', 'P': 'Paper', 'S': 'Scissors'}
EMOJIS = {'R': '🪨',   'P': '📄',   'S': '✂️'}
BEATS  = {'R': 'S', 'S': 'P', 'P': 'R'}

def play(user_choice: str):
    computer_choice = random.choice(['R', 'P', 'S'])
    if computer_choice == user_choice:
        result, msg = 'tie', "IT'S A TIE"
        st.session_state.ties += 1
    elif BEATS[user_choice] == computer_choice:
        result = 'win'
        msg = f"{LABELS[user_choice]} BEATS {LABELS[computer_choice]} — YOU WIN 🎉"
        st.session_state.wins += 1
    else:
        result = 'loss'
        msg = f"{LABELS[computer_choice]} BEATS {LABELS[user_choice]} — CPU WINS 💀"
        st.session_state.losses += 1
    st.session_state.last_result = {'user': user_choice, 'cpu': computer_choice, 'result': result, 'msg': msg}
    st.session_state.history.insert(0, st.session_state.last_result)
    if len(st.session_state.history) > 10:
        st.session_state.history = st.session_state.history[:10]

# ── Title ──
st.markdown("""
<div class="title-wrap">
  <p class="game-title">ROCK PAPER SCISSORS</p>
  <p class="subtitle">Challenge the machine</p>
</div>
""", unsafe_allow_html=True)

# ── Scoreboard ──
w, l, t = st.session_state.wins, st.session_state.losses, st.session_state.ties
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

# ── Move buttons ──
st.markdown('<div class="move-label">Make your move</div>', unsafe_allow_html=True)
col1, col2, col3, _ = st.columns([1, 1, 1, 0.01])
with col1:
    if st.button("🪨  Rock", key="btn_rock", use_container_width=True):
        play('R'); st.rerun()
with col2:
    if st.button("📄  Paper", key="btn_paper", use_container_width=True):
        play('P'); st.rerun()
with col3:
    if st.button("✂️  Scissors", key="btn_scissors", use_container_width=True):
        play('S'); st.rerun()

# ── Arena + Result ──
lr = st.session_state.last_result
if lr:
    st.markdown(f"""
<div class="arena">
  <div class="arena-side">
    <div class="arena-label">You</div>
    <span class="arena-emoji">{EMOJIS[lr['user']]}</span>
    <div class="arena-name">{LABELS[lr['user']]}</div>
  </div>
  <div class="vs-badge">VS</div>
  <div class="arena-side">
    <div class="arena-label">CPU</div>
    <span class="arena-emoji">{EMOJIS[lr['cpu']]}</span>
    <div class="arena-name">{LABELS[lr['cpu']]}</div>
  </div>
</div>
<div class="result-banner result-{lr['result']}">{lr['msg']}</div>
""", unsafe_allow_html=True)

# ── Reset ──
_, mid, _ = st.columns([2, 1, 2])
with mid:
    if st.button("↺  Reset Score", key="btn_reset", use_container_width=True):
        for k in ['wins','losses','ties','history','last_result']:
            st.session_state[k] = 0 if k in ('wins','losses','ties') else ([] if k == 'history' else None)
        st.rerun()

# ── History ──
if st.session_state.history:
    rows_html = "".join(f"""
<div class="history-row h-{h['result']}">
  <span>{EMOJIS[h['user']]} {LABELS[h['user']]}</span>
  <span class="h-badge {h['result']}">{h['result'].upper()}</span>
  <span>{EMOJIS[h['cpu']]} {LABELS[h['cpu']]}</span>
</div>""" for h in st.session_state.history)
    st.markdown(f"""
<div class="history-wrap">
  <div class="history-title">Last 10 rounds</div>
  {rows_html}
</div>
""", unsafe_allow_html=True)
