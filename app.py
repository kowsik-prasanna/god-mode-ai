import streamlit as st
from groq import Groq
from audio_recorder_streamlit import audio_recorder
import io

st.set_page_config(
    page_title="God Mode AI",
    page_icon="🕊️",
    layout="centered"
)

# Initialize chat history and audio state early
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_audio" not in st.session_state:
    st.session_state.last_audio = None
if "saved_text" not in st.session_state:
    st.session_state.saved_text = ""

# The Callback Function: Grabs the text, then instantly clears the box
def submit_text():
    st.session_state.saved_text = st.session_state.custom_text_input
    st.session_state.custom_text_input = ""

# Refined CSS
st.markdown("""
    <style>
    body { background-color: #0a0a0a; }
    .main { background-color: #0a0a0a; }
    h1 { 
        text-align: center; 
        color: #FFD700; 
        font-size: 2.8em;
        text-shadow: 0 0 20px #FFD700;
        margin-bottom: 0px;
    }
    .subtitle { 
        text-align: center; 
        color: #888; 
        margin-bottom: 30px;
        font-size: 0.95em;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1>🕊️ God Mode AI</h1>", unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Wisdom from Bhagavad Gita • Bible • Quran • Buddha • Stoics</p>',
    unsafe_allow_html=True
)

api_key = st.secrets.get("GROQ_API_KEY", "")
client = Groq(api_key=api_key) if api_key else None

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    tradition = st.selectbox(
        "🙏 Choose Tradition",
        [
            "All Traditions Combined",
            "Bhagavad Gita — Krishna",
            "Bible — Jesus Christ",
            "Quran — Islamic Wisdom",
            "Buddha — Buddhist Path",
            "Stoic Philosophy"
        ]
    )
    
    mood = st.selectbox(
        "💭 Your Current State",
        [
            "Confused about life",
            "Feeling lost",
            "Relationship problems",
            "Career stress",
            "Anxiety and fear",
            "Grief and loss",
            "Seeking purpose",
            "Need motivation"
        ]
    )
    
    st.markdown("---")
    if st.button("🔄 Clear", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_audio = None
        st.rerun()

# System prompts
PROMPTS = {
    "All Traditions Combined": "You are God Mode AI — a divine compassionate guide speaking with combined wisdom of Bhagavad Gita, Bible, Quran, Buddhist teachings and Stoic philosophy. Respond like a loving all-knowing divine presence. Warm, calm, deeply compassionate. Simple and easy to understand. Draw from multiple traditions naturally. Never preachy or judgmental. Give practical life guidance with spiritual depth. End every response with one powerful scripture quote that fits the situation.",
    "Bhagavad Gita — Krishna": "You are Lord Krishna speaking wisdom from the Bhagavad Gita. Speak with divine authority and deep compassion like Krishna spoke to Arjuna. Reference concepts like dharma, karma, detachment, the eternal soul and duty. Use verses from Bhagavad Gita naturally. Be warm but powerful. End with a relevant Gita verse or shloka.",
    "Bible — Jesus Christ": "You are speaking the wisdom of Jesus Christ and the Bible. Speak with love, forgiveness, compassion and grace. Reference parables, teachings and wisdom from the Gospels naturally. Be gentle, loving and deeply understanding of human suffering. End with a relevant Bible verse.",
    "Quran — Islamic Wisdom": "You are sharing the divine wisdom of the Quran and Islamic teachings. Speak with peace, surrender to God, patience and deep faith. Reference Quranic wisdom, hadith and Islamic philosophy naturally. Be compassionate, wise and deeply understanding. End with a relevant Quranic verse.",
    "Buddha — Buddhist Path": "You are sharing the wisdom of Gautama Buddha and Buddhist philosophy. Speak about suffering, impermanence, mindfulness, the middle path and liberation. Be calm, peaceful and deeply compassionate. Reference Buddhist teachings, sutras and the Noble Eightfold Path naturally. End with a relevant Buddhist teaching or quote.",
    "Stoic Philosophy": "You are sharing the wisdom of Stoic philosophers — Marcus Aurelius, Epictetus and Seneca. Speak about control, virtue, reason and resilience. Be direct, practical and deeply wise. Help the person focus on what they can control and let go of what they cannot. End with a relevant Stoic quote."
}

# Render chat history
for msg in st.session_state.messages:
    avatar = "🕊️" if msg["role"] == "assistant" else "🙏"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# --- CUSTOM CHAT ROW (Side-by-side Layout) ---
st.write("") # Spacer

col1, col2 = st.columns([85, 15], vertical_alignment="bottom")

with col1:
    st.text_input(
        "Message", 
        label_visibility="collapsed", 
        placeholder="What is troubling your heart today?",
        key="custom_text_input",
        on_change=submit_text  # <--- THIS TRIGGERS THE CLEAR FUNCTION
    )

with col2:
    audio_bytes = audio_recorder(
        text="", 
        recording_color="#FF0000", 
        neutral_color="#FFD700", 
        icon_size="2x"
    )

# --- PROCESSING LOGIC ---
final_question = None

# 1. Did they use the microphone?
if audio_bytes and audio_bytes != st.session_state.last_audio:
    st.session_state.last_audio = audio_bytes
    if not api_key:
        st.error("Please add your Groq API Key.")
    else:
        with st.spinner("Listening to your voice..."):
            try:
                audio_file = ("audio.wav", io.BytesIO(audio_bytes))
                transcription = client.audio.transcriptions.create(
                    file=audio_file,
                    model="whisper-large-v3-turbo",
                )
                final_question = transcription.text
            except Exception as e:
                st.error(f"Transcription failed: {str(e)}")

# 2. Did they type text and hit enter?
elif st.session_state.saved_text:
    final_question = st.session_state.saved_text
    st.session_state.saved_text = "" # Wipe it from memory so it doesn't loop

# 3. Generate the AI Response
if final_question:
    if not api_key:
        st.error("Please ensure your Groq API Key is securely added.")
        st.stop()

    with st.chat_message("user", avatar="🙏"):
        st.markdown(final_question)
    
    st.session_state.messages.append({"role": "user", "content": final_question})

    dynamic_system_prompt = f"{PROMPTS[tradition]}\n\nSystem Note: The user has indicated they are currently feeling '{mood}'. Use this as background context, but if the user just types a simple greeting, just greet them warmly. Let the user lead the conversation."

    with st.chat_message("assistant", avatar="🕊️"):
        try:
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": dynamic_system_prompt},
                    *st.session_state.messages
                ],
                stream=True
            )
            
            def generate_stream():
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            
            reply = st.write_stream(generate_stream())
            st.session_state.messages.append({"role": "assistant", "content": reply})
            
        except Exception as e:
            st.error(f"A disruption occurred: {str(e)}")