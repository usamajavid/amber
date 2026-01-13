import streamlit as st
import base64
import random
import time
import streamlit.components.v1 as components

# ------------------------ PAGE CONFIG ------------------------
st.set_page_config(page_title="Amber ❤️ Osama", page_icon="💖", layout="centered")

# ------------------------ HELPERS ------------------------
@st.cache_data
def load_audio_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

AUDIO_B64 = load_audio_b64("music.mp3")

def ui_fx(audio_b64: str):
    """
    Premium UI layer:
    - gradient background
    - floating hearts
    - subtle sparkles
    - fixed music control bar with Play/Pause
    """
    components.html(
        f"""
        <style>
          :root {{
            --bg1: #090016;
            --bg2: #1a002d;
            --pink: #ff4b8b;
            --rose: #ff7bbd;
            --gold: #ffd1e6;
            --card: rgba(255,255,255,0.08);
            --stroke: rgba(255,255,255,0.14);
            --shadow: 0 18px 60px rgba(0,0,0,0.45);
          }}

          /* Background */
          body {{
            background: radial-gradient(900px 500px at 20% 10%, rgba(255,75,139,0.25), transparent 55%),
                        radial-gradient(800px 500px at 80% 30%, rgba(255,123,189,0.18), transparent 60%),
                        linear-gradient(180deg, var(--bg1), var(--bg2)) !important;
          }}

          /* Softer Streamlit container spacing */
          .block-container {{
            padding-top: 1.0rem !important;
            max-width: 880px !important;
          }}

          /* Floating hearts */
          .val-layer {{
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 0;
            overflow: hidden;
          }}

          .h {{
            position: absolute;
            bottom: -40px;
            opacity: 0.85;
            filter: drop-shadow(0 12px 18px rgba(255,75,139,0.20));
            animation: floatUp linear forwards;
          }}

          @keyframes floatUp {{
            from {{ transform: translateY(0) translateX(0) rotate(0deg); opacity: .9; }}
            to   {{ transform: translateY(-120vh) translateX(var(--dx)) rotate(var(--rot)); opacity: 0; }}
          }}

          /* Subtle sparkle */
          .spark {{
            position: absolute;
            width: 2px; height: 2px;
            background: rgba(255,255,255,0.6);
            border-radius: 999px;
            box-shadow: 0 0 12px rgba(255,255,255,0.35);
            animation: twinkle 2.4s ease-in-out infinite;
          }}
          @keyframes twinkle {{
            0%,100% {{ transform: scale(0.6); opacity: 0.3; }}
            50%     {{ transform: scale(1.5); opacity: 0.8; }}
          }}

          /* Music Bar */
          .musicbar {{
            position: fixed;
            left: 50%;
            transform: translateX(-50%);
            bottom: 18px;
            width: min(720px, calc(100vw - 28px));
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
            color: rgba(255,255,255,0.90);
            font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
            font-weight: 600;
            letter-spacing: .2px;
            font-size: 13px;
            line-height: 1.2;
          }}
          .mb-sub {{
            display:block;
            color: rgba(255,255,255,0.60);
            font-weight: 500;
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
            font-weight: 700;
            font-size: 12px;
            letter-spacing: .2px;
            box-shadow: 0 16px 40px rgba(255,75,139,0.18);
          }}
          .mb-btn:active {{ transform: scale(0.98); }}

          /* Make Streamlit widgets sit above background layer */
          section.main > div {{
            position: relative;
            z-index: 3;
          }}

        </style>

        <div class="val-layer" id="valLayer"></div>

        <audio id="bgm" loop>
          <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3" />
        </audio>

        <div class="musicbar">
          <div class="mb-title">
            For Amber 💖
            <span class="mb-sub">Tap play (browsers block autoplay until you interact)</span>
          </div>
          <button class="mb-btn" id="mbPlay">▶ Play</button>
          <button class="mb-btn" id="mbPause" style="display:none;">⏸ Pause</button>
        </div>

        <script>
          const layer = document.getElementById("valLayer");
          const audio = document.getElementById("bgm");
          const playBtn = document.getElementById("mbPlay");
          const pauseBtn = document.getElementById("mbPause");

          // Restore prior state
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

          // Floating hearts (prevent duplicates on reruns)
          if (!window.__VAL_HEARTS__) {{
            window.__VAL_HEARTS__ = true;
            const emojis = ["💖","💕","💘","❤️","🌹","✨"];
            function spawnHeart() {{
              const h = document.createElement("div");
              h.className = "h";
              h.textContent = emojis[Math.floor(Math.random()*emojis.length)];
              h.style.left = (Math.random()*100) + "vw";
              h.style.fontSize = (18 + Math.random()*22) + "px";
              h.style.setProperty("--dx", ((Math.random()*120)-60) + "px");
              h.style.setProperty("--rot", ((Math.random()*40)-20) + "deg");
              const dur = 7 + Math.random()*6;
              h.style.animationDuration = dur + "s";
              layer.appendChild(h);
              setTimeout(()=>h.remove(), (dur+0.5)*1000);
            }}
            setInterval(spawnHeart, 420);

            // Sparkles
            for (let i=0; i<24; i++) {{
              const s = document.createElement("div");
              s.className = "spark";
              s.style.left = (Math.random()*100) + "vw";
              s.style.top = (Math.random()*100) + "vh";
              s.style.animationDelay = (Math.random()*2.5) + "s";
              layer.appendChild(s);
            }}
          }}
        </script>
        """,
        height=120,  # IMPORTANT: not 0, so bar is visible
    )

