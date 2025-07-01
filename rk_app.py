import streamlit as st
import pyttsx3
import wikipedia
import speech_recognition as sr
import os
import random  # Needed for fun fact mode and cricket game

# ------------------- Voice Input -------------------
def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        st.success(f"🗣️ You said: {text}")
        return text
    except sr.UnknownValueError:
        st.error("❌ Could not understand your voice.")
    except sr.RequestError:
        st.error("⚠️ Connection error with speech service.")
    return ""

# ------------------- Wikipedia Summary -------------------
def get_summary(topic):
    try:
        results = wikipedia.search(topic)
        if not results:
            return "❌ No results found for that topic."
        best_title = results[0]
        page = wikipedia.page(best_title)
        return page.summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"⚠️ Topic '{topic}' has multiple meanings. Try: {e.options[0]}"
    except wikipedia.exceptions.PageError:
        return "❌ Page not found. Try another topic."
    except Exception as e:
        return f"⚠️ Error: {e}"

# ------------------- Duo Voice Podcast Generator -------------------
def speak_duo_conversation(topic, summary):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    voice_a = voices[0].id
    voice_b = voices[1].id if len(voices) > 1 else voices[0].id

    conversation = [
        f"A: Hey, have you heard about {topic}?",
        f"B: Yes! {topic} is really fascinating.",
        f"A: Here's something interesting — {summary.split('.')[0]}.",
        f"B: Wow! And also — {summary.split('.')[1]}.",
        f"A: That’s really impressive.",
        f"B: For sure! {summary.split('.')[2]}.",
        f"A: Glad we talked about this today.",
        f"B: See you next time on RK AI Podcast!"
    ]
    audio_files = []
    for i, line in enumerate(conversation):
        speaker = "A" if line.startswith("A:") else "B"
        voice = voice_a if speaker == "A" else voice_b
        engine.setProperty('voice', voice)
        text = line.replace("A:", "").replace("B:", "").strip()
        file_path = f"line_{i}.mp3"
        engine.save_to_file(text, file_path)
        engine.runAndWait()
        audio_files.append(file_path)

    return audio_files

# 🎥 Talking character GIFs
gif_a = "https://media.giphy.com/media/3oriO0OEd9QIDdllqo/giphy.gif"  # Speaker A
gif_b = "https://media.giphy.com/media/xT5LMsptX4WbiG9zGM/giphy.gif"  # Speaker B

# ------------------- Fun Fact Mode -------------------
def fun_fact_mode():
    st.markdown("## 📚 Fun Fact Mode for Kids")

    category = st.selectbox("🔍 Choose a category", ["🐾 Animals", "🌌 Space", "🇮🇳 India"])

    facts_dict = {
        "🐾 Animals": [
            "🐘 An elephant's trunk has over 40,000 muscles!",
            "🦒 Giraffes have the same number of neck bones as humans!",
            "🐧 Penguins can't fly, but they are great swimmers!",
            "🐝 Bees have 5 eyes and can recognize human faces!",
            "🐊 Crocodiles can't stick their tongues out!"
        ],
        "🌌 Space": [
            "🌌 There are more stars in space than grains of sand on Earth.",
            "🌋 The tallest volcano in the solar system is on Mars.",
            "🪐 Saturn could float in water because it's so light!",
            "🌕 Moonquakes can happen on the Moon!",
            "🚀 A day on Venus is longer than a year on Venus!"
        ],
        "🇮🇳 India": [
            "🇮🇳 The Indian flag was first hoisted in 1906 in Kolkata.",
            "🧵 India is the world's largest producer of spices.",
            "🚀 ISRO launched 104 satellites in one go in 2017!",
            "🎓 Takshashila was one of the world's first universities.",
            "🧠 APJ Abdul Kalam was known as the 'Missile Man of India'."
        ]
    }

    if st.button("🎲 Show Me a Fun Fact!"):
        fact = random.choice(facts_dict[category])
        st.success(f"💡 {fact}")

# ------------------- Offline Cricket Game for Kids -------------------
def cricket_game():
    st.markdown("## 🏏 Play 'Hit the Runs!' - Offline Cricket Game")

    if "score" not in st.session_state:
        st.session_state.score = 0
        st.session_state.out = False

    if not st.session_state.out:
        if st.button("🏏 Bat!"):
            result = random.choice([0, 1, 2, 4, 6, "OUT"])
            if result == "OUT":
                st.session_state.out = True
                st.warning(f"💥 You got OUT! Final Score: {st.session_state.score}")
            else:
                st.session_state.score += result
                st.success(f"🏆 You hit {result} run(s)! Total Score: {st.session_state.score}")
    else:
        st.info(f"🔁 Game Over! Final Score: {st.session_state.score}")
        if st.button("🔄 Restart Game"):
            st.session_state.score = 0
            st.session_state.out = False

