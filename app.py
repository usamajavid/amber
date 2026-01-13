import streamlit as st
import base64
import random
import glob
import os
from datetime import datetime
import streamlit.components.v1 as components

st.set_page_config(page_title="Amber ❤️ Usama", page_icon="💖", layout="centered")

# ------------------------ AUDIO ------------------------
@st.cache_data
def load_audio_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

AUDIO_B64 = load_audio_b64("music.mp3")

# ------------------------ GLOBAL THEME ------------------------
st.markdown(
    """
<style>
html, body, [data-testid="stAppViewContainer"] {
    height: 100%;
    background:
      radial-gradient(900px 500px at 20% 10%, rgba(255,75,139,0.25), transparent 55%),
      radial-gradient(800px 500px at 80% 30%, rgba(255,123,189,0.18), transparent 60%),
      linear-gradient(180deg, #090016, #1a002d) !important;
}
[data-testid="stAppViewContainer"] > .main { background: transparent !important; }
.block-container { padding-top: 2.2rem !important; max-width: 980px !important; }

.val-card {
    background: rgba(255,255,255,0.92);
    border: 1px solid rgba(255,255,255,0.55);
    border-radius: 26px;
    padding: 28px;
    box-shadow: 0 18px 60px rgba(0,0,0,0.35);
    text-align: center;
}
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

section.main > div { position: relative; z-index: 3; }
[data-testid="stProgress"] { margin: 10px 0 18px 0; }

/* Timeline */
.timeline {
  text-align: left;
  margin-top: 14px;
  background: rgba(255,255,255,0.82);
  border: 1px solid rgba(255,255,255,0.55);
  border-radius: 20px;
  padding: 18px;
}
.trow {
  display: flex;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid rgba(91,43,63,0.12);
}
.trow:last-child { border-bottom: none; }
.ticon { font-size: 22px; width: 32px; text-align: center; }
.ttitle { font-weight: 900; color: #2b0a1a; font-family: ui-sans-serif, system-ui; }
.tdesc { color: #5b2b3f; opacity: 0.92; font-weight: 650; font-family: ui-sans-serif, system-ui; }

/* Gallery */
.gallery-card {
  background: rgba(255,255,255,0.92);
  border: 1px solid rgba(255,255,255,0.55);
  border-radius: 26px;
  padding: 18px;
  box-shadow: 0 18px 60px rgba(0,0,0,0.22);
}
.caption {
  font-family: ui-sans-serif, system-ui;
  font-weight: 800;
  color: #2b0a1a;
  margin-top: 8px;
}
.subcap {
  font-family: ui-sans-serif, system-ui;
  font-weight: 650;
  color: #5b2b3f;
  opacity: 0.9;
}

/* Invitation */
.ticket {
  background: radial-gradient(900px 500px at 20% 10%, rgba(255,75,139,0.18), transparent 55%),
              linear-gradient(135deg, rgba(255,255,255,0.92), rgba(255,255,255,0.85));
  border: 1px solid rgba(255,255,255,0.65);
  border-radius: 26px;
  padding: 26px;
  box-shadow: 0 18px 60px rgba(0,0,0,0.30);
  text-align: left;
}
.ticket h2 {
  margin: 0;
  font-family: ui-sans-serif, system-ui;
  color: #2b0a1a;
  font-weight: 950;
}
.ticket .meta {
  margin-top: 10px;
  font-family: ui-sans-serif, system-ui;
  color: #5b2b3f;
  font-weight: 750;
  line-height: 1.8;
}
.badge {
  display: inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  background: linear-gradient(135deg, rgba(255,75,139,0.95), rgba(255,123,189,0.95));
  color: white;
  font-family: ui-sans-serif, system-ui;
  font-weight: 900;
  font-size: 12px;
  margin-top: 12px;
}
</style>
""",
    unsafe_allow_html=True
)

# ------------------------ HEARTS (PURE CSS) ------------------------
def render_hearts(n=38):
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
          position: fixed; inset: 0; pointer-events: none; z-index: 2; overflow: hidden;
        }}
        .vheart {{
          position: absolute; left: var(--l); bottom: -60px; font-size: var(--s);
          animation: vfloat var(--d) linear infinite; animation-delay: var(--t);
          filter: drop-shadow(0 10px 16px rgba(255,75,139,0.25));
          opacity: 0.95; will-change: transform, opacity;
        }}
        @keyframes vfloat {{
          0%   {{ transform: translate(0, 0) rotate(0deg); opacity: .95; }}
          15%  {{ opacity: .95; }}
          100% {{ transform: translate(var(--x), -125vh) rotate(22deg); opacity: 0; }}
        }}
        </style>
        <div class="vhearts">{''.join(spans)}</div>
        """,
        unsafe_allow_html=True
    )

render_hearts()

# ------------------------ MUSIC BUTTON (TOP RIGHT SMALL) ------------------------
components.html(
    f"""
