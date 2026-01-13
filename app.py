import streamlit as st
import base64
import streamlit.components.v1 as components

st.set_page_config(page_title="Amber ❤️ Osama", layout="centered")

# ---------------- MUSIC ----------------
def autoplay_audio(file_path):
    with open(file_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    components.html(f"""
    <audio autoplay loop>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """, height=0)

# ---------------- STATE ----------------
if "stage" not in st.session_state:
    st.session_state.stage = 0
if "music" not in st.session_state:
    st.session_state.music = False
if "answered" not in st.session_state:
    st.session_state.answered = False
if "score" not in st.session_state:
    st.session_state.score = 0

if st.session_state.music:
    autoplay_audio("music.mp3")

# ---------------- STYLE ----------------
st.markdown("""
<style>
body { background-color:#fff0f5; }
.big { font-size:40px; text-align:center; color:#ff4b4b; }
.center { text-align:center; }
button { width:100%; font-size:18px; margin:8px 0; }
</style>
""", unsafe_allow_html=True)

# ---------------- WELCOME ----------------
if st.session_state.stage == 0:
    st.markdown("<div class='big'>Amber 💕</div>", unsafe_allow_html=True)
    st.markdown("<p class='center'>A love story made just for you 💌</p>", unsafe_allow_html=True)

    if st.button("Start Our Story ❤️"):
        st.session_state.stage = 1
        st.session_state.music = True

# ---------------- QUIZ ----------------
quiz = [
    ("Where did we first meet?",
     ["At university", "In your house", "On the street"],
     "In your house"),

    ("Where did we go for our first date?",
     ["Hyde Park", "V&A museum", "Cinema"],
     "V&A museum"),

    ("Amber, do you like me?",
     ["Maybe", "I love you", "You're okay 😅"],
     "I love you")
]

if 1 <= st.session_state.stage <= 3:
    q, options, answer = quiz[st.session_state.stage - 1]
    st.subheader(q)

    if not st.session_state.answered:
        for opt in options:
            if st.button(opt):
                st.session_state.answered = True
                if opt == answer:
                    st.session_state.score += 1
                    st.success("Correct 💖")
                else:
                    st.warning("Even if you missed it… I still love you 😘")

    if st.session_state.answered:
        if st.button("Next ❤️"):
            st.session_state.stage += 1
            st.session_state.answered = False

    st.markdown("### Love Meter 💕")
    st.progress(st.session_state.score / 3)

# ---------------- UNLOCK ----------------
if st.session_state.stage == 4:
    st.markdown("<div class='big'>Love Meter Full 💞</div>", unsafe_allow_html=True)
    if st.button("Open Your Surprise 💌"):
        st.session_state.stage = 5

# ---------------- LOVE LETTER ----------------
if st.session_state.stage == 5:
    st.balloons()
    st.markdown("<div class='big'>Amber 💖</div>", unsafe_allow_html=True)

    st.markdown("""
    ### 💌 My Valentine Proposal

    Hi baby,

    This is my Valentine’s Day proposal for you.  
    I would be the luckiest man in the world if you could accept my proposal and let me take you on a date.

    I love you.  
    I cherish you.  
    And I want to hang out with you for the rest of my life. ❤️  

    — Osama
    """)
