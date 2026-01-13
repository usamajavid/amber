import streamlit as st
import base64
import streamlit.components.v1 as components

st.set_page_config(page_title="Amber ❤️ Osama", layout="centered")

# ---------------- MUSIC ----------------
def play_music():
    with open("music.mp3", "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    components.html(f"""
    <audio id="bgm" loop>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    <script>
    var audio = document.getElementById("bgm");
    if (window.musicOn) {{ audio.play(); }}
    </script>
    """, height=0)

# ---------------- HEARTS ----------------
def floating_hearts():
    components.html("""
    <style>
    .heart {
        position: fixed;
        bottom: -10px;
        font-size: 24px;
        animation: float 8s infinite;
        color: #ff4b6e;
    }
    @keyframes float {
        0% {transform: translateY(0);}
        100% {transform: translateY(-100vh);}
    }
    </style>
    <script>
    for (let i = 0; i < 15; i++) {
        let h = document.createElement("div");
        h.innerHTML = "💖";
        h.className = "heart";
        h.style.left = Math.random()*100 + "vw";
        h.style.animationDuration = (Math.random()*5 + 5) + "s";
        document.body.appendChild(h);
    }
    </script>
    """, height=0)

floating_hearts()

# ---------------- STATE ----------------
if "stage" not in st.session_state:
    st.session_state.stage = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "music" not in st.session_state:
    st.session_state.music = False

if st.session_state.music:
    play_music()

# ---------------- STYLE ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(#ffe6f0,#fff0f5);
}
.card {
    background:white;
    padding:25px;
    border-radius:20px;
    box-shadow:0px 0px 20px pink;
    text-align:center;
}
.big {
    font-size:38px;
    color:#ff4b6e;
}
button {
    background:#ff4b6e !important;
    color:white !important;
    border-radius:20px !important;
    font-size:18px !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- MUSIC BUTTON ----------------
if st.button("🎵 Play / Pause Music"):
    st.session_state.music = not st.session_state.music

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
    q, options, answer = quiz[st.session_state.stage-1]
    st.markdown(f"<div class='card'><h2>{q}</h2>", unsafe_allow_html=True)

    if not st.session_state.answered:
        for o in options:
            if st.button(o):
                st.session_state.answered = True
                if o == answer:
                    st.session_state.score += 1
                    st.success("Correct 💕")
                else:
                    st.warning("Still loved 😘")

    if st.session_state.answered:
        if st.button("Next ❤️"):
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
    I love you.  
    I cherish you.  
    And I want to hang out with you for the rest of my life. ❤️<br><br>
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

    col1, col2 = st.columns(2)

    with col1:
        if st.button("YES 💕"):
            st.session_state.stage = 7
    with col2:
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