# ------------------- Main Streamlit App -------------------
def main():
    st.set_page_config(page_title="🎙️ RK AI Voice Podcast", layout="centered")

    # ✅ Background and style
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background-image: url("https://images.unsplash.com/photo-1503264116251-35a269479413");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
        [data-testid="stAppViewContainer"]::before {
            content: "";
            position: fixed;
            top: 0; left: 0;
            width: 100vw; height: 100vh;
            background: rgba(0, 0, 0, 0.6);
            z-index: 0;
        }
        .main-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 16px;
            backdrop-filter: blur(10px);
            position: relative;
            z-index: 1;
            max-width: 750px;
            margin: 40px auto;
        }
        h1, h2, h3, p, label, .stRadio > div, .stMarkdown {
            color: white !important;
        }
        .stTextInput input {
            font-size: 18px !important;
            padding: 10px !important;
            background-color: #ffffff10;
            color: #000000!important;
        }
        .stButton>button {
            font-size: 18px;
            padding: 10px 20px;
            border-radius: 8px;
            background-color: #4285F4;
            color: white;
            border: none;
        }
        iframe {
            border-radius: 12px;
        }
        </style>
    """, unsafe_allow_html=True)

    # 🧠 Content card
    with st.container():
        st.markdown("""<div class='main-card'>""", unsafe_allow_html=True)

        st.markdown("""
            <h1 style='text-align:center; font-size: 38px; font-family: Google Sans;'>
                <span style='color:#4285F4;'>R</span>
                <span style='color:#DB4437;'>K</span>
                <span style='color:#F4B400;'>A</span>
                <span style='color:#0F9D58;'>I</span> 🔍
            </h1>
            <p style='text-align:center; font-size:18px;'>Your Personal Story-to-Podcast Assistant</p>
        """, unsafe_allow_html=True)

        st.markdown("""
            <h2 style='text-align:left; font-size: 28px; font-weight: 600; font-family: Google Sans;'>
                🔎 <span style='color:#4285F4;'>C</span>
                <span style='color:#DB4437;'>h</span>
                <span style='color:#F4B400;'>o</span>
                <span style='color:#0F9D58;'>o</span>
                <span style='color:#4285F4;'>s</span>
                <span style='color:#DB4437;'>e</span>
                <span style='color:white;'> Input Type</span>
            </h2>
        """, unsafe_allow_html=True)

        mode = st.radio("Input Mode:", ["🎤 Voice", "⌨️ Text"], horizontal=True)

        if mode == "🎤 Voice":
            if st.button("🎧 Start Listening"):
                topic = get_voice_input()
            else:
                topic = ""
        else:
            topic = st.text_input("ENTER TOPIC ").strip().title()

        st.markdown("</div>", unsafe_allow_html=True)

    # 🎙️ Story + Podcast
    if topic:
        summary = get_summary(topic)

        if "❌" not in summary and "⚠️" not in summary:
            st.markdown("## 📖 Wikipedia Story Summary")
            st.write(summary)

            st.markdown("## 👥 Animated Podcast with Talking Characters")
            audio_files = speak_duo_conversation(topic, summary)

            for i, audio in enumerate(audio_files):
                speaker = "A" if i % 2 == 0 else "B"
                col1, col2 = st.columns(2)

                with col1:
                    if speaker == "A":
                        st.image(gif_a, width=250, caption="🎙️ Speaker A is talking...")
                    else:
                        st.image("https://via.placeholder.com/250?text=Speaker+A", width=250)

                with col2:
                    if speaker == "B":
                        st.image(gif_b, width=250, caption="🎙️ Speaker B is talking...")
                    else:
                        st.image("https://via.placeholder.com/250?text=Speaker+B", width=250)

                st.audio(audio, format="audio/mp3")
                st.markdown("---")
        else:
            st.error(summary)

    # 📚 Fun Fact Mode
    with st.expander("📚 Fun Fact Mode"):
        fun_fact_mode()

    # 🏏 Offline Cricket Game
    with st.expander("🏏 Offline Cricket Game"):
        cricket_game()

# 🚀 Run
if __name__ == "__main__":
    main()
