import streamlit as st
import random

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RPS · BATTLE",
    page_icon="⚔️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=DM+Mono:wght@400;500&display=swap');

:root {
    --bg:       #06060a;
    --panel:    #0e0e16;
    --border:   #1e1e30;
    --accent:   #f0f;
    --accent2:  #0ff;
    --win:      #39ff14;
    --loss:     #ff2d55;
    --tie:      #ffd60a;
    --txt:      #e8e8ff;
    --muted:    #5555aa;
}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: var(--bg) !important;
    font-family: 'DM Mono', monospace;
    color: var(--txt);
}
[data-testid="stHeader"]          { background: transparent !important; }
[data-testid="block-container"]   { padding-top: 2rem !important; max-width: 680px !important; }

/* ── Scanline overlay ── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed; inset: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 3px,
        rgba(0,0,0,0.18) 3px,
        rgba(0,0,0,0.18) 4px
    );
    pointer-events: none;
    z-index: 9999;
}

/* ── HEADER ── */
.header {
    text-align: center;
    margin-bottom: 2rem;
    position: relative;
}
.header-eyebrow {
    font-size: 0.65rem;
    letter-spacing: 0.55em;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.header-title {
    font-family: 'Black Han Sans', sans-serif;
    font-size: clamp(3.2rem, 10vw, 5.8rem);
    line-height: 0.9;
    letter-spacing: -0.01em;
    margin: 0;
    position: relative;
    display: inline-block;
}
.header-title .t1 { color: var(--txt); }
.header-title .t2 {
    color: transparent;
    -webkit-text-stroke: 2px var(--accent);
    text-shadow: 0 0 30px var(--accent);
}
.header-title .t3 { color: var(--accent2); text-shadow: 0 0 20px var(--accent2); }
.header-sub {
    font-size: 0.65rem;
    letter-spacing: 0.5em;
    color: var(--muted);
    text-transform: uppercase;
    margin-top: 0.6rem;
}

/* ── SCORE ── */
.scoreboard {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 0.6rem;
    margin: 0 0 2rem;
}
.score-cell {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 0.9rem 0.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.score-cell::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}
.score-cell.wins::after   { background: var(--win); box-shadow: 0 0 12px var(--win); }
.score-cell.losses::after { background: var(--loss); box-shadow: 0 0 12px var(--loss); }
.score-cell.ties::after   { background: var(--tie); box-shadow: 0 0 12px var(--tie); }

.score-label {
    font-size: 0.55rem;
    letter-spacing: 0.4em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.3rem;
}
.score-num {
    font-family: 'Black Han Sans', sans-serif;
    font-size: 2.6rem;
    line-height: 1;
}
.score-num.wins   { color: var(--win);  text-shadow: 0 0 20px var(--win); }
.score-num.losses { color: var(--loss); text-shadow: 0 0 20px var(--loss); }
.score-num.ties   { color: var(--tie);  text-shadow: 0 0 20px var(--tie); }

/* ── MOVE LABEL ── */
.move-prompt {
    font-size: 0.6rem;
    letter-spacing: 0.5em;
    color: var(--muted);
    text-transform: uppercase;
    text-align: center;
    margin-bottom: 0.8rem;
}

/* ── Streamlit button override ── */
.stButton > button {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    color: var(--txt) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 2rem !important;
    border-radius: 6px !important;
    padding: 1.4rem 0.5rem !important;
    width: 100% !important;
    transition: all 0.18s ease !important;
    position: relative !important;
    overflow: hidden !important;
    letter-spacing: 0 !important;
    line-height: 1 !important;
}
.stButton > button:hover {
    border-color: var(--accent) !important;
    box-shadow: 0 0 24px rgba(255,0,255,0.3), inset 0 0 24px rgba(255,0,255,0.06) !important;
    transform: translateY(-3px) scale(1.04) !important;
    color: #fff !important;
}
.stButton > button:active {
    transform: translateY(0) scale(0.97) !important;
}

/* Rock/Paper/Scissors specific glow colors */
div[data-testid="column"]:nth-child(1) .stButton > button:hover {
    border-color: #ff7b00 !important;
    box-shadow: 0 0 24px rgba(255,123,0,0.4), inset 0 0 24px rgba(255,123,0,0.08) !important;
}
div[data-testid="column"]:nth-child(2) .stButton > button:hover {
    border-color: var(--accent2) !important;
    box-shadow: 0 0 24px rgba(0,255,255,0.4), inset 0 0 24px rgba(0,255,255,0.08) !important;
}
div[data-testid="column"]:nth-child(3) .stButton > button:hover {
    border-color: var(--accent) !important;
    box-shadow: 0 0 24px rgba(255,0,255,0.4), inset 0 0 24px rgba(255,0,255,0.08) !important;
}

/* btn sub-labels */
.btn-inner { text-align: center; pointer-events: none; }
.btn-emoji { font-size: 2.2rem; display: block; }
.btn-name  { font-size: 0.55rem; letter-spacing: 0.35em; color: var(--muted); text-transform: uppercase; margin-top: 0.3rem; display: block; }

/* ── ARENA ── */
.arena {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    gap: 1rem;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1.8rem 1.5rem;
    margin: 1.5rem 0;
    position: relative;
    overflow: hidden;
}
.arena::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at center, rgba(255,0,255,0.04) 0%, transparent 70%);
    pointer-events: none;
}
.arena-side { text-align: center; }
.arena-tag {
    font-size: 0.55rem;
    letter-spacing: 0.45em;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 0.7rem;
}
.arena-emoji {
    font-size: 4.5rem;
    display: block;
    line-height: 1;
    animation: popIn 0.4s cubic-bezier(.34,1.56,.64,1) both;
}
@keyframes popIn {
    from { transform: scale(0.3) rotate(-20deg); opacity: 0; }
    to   { transform: scale(1)   rotate(0deg);   opacity: 1; }
}
.arena-name {
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    color: var(--txt);
    margin-top: 0.5rem;
    text-transform: uppercase;
}
.vs {
    font-family: 'Black Han Sans', sans-serif;
    font-size: 1.8rem;
    color: var(--border);
    letter-spacing: 0.05em;
}

