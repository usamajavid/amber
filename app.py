import streamlit as st
import base64
import random
import streamlit.components.v1 as components

st.set_page_config(page_title="Amber ❤️ Usama", page_icon="💖", layout="centered")

# ------------------------ AUDIO ------------------------
@st.cache_data
def load_audio_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

AUDIO_B64 = load_audio_b64("music.mp3")

# ------------------------ GLOBAL THEME (FULL PAGE BACKGROUND) ------------------------
st.markdown(
    """
<style>
/* FULL PAGE BACKGROUND */
html, body, [data-testid="stAppViewContainer"] {
    height: 100%;
    background:
      radial-gradient(900px 500px at 20% 10%, rgba(255,75,139,0.25), transparent 55%),
      radial-gradient(800px 500px at 80% 30%, rgba(255,123,189,0.18), transparent 60%),
      linear-gradient(180deg, #090016, #1a002d) !important;
}

/* Remove default white background */
[data-testid="stAppViewContainer"] > .main {
    background: transparent !important;
}

/* Center width + space for top bar */
.block-container {
    padding-top: 4.5rem !important;
    max-width: 880px !important;
}

/* Card */
.val-card {
    background: rgba(255,255,255,0.92);
    border: 1px solid rgba(255,255,255,0.55);
    border-radius: 26px;
    padding: 28px;
    box-shadow: 0 18px 60px rgba(0,0,0,0.35);
    text-align: center;
}

/* Text */
.val-title {
    font-family: ui-sans-serif, system-ui;
    font-size: 42px;
    font-weight: 900;
    color: #2b0a1a;
}
.val-sub {
    font-family: ui-sans-serif, system-ui;
    font-size: 15px;
    font-weight: 650;
    color: #5b2b3f;
    opacity: 0.92;
    margin-top: 8px;
    line-height: 1.6;
}

/* Buttons */
.stButton > button{
    width: 100%;
    border: 0 !important;
    border-radius: 18px !important;
    padding: 0.85rem 1rem !important;
    font-size: 18px !important;
    font-weight: 850 !important;
    color: white !important;
    background: linear-gradient(135deg, rgba(255,75,139,0.98), rgba(255,123,189,0.98)) !important;
    box-shadow: 0 18px 45px rgba(255,75,139,0.25) !important;
}
.stButton > button:hover{ filter: brightness(1.02); }
.stButton > button:active{ transform: scale(0.99); }

/* Keep content above hearts */
section.main > div { position: relative; z-index: 3; }

/* Progress spacing */
[data-testid="stProgress"] { margin: 10px 0 20px 0; }
</style>
""",
    unsafe_allow_html=True
)

# ------------------------ HEARTS (PURE CSS — WORKS EVERY TIME) ------------------------
def render_hearts(n=35):
    emojis = ["💖", "💕", "💘", "❤️", "🌹", "✨"]
    spans = []
    for _ in range(n):
        left = random.randint(0, 100)
        size = random.randint(18, 36)
        dur = round(random.uniform(7.5, 14.5), 2)
        delay = round(random.uniform(0, 6), 2)
        drift = random.randint(-90, 90)
        emoji = random.choice(emojis)
        spans.append(
            f"<span class='vheart' style='--l:{left}vw; --s:{size}px; --d:{dur}s; --t:{delay}s; --x:{drift}px'>{emoji}</span>"
        )

    st.markdown(
        f"""
        <style>
        .vhearts {{
          position: fixed;
          inset: 0;
          pointer-events: none;
          z-index: 2; /* above background */
          overflow: hidden;
        }}
        .vheart {{
          position: absolute;
          left: var(--l);
          bottom: -60px;
          font-size: var(--s);
          animation: vfloat var(--d) linear infinite;
          animation-delay: var(--t);
          filter: drop-shadow(0 10px 16px rgba(255,75,139,0.25));
          opacity: 0.95;
          will-change: transform, opacity;
        }}
        @keyframes vfloat {{
          0%   {{ transform: translate(0, 0) rotate(0deg); opacity: .95; }}
          15%  {{ opacity: .95; }}
          100% {{ transform: translate(var(--x), -125vh) rotate(22deg); opacity: 0; }}
        }}
        </style>

        <div class="vhearts">
          {''.join(spans)}
        </div>
        """,
        unsafe_allow_html=True
    )

render_hearts()

