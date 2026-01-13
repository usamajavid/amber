import streamlit as st
import base64
import streamlit.components.v1 as components

st.set_page_config(page_title="Amber ❤️ Osama", layout="centered")

# ---------------- MUSIC (WORKING) ----------------
def music_widget(file_path: str):
    with open(file_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    # Uses localStorage to remember play state across reruns/pages
    components.html(
        f"""
        <style>
          .music-pill {{
            position: fixed;
            top: 16px;
            right: 16px;
            z-index: 99999;
            background: #ff4b6e;
            color: white;
            border: none;
            padding: 10px 14px;
            border-radius: 999px;
            font-size: 14px;
            cursor: pointer;
            box-shadow: 0 6px 18px rgba(255, 75, 110, 0.35);
          }}
          .music-pill:active {{ transform: scale(0.98); }}
        </style>

        <audio id="bgm" loop>
          <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>

        <button class="music-pill" id="musicBtn">🎵 Play Music</button>

        <script>
          const audio = document.getElementById("bgm");
          const btn = document.getElementById("musicBtn");

          // Restore last state
          const saved = localStorage.getItem("musicOn");
          if (saved === "true") {{
            audio.volume = 0.4;
            audio.play().catch(()=>{{}});
            btn.innerText = "⏸ Pause Music";
          }}

          btn.addEventListener("click", async () => {{
            audio.volume = 0.4;

            if (audio.paused) {{
              try {{
                await audio.play();
                localStorage.setItem("musicOn", "true");
                btn.innerText = "⏸ Pause Music";
              }} catch (e) {{
                // If blocked, show a hint
                btn.innerText = "🔊 Tap again";
              }}
            }} else {{
              audio.pause();
              localStorage.setItem("musicOn", "false");
              btn.innerText = "🎵 Play Music";
            }}
          }});
        </script>
        """,
        height=0,
    )

# ---------------- HEARTS ----------------
def floating_hearts():
    components.html("""
    <style>
      .heart {
        position: fixed;
        bottom: -10px;
        font-size: 22px;
        animation: float 8s linear infinite;
        z-index: 1;
        pointer-events: none;
      }
      @keyframes float {
        from { transform: translateY(0); opacity: 0.9; }
        to   { transform: translateY(-110vh); opacity: 0.0; }
      }
    </style>
    <script>
      // Prevent duplicates on reruns
      if (!window.__heartsStarted) {
        window.__heartsStarted = true;

        function spawnHeart() {
          const h = document.createElement("div");
          h.className = "heart";
          h.textContent = ["💖","💕","💘","❤️"][Math.floor(Math.random()*4)];
          h.style.left = Math.random() * 100 + "vw";
          h.style.animationDuration = (Math.random()*4 + 6) + "s";
          h.style.fontSize = (Math.random()*12 + 18) + "px";
          document.body.appendChild(h);

          setTimeout(() => h.remove(), 9000);
        }

        setInterval(spawnHeart, 500);
      }
    </script>
    """, height=0)

# ---- render widgets once per page load ----
music_widget("music.mp3")
floating_hearts()

# ---------------- STATE ----------------
if "stage" not in st.session_state:
    st.session_state.stage = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False

# ---------------- STYLE ----------------
st.markdown("""
<style>
body { background: linear-gradient(#ffe6f0,#fff0f5); }
.card {
  background: white;
  padding: 26px;
  border-radius: 22px;
  box-shadow: 0px 0px 24px rgba(255, 75, 110, 0.25);
  text-align: center;
  position: relative;
  z-index: 5;
}
.big { font-size: 40px; color: #ff4b6e; }
button { border-radius: 20px !important; font-size: 18px !important; }
</style>
""", unsafe_allow_html=True)

# ---------------- WELCOME ----------------
if st.session_state.stage == 0:
    st.markdown("<div class='card'><div class='big'>Amber 💖</div><p>A Valentine just for you</p></div>", unsafe_allow_html=True)
    if st.button("Start Our Love Story ❤️"):
        st.session_state.stage = 1

# ---------------- QUIZ ----------------
quiz = [
    ("Where did we first meet?", ["At university","In your house","On the street"], "In your house"),
    ("Where did we go for our first date?", ["Hyde Park","V&A museum","Cinema"], "V&A museum"),
    ("Amber, do you like me?", ["Maybe","I love you","You're okay 😅"], "I love you")
]

if 1 <= st.session_state.stage <= 3:
    q, options, answer = quiz[st.session_state.stage - 1]
    st.markdown(f"<div class='card'><h2>{q}</h2>", unsafe_allow_html=True)

    if not st.session_state.answered:
        for opt in options:
            if st.button(opt, key=f"opt_{st.session_state.stage}_{opt}"):
                st.session_state.answered = True
                if opt == answer:
                    st.session_state.score += 1
                    st.success("Correct 💕")
                else:
                    st.warning("Still loved 😘")

    if st.session_state.answered:
        if st.button("Next ❤️", key=f"next_{st.session_state.stage}"):
            st.session_state.stage += 1
            st.session_state.answered = False

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("### Love Meter 💖")
    st.progress(st.session_state.score / 3)

# ---------------- UNLOCK ----------------
if st.session_state.stage == 4:
    st.markdown("<div class='card'><div class='big'>Love Meter Full 💞</div></div>", unsafe_allow_html=True)
    if st.button("Open Your Surprise 💌"):
        st.session_state.stage = 5

# ---------------- LOVE LETTER ----------------
if st.session_state.stage == 5:
    st.markdown("""
    <div class='card'>
      <div class='big'>Amber 💕</div>
      <p>
      Hi baby,<br><br>
      This is my Valentine’s Day proposal for you.
      I would be the luckiest man in the world if you could accept my proposal and let me take you on a date.<br><br>
      I love you. I cherish you. And I want to hang out with you for the rest of my life. ❤️<br><br>
      — Osama
      </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("💍 Continue"):
        st.session_state.stage = 6

# ---------------- FINAL PROPOSAL ----------------
if st.session_state.stage == 6:
    st.balloons()
    st.markdown("""
    <div class='card'>
      <div class='big'>Amber 💖</div>
      <h2>Will you be my Valentine?</h2>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("YES 💕"):
            st.session_state.stage = 7
    with c2:
        if st.button("OF COURSE 😍"):
            st.session_state.stage = 7

# ---------------- CELEBRATION ----------------
if st.session_state.stage == 7:
    st.balloons()
    st.markdown("""
    <div class='card'>
      <div class='big'>Yayyy 💖</div>
      <h2>We have a Valentine date now 😘</h2>
      <p>I can’t wait to spend this special day with you, Amber ❤️</p>
    </div>
    """, unsafe_allow_html=True)
