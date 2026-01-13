import streamlit as st
import time
import base64
import streamlit.components.v1 as components

st.set_page_config(page_title="Amber ❤️ Osama", layout="centered")

# ---------------- MUSIC ----------------
def autoplay_audio(file_path):
    with open(file_path, "rb") as f:
        audio_bytes = f.read()
        b64 = base64.b64encode(audio_bytes).decode()

    audio_html = f"""
    <audio id="bgmusic" autoplay loop>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    <script>
    var audio = document.getElementById("bgmusic");
    audio.volume = 0.4;
    </script>
    """
    components.html(audio_html, height=0)

# ---------------- STATE ----------------
if "stage" not in st.session_state:
    st.session_state.stage = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "music" not in st.session_state:
    st.session_state.music = False

if st.session_state.music:
    autoplay_audio("music.mp3")

# ---------------- STYLE ----------------
st.markdown("""
<style>
body { background-color:#fff0f5; }
.big { font-size:42px; text-align:center; color:#ff4b4b; }
.center { text-align:center; }
.option button { width:100%; font-size:18px; margin:5px 0; }
</style>
""", unsafe_allow_html=True)

# ---------------- WELCOME ----------------
if st.session_state.stage == 0:
    st.markdown("<div class='big'>Amber 💕</div>", unsafe_allow_html=True)
    st.markdown("<p class='center'>A little love story made just for you 💌</p>", unsafe_allow_html=True)
    st.markdown("<h1 class='center'>❤️</h1>", unsafe_allow_html=True)

    if st.button("Start Our Story"):
        st.session_state.stage = 1
        st.session_state.music = True
        st.experimental_rerun()

# ---------------- QUESTIONS ----------------
quiz = [
    {
        "q": "Where did we first meet?",
        "options": ["At university", "In your house", "On the street"],
        "answer": "In your house"
    },
    {
        "q": "Where did we go for our first date?",
        "options": ["Hyde Park", "Cinema", "V&A museum"],
        "answer": "V&A museum"
    },
    {
        "q": "Amber, do you like me?",
        "options": ["Maybe", "I love you", "You're okay 😅"],
        "answer": "I love you"
    }
]

if 1 <= st.session_state.stage <= 3:
    qdata = quiz[st.session_state.stage - 1]

    st.subheader(qdata["q"])

    for opt in qdata["options"]:
        if st.button(opt):
            if opt == qdata["answer"]:
                st.session_state.score += 1
                st.success("Correct 💖")
            else:
                st.warning("Even if you missed it… I still love you 😘")

            time.sleep(0.8)
            st.session_state.stage += 1
            st.experimental_rerun()

    st.markdown("### Love Meter 💕")
    st.progress(st.session_state.score / 3)

# ---------------- UNLOCK ----------------
if st.session_state.stage == 4:
    st.markdown("<div class='big'>Love Meter Full 💞</div>", unsafe_allow_html=True)
    if st.button("Open Your Surprise 💌"):
        st.session_state.stage = 5
        st.experimental_rerun()

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
