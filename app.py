import streamlit as st
import time
import base64

st.set_page_config(page_title="Amber ❤️ Osama", layout="centered")

# --- Background music ---
def play_music():
    with open("music.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(
            f"""
            <audio autoplay loop>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """,
            unsafe_allow_html=True,
        )

play_music()

# --- Session state ---
if "stage" not in st.session_state:
    st.session_state.stage = 0
if "score" not in st.session_state:
    st.session_state.score = 0

# --- Styling ---
st.markdown("""
<style>
body {
    background-color: #fff0f5;
}
.big {
    font-size: 40px;
    text-align: center;
    color: #ff4b4b;
}
.heart {
    font-size: 60px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# --- Welcome Screen ---
if st.session_state.stage == 0:
    st.markdown("<div class='big'>Welcome Amber 💕</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>This is a little love story made just for you 💌</p>", unsafe_allow_html=True)
    st.markdown("<div class='heart'>❤️</div>", unsafe_allow_html=True)
    if st.button("Start Our Story"):
        st.session_state.stage = 1

# --- Quiz Questions ---
questions = [
    ("Where did we first meet?", "In your house"),
    ("Where did we go for our first date?", "V&A museum"),
    ("Amber, do you like me?", "I love you")
]

if 1 <= st.session_state.stage <= 3:
    q, a = questions[st.session_state.stage - 1]
    st.subheader(q)
    user_answer = st.text_input("Your answer")

    if st.button("Submit"):
        if user_answer.strip().lower() == a.lower():
            st.success("Correct! 💖")
            st.session_state.score += 1
        else:
            st.warning("Even if you missed it… I still love you 😘")
        time.sleep(1)
        st.session_state.stage += 1

    st.progress(st.session_state.score / 3)

# --- Secret Message Unlock ---
if st.session_state.stage == 4:
    st.markdown("<div class='big'>Love Meter Full 💕</div>", unsafe_allow_html=True)
    if st.button("Open Your Surprise 💌"):
        st.session_state.stage = 5

# --- Love Letter ---
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
