// =============================================================
//  script.js  —  Rock Paper Scissors ARENA
//  Handles: game logic, Flask API calls, animations, sound, particles
// =============================================================

// ── Grab DOM Elements ─────────────────────────────────────────
const choiceBtns    = document.querySelectorAll('.choice-btn');
const playerEmoji   = document.getElementById('player-emoji');
const playerName    = document.getElementById('player-name');
const cpuEmoji      = document.getElementById('cpu-emoji');
const cpuName       = document.getElementById('cpu-name');
const statusBar     = document.getElementById('status-bar');
const statusText    = document.getElementById('status-text');
const playerScoreEl = document.getElementById('player-score');
const cpuScoreEl    = document.getElementById('cpu-score');
const playerCard    = document.getElementById('player-score-card');
const cpuCard       = document.getElementById('cpu-score-card');
const playerDisplay = document.getElementById('player-display');
const cpuDisplay    = document.getElementById('cpu-display');
const restartBtn    = document.getElementById('restart-btn');
const roundNumEl    = document.getElementById('round-num');
const bgCanvas      = document.getElementById('bg-canvas');

// ── Game State Variables ──────────────────────────────────────
let playerScore = 0;  // Tracks player's total wins
let cpuScore    = 0;  // Tracks CPU's total wins
let round       = 0;  // Current round number
let isPlaying   = false; // Prevents double-clicks during animation

// ── Emoji Map: choice name → emoji ───────────────────────────
const EMOJI = {
  rock:     '🪨',
  paper:    '📄',
  scissors: '✂️'
};

// ── Web Audio API Setup (for sound effects without audio files)
const AudioCtx = window.AudioContext || window.webkitAudioContext;
let audioCtx = null;  // Created on first user interaction (browser policy)

/**
 * Creates a short beep/tone using the Web Audio API.
 * @param {number} freq    - Frequency in Hz (pitch)
 * @param {number} dur     - Duration in seconds
 * @param {string} type    - Oscillator type: 'sine','square','sawtooth','triangle'
 * @param {number} vol     - Volume 0.0 to 1.0
 */
function playTone(freq, dur, type = 'sine', vol = 0.3) {
  try {
    if (!audioCtx) audioCtx = new AudioCtx(); // Create context on first play

    const osc    = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();

    osc.connect(gainNode);
    gainNode.connect(audioCtx.destination);

    osc.type      = type;
    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);

    // Fade out to avoid clicking artefact
    gainNode.gain.setValueAtTime(vol, audioCtx.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + dur);

    osc.start(audioCtx.currentTime);
    osc.stop(audioCtx.currentTime + dur);
  } catch (e) {
    // Silently ignore if audio is unavailable
  }
}

// Convenience sound functions
const sounds = {
  click: () => playTone(520, 0.09, 'square', 0.18),
  win:   () => {
    playTone(523, 0.1, 'sine', 0.3);
    setTimeout(() => playTone(659, 0.1, 'sine', 0.3), 120);
    setTimeout(() => playTone(784, 0.2, 'sine', 0.3), 240);
  },
  lose:  () => {
    playTone(300, 0.15, 'sawtooth', 0.2);
    setTimeout(() => playTone(200, 0.3, 'sawtooth', 0.2), 160);
  },
  tie:   () => playTone(440, 0.25, 'triangle', 0.2),
};

// =============================================================
//  PARTICLE BACKGROUND (Canvas animation)
// =============================================================
const ctx    = bgCanvas.getContext('2d');
let particles = [];

/** Resize canvas to fill window */
function resizeCanvas() {
  bgCanvas.width  = window.innerWidth;
  bgCanvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

/** Create one particle with random properties */
function makeParticle() {
  return {
    x:    Math.random() * bgCanvas.width,
    y:    Math.random() * bgCanvas.height,
    r:    Math.random() * 1.5 + 0.4,    // radius
    vx:   (Math.random() - 0.5) * 0.3,  // x velocity
    vy:   (Math.random() - 0.5) * 0.3,  // y velocity
    // Random neon color
    hue:  Math.random() > 0.5 ? 185 : 330, // cyan or magenta hue
    alpha: Math.random() * 0.5 + 0.15,
  };
}

// Initialise 80 particles
for (let i = 0; i < 80; i++) particles.push(makeParticle());

/** Draw and move all particles each frame */
function animateParticles() {
  ctx.clearRect(0, 0, bgCanvas.width, bgCanvas.height);

  particles.forEach(p => {
    // Draw
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
    ctx.fillStyle = `hsla(${p.hue}, 100%, 70%, ${p.alpha})`;
    ctx.fill();

    // Move
    p.x += p.vx;
    p.y += p.vy;

    // Wrap around edges
    if (p.x < 0) p.x = bgCanvas.width;
    if (p.x > bgCanvas.width) p.x = 0;
    if (p.y < 0) p.y = bgCanvas.height;
    if (p.y > bgCanvas.height) p.y = 0;
  });

  requestAnimationFrame(animateParticles);
}
animateParticles(); // Start the loop

// =============================================================
//  CHOICE BUTTON CLICK HANDLER
// =============================================================
choiceBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    if (isPlaying) return; // Block while a round is in progress
    const choice = btn.dataset.choice;
    playRound(choice, btn);
  });
});