# ------------------------ MUSIC BAR (TOP) ------------------------
components.html(
    f"""
<style>
.musicbar {{
  position: fixed;
  left: 50%;
  transform: translateX(-50%);
  top: 16px;
  width: min(900px, calc(100vw - 28px));
  background: rgba(255,255,255,0.10);
  border: 1px solid rgba(255,255,255,0.16);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-radius: 18px;
  padding: 12px 14px;
  z-index: 9999;
  box-shadow: 0 18px 60px rgba(0,0,0,0.35);
  display: flex;
  gap: 10px;
  align-items: center;
}}

.mb-title {{
  flex: 1;
  color: rgba(255,255,255,0.92);
  font-family: ui-sans-serif, system-ui;
  font-weight: 750;
  font-size: 13px;
  line-height: 1.2;
}}
.mb-sub {{
  display:block;
  color: rgba(255,255,255,0.65);
  font-weight: 650;
  font-size: 11px;
  margin-top: 2px;
}}

.mb-btn {{
  border: none;
  cursor: pointer;
  background: linear-gradient(135deg, rgba(255,75,139,0.95), rgba(255,123,189,0.95));
  color: white;
  border-radius: 14px;
  padding: 10px 12px;
  font-family: ui-sans-serif, system-ui;
  font-weight: 850;
  font-size: 12px;
  box-shadow: 0 16px 40px rgba(255,75,139,0.18);
}}
.mb-btn:active {{ transform: scale(0.98); }}
</style>

<audio id="bgm" loop>
  <source src="data:audio/mp3;base64,{AUDIO_B64}" type="audio/mp3" />
</audio>

<div class="musicbar">
  <div class="mb-title">
    For Amber 💖
    <span class="mb-sub">Tap Play (browsers block autoplay until you interact)</span>
  </div>
  <button class="mb-btn" id="mbPlay">▶ Play</button>
  <button class="mb-btn" id="mbPause" style="display:none;">⏸ Pause</button>
</div>

<script>
  const audio = document.getElementById("bgm");
  const playBtn = document.getElementById("mbPlay");
  const pauseBtn = document.getElementById("mbPause");

  const saved = localStorage.getItem("val_music_on");
  if (saved === "true") {{
    audio.volume = 0.45;
    audio.play().then(()=> {{
      playBtn.style.display="none";
      pauseBtn.style.display="inline-block";
    }}).catch(()=>{{}});
  }}

  playBtn.addEventListener("click", async () => {{
    audio.volume = 0.45;
    try {{
      await audio.play();
      localStorage.setItem("val_music_on","true");
      playBtn.style.display="none";
      pauseBtn.style.display="inline-block";
    }} catch(e) {{
      playBtn.textContent = "🔊 Tap again";
    }}
  }});

  pauseBtn.addEventListener("click", () => {{
    audio.pause();
    localStorage.setItem("val_music_on","false");
    pauseBtn.style.display="none";
    playBtn.style.display="inline-block";
    playBtn.textContent = "▶ Play";
  }});
</script>
""",
    height=80
)

# ------------------------ STATE ------------------------
if "stage" not in st.session_state:
    st.session_state.stage = 0
if "score" not in st.session_state:
    st.session_state.score = 0

def go(stage: int):
    st.session_state.stage = stage
    st.rerun()

# ------------------------ QUIZ ------------------------
quiz = [
    ("Where did we first meet?", ["At university", "In your house", "On the street"], "In your house"),
    ("Where did we go for our first date?", ["Hyde Park", "V&A museum", "Cinema"], "V&A museum"),
    ("Amber, do you like me?", ["Maybe", "I love you", "You're okay 😅"], "I love you"),
]
TOTAL = len(quiz)

# Progress
st.progress(min(1.0, st.session_state.score / TOTAL if TOTAL else 0))

# ------------------------ PAGES ------------------------
if st.session_state.stage == 0:
    st.markdown(
        """
        <div class="val-card">
            <div class="val-title">Amber 💖</div>
            <div class="val-sub">
                I made this just for you. Put your headphones on… then press start. 💌
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write("")
    if st.button("Start Our Love Story 💞"):
        go(1)

elif 1 <= st.session_state.stage <= TOTAL:
    q, options, answer = quiz[st.session_state.stage - 1]

    st.markdown(
        f"""
        <div class="val-card">
            <div class="val-title" style="font-size:28px;">Question {st.session_state.stage} of {TOTAL}</div>
            <div class="val-sub" style="font-size:18px; margin-top:10px;">{q}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    cols = st.columns(2)
    for i, opt in enumerate(options):
        with cols[i % 2]:
            if st.button(opt, key=f"opt_{st.session_state.stage}_{i}"):
                if opt == answer:
                    st.session_state.score += 1
                st.session_state.stage += 1
                st.rerun()

elif st.session_state.stage == TOTAL + 1:
    st.markdown(
        """
        <div class="val-card">
            <div class="val-title">Unlocked 💞</div>
            <div class="val-sub">Your surprise is ready…</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write("")
    if st.button("Open Your Surprise 💌"):
        go(TOTAL + 2)

elif st.session_state.stage == TOTAL + 2:
    st.markdown(
        """
        <div class="val-card">
            <div class="val-title">My Valentine Proposal 💍</div>
            <div class="val-sub" style="text-align:left; margin-top:16px; font-size:16px; line-height:1.75;">
            Hi baby,<br><br>
            This is my Valentine’s Day proposal for you.
            I would be the luckiest man in the world if you could accept my proposal and let me take you on a date.<br><br>
            I love you.<br>
            I cherish you.<br>
            And I want to hangout with you for the rest of my life. ❤️<br><br>
            — Usama
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write("")
    if st.button("Continue 💖"):
        go(TOTAL + 3)

elif st.session_state.stage == TOTAL + 3:
    st.markdown(
        """
        <div class="val-card">
            <div class="val-title">Amber 💖</div>
            <div class="val-sub" style="font-size:20px; margin-top:12px;">
                Will you be my Valentine?
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("YES 💕"):
            go(TOTAL + 4)
    with c2:
        if st.button("OF COURSE 😍"):
            go(TOTAL + 4)

elif st.session_state.stage == TOTAL + 4:
    st.markdown(
        """
        <div class="val-card">
            <div class="val-title" style="font-size:30px;">One last thing 💗</div>
            <div class="val-sub" style="font-size:18px; margin-top:12px;">
                Where do you wanna go for our date?
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🧺 Small picnic"):
            go(TOTAL + 5)
    with c2:
        if st.button("🏙️ London"):
            go(TOTAL + 5)

else:
    st.balloons()
    st.markdown(
        """
        <div class="val-card">
            <div class="val-title">Perfect 💖</div>
            <div class="val-sub" style="font-size:18px;">
                It’s a date 😘 <br>
                I can’t wait to spend this day with you, Amber ❤️
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    if st.button("Replay ✨"):
        st.session_state.stage = 0
        st.session_state.score = 0
        st.rerun()