/* ── RESULT BANNER ── */
.result-banner {
    text-align: center;
    padding: 0.9rem 1.5rem;
    border-radius: 4px;
    margin: 0.6rem 0 1.2rem;
    font-family: 'Black Han Sans', sans-serif;
    font-size: 1.4rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    animation: slideUp 0.4s cubic-bezier(.34,1.56,.64,1) both;
}
@keyframes slideUp {
    from { transform: translateY(14px); opacity: 0; }
    to   { transform: translateY(0);    opacity: 1; }
}
.result-win {
    background: rgba(57,255,20,0.07);
    border: 1px solid rgba(57,255,20,0.35);
    color: var(--win);
    text-shadow: 0 0 20px var(--win);
}
.result-loss {
    background: rgba(255,45,85,0.07);
    border: 1px solid rgba(255,45,85,0.35);
    color: var(--loss);
    text-shadow: 0 0 20px var(--loss);
}
.result-tie {
    background: rgba(255,214,10,0.07);
    border: 1px solid rgba(255,214,10,0.35);
    color: var(--tie);
    text-shadow: 0 0 20px var(--tie);
}

/* ── HISTORY ── */
.history-wrap {
    margin-top: 1.8rem;
    border-top: 1px solid var(--border);
    padding-top: 1.2rem;
}
.history-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.7rem;
}
.history-title {
    font-size: 0.55rem;
    letter-spacing: 0.45em;
    color: var(--muted);
    text-transform: uppercase;
}
.history-row {
    display: grid;
    grid-template-columns: 1fr 56px 1fr;
    align-items: center;
    padding: 0.45rem 0.7rem;
    border-radius: 4px;
    font-size: 0.7rem;
    transition: background 0.15s;
    border-left: 2px solid transparent;
    margin-bottom: 2px;
}
.history-row:hover { background: rgba(255,255,255,0.03); }
.h-win  { border-left-color: var(--win); }
.h-loss { border-left-color: var(--loss); }
.h-tie  { border-left-color: var(--tie); }
.h-you  { color: var(--txt); }
.h-cpu  { color: var(--txt); text-align: right; }
.h-badge {
    text-align: center;
    font-size: 0.5rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    padding: 3px 6px;
    border-radius: 3px;
    text-transform: uppercase;
}
.h-badge.win  { background: rgba(57,255,20,0.12);  color: var(--win); }
.h-badge.loss { background: rgba(255,45,85,0.12);  color: var(--loss); }
.h-badge.tie  { background: rgba(255,214,10,0.12); color: var(--tie); }

/* ── WIN RATE BAR ── */
.winbar-wrap { margin-top: 1.4rem; }
.winbar-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.55rem;
    letter-spacing: 0.3em;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 0.35rem;
}
.winbar-track {
    height: 5px;
    background: var(--border);
    border-radius: 999px;
    overflow: hidden;
}
.winbar-fill {
    height: 100%;
    background: var(--win);
    box-shadow: 0 0 10px var(--win);
    border-radius: 999px;
    transition: width 0.5s ease;
}