/**
 * Main game function — runs one full round.
 * @param {string} userChoice - 'rock', 'paper', or 'scissors'
 * @param {HTMLElement} btn   - The clicked button element
 */
async function playRound(userChoice, btn) {
  isPlaying = true;
  round++;
  roundNumEl.textContent = round;

  sounds.click(); // Click sound

  // ── 1. Show user choice immediately ───────────────────────
  showUserChoice(userChoice, btn);

  // ── 2. Show "thinking" state ───────────────────────────────
  showThinking();

  // ── 3. Disable all buttons during processing ───────────────
  setButtonsDisabled(true);

  // ── 4. Send user choice to Flask backend ───────────────────
  let data;
  try {
    const response = await fetch('/play', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ choice: userChoice })
    });

    if (!response.ok) throw new Error('Server error');
    data = await response.json();

  } catch (err) {
    // If Flask is down or there's a network error
    statusBar.className = 'status-bar';
    statusText.textContent = '⚠️ Could not connect to server. Is Flask running?';
    setButtonsDisabled(false);
    isPlaying = false;
    return;
  }

  // ── 5. Small dramatic delay before revealing CPU choice ────
  await delay(900);

  // ── 6. Reveal computer's choice ───────────────────────────
  revealCpuChoice(data.computer);

  // ── 7. Show result after a brief pause ────────────────────
  await delay(400);
  showResult(data.result, data.user, data.computer);

  // ── 8. Re-enable buttons ───────────────────────────────────
  await delay(600);
  setButtonsDisabled(false);
  isPlaying = false;
}

// =============================================================
//  UI UPDATE HELPERS
// =============================================================

/** Show the player's choice on the left card */
function showUserChoice(choice, btn) {
  // Clear previous glow classes
  playerDisplay.className = 'choice-display reveal';

  playerEmoji.textContent = EMOJI[choice];
  playerName.textContent  = choice;

  // Trigger pop animation
  playerEmoji.classList.remove('pop');
  void playerEmoji.offsetWidth; // Force reflow to restart animation
  playerEmoji.classList.add('pop');

  // Highlight the selected button briefly
  btn.classList.add('selected');
  setTimeout(() => btn.classList.remove('selected'), 400);

  // Reset CPU display to waiting state
  cpuDisplay.className = 'choice-display';
  cpuEmoji.textContent = '⏳';
  cpuName.textContent  = '...';
}

/** Show "thinking" animation in status bar */
function showThinking() {
  statusBar.className = 'status-bar thinking';
  statusText.innerHTML = `CPU is thinking <span class="thinking-dots">
    <span>.</span><span>.</span><span>.</span>
  </span>`;
}

/** Reveal the CPU's choice on the right card */
function revealCpuChoice(choice) {
  cpuDisplay.classList.add('reveal');

  cpuEmoji.textContent = EMOJI[choice];
  cpuName.textContent  = choice;

  cpuEmoji.classList.remove('pop');
  void cpuEmoji.offsetWidth;
  cpuEmoji.classList.add('pop');
}

/**
 * Show the round result: update status bar, scores, glow effects, sounds.
 * @param {string} result - 'win', 'lose', or 'tie'
 * @param {string} user   - user's choice
 * @param {string} cpu    - cpu's choice
 */