<style>
.music-pill {{
  position: fixed;
  top: 16px;
  right: 16px;
  z-index: 9999;
  background: rgba(255,255,255,0.14);
  border: 1px solid rgba(255,255,255,0.22);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  color: rgba(255,255,255,0.92);
  border-radius: 999px;
  padding: 8px 10px;
  display: flex;
  gap: 8px;
  align-items: center;
  box-shadow: 0 18px 50px rgba(0,0,0,0.28);
  font-family: ui-sans-serif, system-ui;
  font-weight: 850;
  font-size: 12px;
}}
.music-btn {{
  border: none;
  cursor: pointer;
  background: linear-gradient(135deg, rgba(255,75,139,0.95), rgba(255,123,189,0.95));
  color: white;
  border-radius: 999px;
  padding: 7px 10px;
  font-weight: 950;
  font-size: 12px;
}}
.music-btn:active {{ transform: scale(0.98); }}
</style>

<audio id="bgm" loop>
  <source src="data:audio/mp3;base64,{AUDIO_B64}" type="audio/mp3" />
</audio>

<div class="music-pill">
  <span>🎵</span>
  <button class="music-btn" id="mbPlay">Play</button>
  <button class="music-btn" id="mbPause" style="display:none;">Pause</button>
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
      playBtn.textContent = "Tap";
    }}
  }});

  pauseBtn.addEventListener("click", () => {{
    audio.pause();
    localStorage.setItem("val_music_on","false");
    pauseBtn.style.display="none";
    playBtn.style.display="inline-block";
    playBtn.textContent = "Play";
  }});
</script>
""",
    height=0
)

# ------------------------ STATE ------------------------
if "stage" not in st.session_state:
    st.session_state.stage = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "date_choice" not in st.session_state:
    st.session_state.date_choice = None

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

st.progress(min(1.0, st.session_state.score / TOTAL if TOTAL else 0))

# ------------------------ GALLERY HELPERS ------------------------
def nice_caption(filename: str) -> str:
    base = os.path.splitext(os.path.basename(filename))[0]
    base = base.replace("_", " ").replace("-", " ").strip()
    if base[:2].isdigit() and len(base) > 3:
        base = base[2:].lstrip()
    return base.title() if base else "Memory"

def load_photos():
    paths = []
    for ext in ("jpg", "jpeg", "png", "webp"):
        paths += glob.glob(os.path.join("photos", f"*.{ext}"))
        paths += glob.glob(os.path.join("photos", f"*.{ext.upper()}"))
    paths = sorted(paths)
    return paths

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

# NEW: "Our Story" section (Timeline + Gallery)
elif st.session_state.stage == TOTAL + 1:
    st.markdown(
        """
        <div class="val-card">
            <div class="val-title">Our Story 💞</div>
            <div class="val-sub">Before the surprise… a few memories.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="timeline">
          <div class="trow">
            <div class="ticon">🏠</div>
            <div>
              <div class="ttitle">First time we met</div>
              <div class="tdesc">In your house — and everything changed.</div>
            </div>
          </div>
          <div class="trow">
            <div class="ticon">🏛️</div>
            <div>
              <div class="ttitle">First date</div>
              <div class="tdesc">V&amp;A museum — classy, cute, unforgettable.</div>
            </div>
          </div>
          <div class="trow">
            <div class="ticon">💖</div>
            <div>
              <div class="ttitle">Today</div>
              <div class="tdesc">Still choosing you. Every day. Always.</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.markdown("<div class='gallery-card'>", unsafe_allow_html=True)
    st.markdown("<div class='caption'>Our Memories 📸</div>", unsafe_allow_html=True)
    st.markdown("<div class='subcap'>Add photos in a folder named <b>photos/</b> to make this even more personal.</div>", unsafe_allow_html=True)

    photos = load_photos()
    st.write("")
    if photos:
        # show as a nice grid
        cols = st.columns(3)
        for idx, p in enumerate(photos[:12]):  # show up to 12 for a clean look
            with cols[idx % 3]:
                st.image(p, use_container_width=True)
                st.caption(nice_caption(p))
    else:
        st.info("No photos found yet. Create a folder named 'photos' and add JPG/PNG images to show them here.")

    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    if st.button("Continue to your surprise 💌"):
        go(TOTAL + 2)

elif st.session_state.stage == TOTAL + 2:
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
        go(TOTAL + 3)

elif st.session_state.stage == TOTAL + 3:
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
        go(TOTAL + 4)

elif st.session_state.stage == TOTAL + 4:
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
            go(TOTAL + 5)
    with c2:
        if st.button("OF COURSE 😍"):
            go(TOTAL + 5)

elif st.session_state.stage == TOTAL + 5:
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
            st.session_state.date_choice = "Small picnic 🧺"
            go(TOTAL + 6)
    with c2:
        if st.button("🏙️ London"):
            st.session_state.date_choice = "London 🏙️"
            go(TOTAL + 6)

# Invitation Card (NEW)
else:
    st.balloons()
    choice = st.session_state.date_choice or "A surprise date 💖"
    today = datetime.now().strftime("%d %b %Y")

    st.markdown(
        f"""
        <div class="ticket">
          <h2>Valentine Invitation 💌</h2>
          <div class="meta">
            <b>For:</b> Amber 💖<br>
            <b>From:</b> Usama ❤️<br><br>
            <b>Plan:</b> {choice}<br>
            <b>Date:</b> {today}<br>
            <b>Dress code:</b> Cute (as always) 😘<br>
            <b>Note:</b> I’ll take care of everything.
          </div>
          <div class="badge">CONFIRMED ✅</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
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
        st.session_state.date_choice = None
        st.rerun()
