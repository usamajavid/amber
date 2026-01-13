import streamlit as st
import base64
import random
import streamlit.components.v1 as components

st.set_page_config(page_title="Amber ❤️ Osama", layout="centered")

# ---------- Load music once ----------
@st.cache_data
def load_mp3_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()

MUSIC_BYTES = load_mp3_bytes("music.mp3")

# ---------- Session state ----------
if "stage" not in st.session_state:
    st.session_state.stage = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "music_on" not in st.session_state:
    st.session_state.music_on = False

# ---------- Valentine styling ----------
st.markdown("""
<style>
:root{
  --pink:#ff4b6e;
  --bg1:#ffe6f0;
  --bg2:#fff0f5;
}
body { background: linear-gradient(var(--bg1), var(--bg2)); }
.block-container { padding-top: 1.2rem; }
.card{
  background: white;
  padding: 26px;
  border-radius: 22px;
  box-shadow: 0 10px 30px rgba(255, 75, 110, 0.18);
  text-align: center;
  position: relative;
  z-index: 5;
}
.big{ font-size: 42px; color: var(--pink); font-weight: 800; }
.sub{ font-size: 16px; opacity: 0.8; margin-top: 6px; }
.small{ font-size: 14px; opacity: 0.75; }

.stButton > button{
  background: var(--pink) !important;
  color: white !important;
  border-radius: 18px !important;
  font-size: 18px !important;
  padding: 0.55rem 1rem !important;
  border: none !important;
  width: 100%;
}
.stButton > button:hover{ filter: brightness(0.98); }
</style>
""", unsafe_allow_html=True)

# ---------- Floating hearts (visible + no iframe needed) ----------
# We use an HTML component with a non-zero height so it actually renders.
components.html("""
<style>
.hearts-wrap { position: fixed; inset: 0; pointer-events:none; z-index: 2; }
.heart {
  position: absolute;
  bottom: -30px;
  animation: floatUp linear forwards;
  opacity: 0.95;
  filter: drop-shadow(0 6px 12px rgba(255,75,110,0.25));
}
@keyframes floatUp {
  from { transform: translateY(0) translateX(0); opacity: 0.95; }
  to   { transform: translateY(-120vh) translateX(var(--drift)); opacity: 0.0; }
}
</style>
<div class="hearts-wrap" id="hw"></div>
<script>
(function(){
  if (window.__VAL_HEARTS__) return;
  window.__VAL_HEARTS__ = true;

  const wrap = document.getElementById("hw");
  const emojis = ["💖","💕","💘","❤️","🌹"];
  function spawn(){
    const h = document.createElement("div");
    h.className = "heart";
    h.textContent = emojis[Math.floor(Math.random()*emojis.length)];
    h.style.left = (Math.random()*100) + "vw";
    h.style.fontSize = (18 + Math.random()*18) + "px";
    h.style.setProperty("--drift", ((Math.random()*80)-40) + "px");
    const dur = 6 + Math.random()*6;
    h.style.animationDuration = dur + "s";
    wrap.appendChild(h);
    setTimeout(()=>h.remove(), (dur+0.5)*1000);
  }
  setInterval(spawn, 450);
})();
</script>
""", height=10)

# ---------- MUSIC UI (reliable) ----------
st.markdown("<div class='card'><div class='big'>Amber 💖</div><div class='sub'>A Valentine just for you</div></div>", unsafe_allow_html=True)
st.write("")

colA, colB = st.columns([1,1], vertical_alignment="center")

with colA:
    if st.button("🎵 Play / Pause Music"):
        st.session_state.music_on = not st.session_state.music_on

with colB:
    st.markdown(
        "<div class='small'>Tip: Browsers block autoplay. Tap Play once and it’ll work.</div>",
        unsafe_allow_html=True
    )

# Show audio player only when music_on is True (or always if you prefer)
if st.session_state.music_on:
    # Native Streamlit audio player (most compatible)
    st.audio(MUSIC_BYTES, format="audio/mp3")

st.write("")

# ---------- Quiz data ----------
quiz = [
    ("Where did we first meet?", ["At university", "In your house", "On the street"], "In your house"),
    ("Where did we go for our first date?", ["Hyde Park", "V&A museum", "Cinema"], "V&A museum"),
    ("Amber, do you like me?", ["Maybe", "I love you", "You're okay 😅"], "I love you"),
]

TOTAL_Q = len(quiz)

# ---------- Welcome / Flow ----------
if st.session_state.stage == 0:
    st.markdown("""
    <div class='card'>
      <h2>Ready for a little love game? 💝</h2>
      <p class='small'>Answer the questions… and unlock your surprise.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Start Our Love Story ❤️"):
        st.session_state.stage = 1

elif 1 <= st.session_state.stage <= TOTAL_Q:
    q, options, answer = quiz[st.session_state.stage - 1]

    st.markdown(f"<div class='card'><h2>{q}</h2></div>", unsafe_allow_html=True)
    st.write("")

    # Answer selection
    if not st.session_state.answered:
        for opt in options:
            if st.button(opt, key=f"opt_{st.session_state.stage}_{opt}"):
                st.session_state.answered = True
                if opt == answer:
                    st.session_state.score += 1
                    st.success("Correct 💕")
                else:
                    st.warning("Even if you missed it… I still love you 😘")

    # Next page
    if st.session_state.answered:
        st.write("")
        if st.button("Next ❤️", key=f"next_{st.session_state.stage}"):
            st.session_state.stage += 1
            st.session_state.answered = False

    # Love meter (fills correctly)
    st.write("")
    st.markdown("### Love Meter 💖")
    st.progress(st.session_state.score / TOTAL_Q)
    st.caption(f"Score: {st.session_state.score}/{TOTAL_Q}")

elif st.session_state.stage == TOTAL_Q + 1:
    st.markdown("<div class='card'><div class='big'>Love Meter Full 💞</div><p>Time for your surprise…</p></div>", unsafe_allow_html=True)
    if st.button("Open Your Surprise 💌"):
        st.session_state.stage += 1

elif st.session_state.stage == TOTAL_Q + 2:
    st.balloons()
    st.markdown("""
    <div class='card'>
      <div class='big'>Amber 💕</div>
      <h3>My Valentine Proposal</h3>
      <p style="line-height:1.6;">
        Hi baby,<br><br>
        This is my Valentine’s Day proposal for you.
        I would be the luckiest man in the world if you could accept my proposal and let me take you on a date.<br><br>
        I love you.<br>
        I cherish you.<br>
        And I want to hang out with you for the rest of my life. ❤️<br><br>
        — Osama
      </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("💍 Continue"):
        st.session_state.stage += 1

elif st.session_state.stage == TOTAL_Q + 3:
    st.markdown("""
    <div class='card'>
      <div class='big'>Amber 💖</div>
      <h2>Will you be my Valentine?</h2>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("YES 💕"):
            st.session_state.stage += 1
    with c2:
        if st.button("OF COURSE 😍"):
            st.session_state.stage += 1

else:
    st.balloons()
    st.markdown("""
    <div class='card'>
      <div class='big'>Yayyy 💖</div>
      <h2>We have a Valentine date now 😘</h2>
      <p>I can’t wait to spend this special day with you, Amber ❤️</p>
    </div>
    """, unsafe_allow_html=True)