function showResult(result, user, cpu) {
  // Remove all state classes from displays
  playerDisplay.classList.remove('win-glow','lose-glow','tie-glow','shake');
  cpuDisplay.classList.remove('win-glow','lose-glow','tie-glow','shake');
  playerCard.classList.remove('player-win','cpu-win','bump');
  cpuCard.classList.remove('player-win','cpu-win','bump');
  statusBar.className = 'status-bar';

  if (result === 'win') {
    // ── Player wins ──────────────────────────────────────────
    playerScore++;
    animateScore(playerScoreEl, playerScore);

    statusBar.classList.add('win');
    statusText.textContent = `🏆 You win! ${capitalise(user)} beats ${capitalise(cpu)}!`;

    playerDisplay.classList.add('win-glow');
    cpuDisplay.classList.add('lose-glow', 'shake');
    playerCard.classList.add('player-win', 'bump');

    sounds.win();
    spawnConfetti();  // Celebratory confetti!

  } else if (result === 'lose') {
    // ── CPU wins ─────────────────────────────────────────────
    cpuScore++;
    animateScore(cpuScoreEl, cpuScore);

    statusBar.classList.add('lose');
    statusText.textContent = `💀 CPU wins! ${capitalise(cpu)} beats ${capitalise(user)}!`;

    cpuDisplay.classList.add('win-glow');
    playerDisplay.classList.add('lose-glow', 'shake');
    cpuCard.classList.add('cpu-win', 'bump');

    sounds.lose();

  } else {
    // ── Tie ───────────────────────────────────────────────────
    statusBar.classList.add('tie');
    statusText.textContent = `🤝 It's a tie! Both chose ${capitalise(user)}.`;

    playerDisplay.classList.add('tie-glow');
    cpuDisplay.classList.add('tie-glow');

    sounds.tie();
  }
}

/** Animate score number rolling up to new value */
function animateScore(el, target) {
  let current = parseInt(el.textContent) || 0;
  const step  = () => {
    if (current < target) {
      current++;
      el.textContent = current;
      setTimeout(step, 60);
    }
  };
  step();
}

/** Enable or disable all choice buttons */
function setButtonsDisabled(disabled) {
  choiceBtns.forEach(btn => btn.disabled = disabled);
}

// =============================================================
//  RESTART BUTTON
// =============================================================
restartBtn.addEventListener('click', () => {
  sounds.click();
  resetGame();
});

function resetGame() {
  playerScore = 0;
  cpuScore    = 0;
  round       = 0;

  playerScoreEl.textContent = '0';
  cpuScoreEl.textContent    = '0';
  roundNumEl.textContent    = '0';

  playerEmoji.textContent = '❓';
  playerName.textContent  = '—';
  cpuEmoji.textContent    = '🤖';
  cpuName.textContent     = '—';

  playerDisplay.className = 'choice-display';
  cpuDisplay.className    = 'choice-display';
  playerCard.className    = 'score-card';
  cpuCard.className       = 'score-card';

  statusBar.className   = 'status-bar';
  statusText.textContent = 'Pick a weapon to start!';

  setButtonsDisabled(false);
  isPlaying = false;
}

// =============================================================
//  CONFETTI BURST (spawned on win)
// =============================================================
const CONFETTI_COLORS = ['#00f5ff','#ff2d78','#ffe600','#39ff14','#ffffff'];

function spawnConfetti() {
  const cx = window.innerWidth  / 2;
  const cy = window.innerHeight / 2;

  for (let i = 0; i < 40; i++) {
    const piece = document.createElement('div');
    piece.className = 'confetti-piece';
    piece.style.cssText = `
      left: ${cx + (Math.random() - 0.5) * 200}px;
      top:  ${cy + (Math.random() - 0.5) * 100}px;
      background: ${CONFETTI_COLORS[Math.floor(Math.random() * CONFETTI_COLORS.length)]};
      animation-duration: ${0.8 + Math.random() * 0.7}s;
      animation-delay: ${Math.random() * 0.3}s;
      transform: rotate(${Math.random() * 360}deg);
    `;
    document.body.appendChild(piece);

    // Remove the piece from DOM after its animation ends
    piece.addEventListener('animationend', () => piece.remove());
  }
}

// =============================================================
//  UTILITY
// =============================================================

/** Capitalise first letter: 'rock' → 'Rock' */
function capitalise(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

/** Simple promise-based delay */
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// =============================================================
//  KEYBOARD SUPPORT
//  Press 1 = Rock, 2 = Paper, 3 = Scissors
// =============================================================
document.addEventListener('keydown', (e) => {
  if (isPlaying) return;
  const map = { '1': 'rock', '2': 'paper', '3': 'scissors' };
  if (map[e.key]) {
    const btn = document.querySelector(`[data-choice="${map[e.key]}"]`);
    if (btn) playRound(map[e.key], btn);
  }
});