def card(title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div style="
          background: rgba(255,255,255,0.08);
          border: 1px solid rgba(255,255,255,0.14);
          border-radius: 26px;
          padding: 26px 26px 22px 26px;
          box-shadow: 0 18px 60px rgba(0,0,0,0.40);
          backdrop-filter: blur(16px);
          -webkit-backdrop-filter: blur(16px);
          margin-bottom: 14px;
        ">
          <div style="font-family: ui-sans-serif, system-ui; font-weight: 900; font-size: 44px;
                      letter-spacing:-0.5px; color: rgba(255,255,255,0.95); line-height:1.05;">
            {title}
          </div>
          <div style="margin-top: 8px; font-family: ui-sans-serif, system-ui; font-weight: 600;
                      color: rgba(255,255,255,0.72); font-size: 15px; line-height:1.5;">
            {subtitle}
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def premium_button_css():
    st.markdown(
        """
        <style>
        .stButton > button{
          width: 100%;
          border: 0 !important;
          border-radius: 18px !important;
          padding: 0.85rem 1rem !important;
          font-size: 18px !important;
          font-weight: 800 !important;
          letter-spacing: 0.2px !important;
          color: rgba(255,255,255,0.95) !important;
          background: linear-gradient(135deg, rgba(255,75,139,0.95), rgba(255,123,189,0.95)) !important;
          box-shadow: 0 18px 45px rgba(255,75,139,0.20) !important;
        }
        .stButton > button:hover{ filter: brightness(1.02); }
        .stButton > button:active{ transform: scale(0.99); }
        </style>
        """,
        unsafe_allow_html=True
    )

def set_stage(new_stage: int):
    st.session_state.stage = new_stage
    st.rerun()

def answer_and_advance(is_correct: bool):
    if is_correct:
        st.session_state.score += 1
    st.session_state.stage += 1
    st.rerun()

# ------------------------ STATE ------------------------
if "stage" not in st.session_state:
    st.session_state.stage = 0
if "score" not in st.session_state:
    st.session_state.score = 0

# ------------------------ RENDER FX LAYER ------------------------
ui_fx(AUDIO_B64)
premium_button_css()

# ------------------------ QUIZ DATA ------------------------
quiz = [
    ("Where did we first meet?", ["At university", "In your house", "On the street"], "In your house"),
    ("Where did we go for our first date?", ["Hyde Park", "V&A museum", "Cinema"], "V&A museum"),
    ("Amber, do you like me?", ["Maybe", "I love you", "You're okay 😅"], "I love you"),
]
TOTAL = len(quiz)

# ------------------------ TOP PROGRESS ------------------------
# Professional progress indicator
progress = min(1.0, st.session_state.score / TOTAL if TOTAL else 0)
st.progress(progress)

# ------------------------ PAGES ------------------------
if st.session_state.stage == 0:
    card("Amber 💖", "I made this for you — a little love experience, not just a message.")
    st.markdown(
        "<div style='color:rgba(255,255,255,0.70); font-family:ui-sans-serif,system-ui; "
        "margin: 10px 0 18px 0;'>"
        "Put your headphones on… then press start. 💌"
        "</div>",
        unsafe_allow_html=True
    )
    if st.button("Start Our Love Story ❤️"):
        set_stage(1)

elif 1 <= st.session_state.stage <= TOTAL:
    q, options, correct = quiz[st.session_state.stage - 1]
    card("A little quiz…", f"Question {st.session_state.stage} of {TOTAL}")
    st.markdown(
        f"<div style='font-size:26px; font-weight:900; color:rgba(255,255,255,0.93); "
        f"font-family:ui-sans-serif,system-ui; margin: 6px 0 10px 0;'>{q}</div>",
        unsafe_allow_html=True
    )

    # Two-column options for a premium layout
    cols = st.columns(2)
    for i, opt in enumerate(options):
        with cols[i % 2]:
            if st.button(opt, key=f"opt_{st.session_state.stage}_{i}"):
                answer_and_advance(opt == correct)

    # Love meter (fills instantly when score increases)
    st.markdown(
        f"<div style='margin-top:14px; color:rgba(255,255,255,0.70); font-family:ui-sans-serif,system-ui;'>"
        f"Love Meter: <b style='color:rgba(255,255,255,0.95);'>{st.session_state.score}</b> / {TOTAL} 💗"
        f"</div>",
        unsafe_allow_html=True
    )

elif st.session_state.stage == TOTAL + 1:
    card("Unlocked 💞", "You’ve reached the surprise.")
    if st.button("Open your surprise 💌"):
        set_stage(TOTAL + 2)

elif st.session_state.stage == TOTAL + 2:
    # Letter with a premium feel
    st.markdown(
        """
        <div style="
          background: rgba(255,255,255,0.08);
          border: 1px solid rgba(255,255,255,0.14);
          border-radius: 26px;
          padding: 28px;
          box-shadow: 0 18px 60px rgba(0,0,0,0.40);
          backdrop-filter: blur(16px);
          -webkit-backdrop-filter: blur(16px);
        ">
          <div style="font-family:ui-sans-serif,system-ui; font-weight:900; font-size:36px; color:rgba(255,255,255,0.95);">
            My Valentine Proposal 💍
          </div>
          <div style="margin-top:14px; font-family:ui-sans-serif,system-ui; font-size:16px; line-height:1.75;
                      color:rgba(255,255,255,0.78);">
            Hi baby,<br><br>
            This is my Valentine’s Day proposal for you.
            I would be the luckiest man in the world if you could accept my proposal and let me take you on a date.<br><br>
            I love you.<br>
            I cherish you.<br>
            And I want to hang out with you for the rest of my life. ❤️<br><br>
            — Osama
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write("")
    if st.button("Continue 💖"):
        set_stage(TOTAL + 3)

elif st.session_state.stage == TOTAL + 3:
    card("Amber 💖", "One last question…")
    st.markdown(
        "<div style='font-size:30px; font-weight:950; color:rgba(255,255,255,0.95); "
        "font-family:ui-sans-serif,system-ui; margin: 6px 0 14px 0;'>"
        "Will you be my Valentine?"
        "</div>",
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button("YES 💕"):
            set_stage(TOTAL + 4)
    with c2:
        if st.button("OF COURSE 😍"):
            set_stage(TOTAL + 4)

else:
    st.balloons()
    card("Yayyy 💖", "We have a Valentine date now 😘")
    st.markdown(
        "<div style='color:rgba(255,255,255,0.78); font-family:ui-sans-serif,system-ui; "
        "font-size:16px; line-height:1.7;'>"
        "I can’t wait to spend this special day with you, Amber ❤️"
        "</div>",
        unsafe_allow_html=True
    )
    st.write("")
    if st.button("Replay ✨"):
        st.session_state.stage = 0
        st.session_state.score = 0
        st.rerun()