/* reset button area */
.reset-wrap { text-align: center; margin: 0.4rem 0 0.2rem; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
for key, default in [('wins', 0), ('losses', 0), ('ties', 0), ('history', []), ('last_result', None)]:
    if key not in st.session_state:
        st.session_state[key] = default

LABELS = {'R': 'Rock', 'P': 'Paper', 'S': 'Scissors'}
EMOJIS = {'R': '🪨', 'P': '📄', 'S': '✂️'}
BEATS  = {'R': 'S', 'S': 'P', 'P': 'R'}

def play(user_choice: str):
    cpu = random.choice(['R', 'P', 'S'])
    if cpu == user_choice:
        result = 'tie'; msg = "DRAW"
        st.session_state.ties += 1
    elif BEATS[user_choice] == cpu:
        result = 'win'; msg = "YOU WIN"
        st.session_state.wins += 1
    else:
        result = 'loss'; msg = "YOU LOSE"
        st.session_state.losses += 1

    st.session_state.last_result = {
        'user': user_choice, 'cpu': cpu, 'result': result, 'msg': msg
    }
    st.session_state.history.insert(0, st.session_state.last_result)
    if len(st.session_state.history) > 10:
        st.session_state.history = st.session_state.history[:10]

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header">
  <div class="header-eyebrow">⚔️ &nbsp; arcade edition &nbsp; ⚔️</div>
  <div class="header-title">
    <span class="t1">RO</span><span class="t2">CK</span><br>
    <span class="t3">PA</span><span class="t1">PER</span><br>
    <span class="t2">SC</span><span class="t3">ISSORS</span>
  </div>
  <div class="header-sub">man vs machine</div>
</div>
""", unsafe_allow_html=True)

# ── SCOREBOARD ────────────────────────────────────────────────────────────────
w = st.session_state.wins
l = st.session_state.losses
t = st.session_state.ties
total = w + l + t
win_pct = round((w / total) * 100) if total > 0 else 0

st.markdown(f"""
<div class="scoreboard">
  <div class="score-cell wins">
    <div class="score-label">Wins</div>
    <div class="score-num wins">{w}</div>
  </div>
  <div class="score-cell losses">
    <div class="score-label">Losses</div>
    <div class="score-num losses">{l}</div>
  </div>
  <div class="score-cell ties">
    <div class="score-label">Ties</div>
    <div class="score-num ties">{t}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Win rate bar
if total > 0:
    st.markdown(f"""
<div class="winbar-wrap">
  <div class="winbar-label">
    <span>Win rate</span>
    <span>{win_pct}%</span>
  </div>
  <div class="winbar-track">
    <div class="winbar-fill" style="width:{win_pct}%"></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── CHOICE BUTTONS ────────────────────────────────────────────────────────────
st.markdown('<div class="move-prompt">— choose your weapon —</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3, gap="small")
with c1:
    if st.button("🪨\nROCK", key="btn_r", use_container_width=True):
        play('R'); st.rerun()
with c2:
    if st.button("📄\nPAPER", key="btn_p", use_container_width=True):
        play('P'); st.rerun()
with c3:
    if st.button("✂️\nSCISSORS", key="btn_s", use_container_width=True):
        play('S'); st.rerun()

# ── BATTLE ARENA ──────────────────────────────────────────────────────────────
lr = st.session_state.last_result
if lr:
    u_e = EMOJIS[lr['user']]; c_e = EMOJIS[lr['cpu']]
    u_l = LABELS[lr['user']]; c_l = LABELS[lr['cpu']]
    res = lr['result'];        msg = lr['msg']

    st.markdown(f"""
<div class="arena">
  <div class="arena-side">
    <div class="arena-tag">You</div>
    <span class="arena-emoji">{u_e}</span>
    <div class="arena-name">{u_l}</div>
  </div>
  <div class="vs">VS</div>
  <div class="arena-side">
    <div class="arena-tag">CPU</div>
    <span class="arena-emoji">{c_e}</span>
    <div class="arena-name">{c_l}</div>
  </div>
</div>
<div class="result-banner result-{res}">{msg}</div>
""", unsafe_allow_html=True)
else:
    st.markdown("""
<div class="arena" style="justify-content:center;">
  <div style="text-align:center;color:#2a2a44;font-size:0.7rem;letter-spacing:0.4em;text-transform:uppercase;padding:1rem 0;">
    Awaiting your move...
  </div>
</div>
""", unsafe_allow_html=True)

# ── RESET ─────────────────────────────────────────────────────────────────────
_, mid, _ = st.columns([2, 1, 2])
with mid:
    if st.button("↺ Reset", key="btn_reset", use_container_width=True):
        for k in ['wins', 'losses', 'ties', 'history', 'last_result']:
            st.session_state[k] = 0 if k in ('wins', 'losses', 'ties') else ([] if k == 'history' else None)
        st.rerun()

# ── HISTORY ───────────────────────────────────────────────────────────────────
if st.session_state.history:
    rows_html = ""
    for h in st.session_state.history:
        rows_html += f"""
<div class="history-row h-{h['result']}">
  <span class="h-you">{EMOJIS[h['user']]} {LABELS[h['user']]}</span>
  <span class="h-badge {h['result']}">{h['result'].upper()}</span>
  <span class="h-cpu">{LABELS[h['cpu']]} {EMOJIS[h['cpu']]}</span>
</div>"""

    st.markdown(f"""
<div class="history-wrap">
  <div class="history-header">
    <span class="history-title">Round history</span>
    <span class="history-title">{total} played</span>
  </div>
  {rows_html}
</div>
""", unsafe_allow_html=True)
