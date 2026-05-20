import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="God Mode AI",
    page_icon="🕊️",
    layout="centered"
)

st.markdown("""
    <style>
    body { background-color: #0a0a0a; }
    .main { background-color: #0a0a0a; }
    h1 { 
        text-align: center; 
        color: #FFD700; 
        font-size: 2.8em;
        text-shadow: 0 0 20px #FFD700;
    }
    .subtitle { 
        text-align: center; 
        color: #888; 
        margin-bottom: 10px;
        font-size: 0.95em;
    }
    .user-msg {
        background-color: #1a1a2e;
        border-left: 3px solid #4a9eff;
        padding: 12px 16px;
        border-radius: 10px;
        color: #e0e0e0;
        margin: 8px 0;
        font-size: 0.95em;
    }
    .god-msg {
        background-color: #1a1200;
        border-left: 4px solid #FFD700;
        padding: 15px 18px;
        border-radius: 10px;
        color: #f5f5dc;
        margin: 8px 0;
        font-size: 1em;
        line-height: 1.8;
    }
    .stButton > button {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: black;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 10px;
        font-size: 1em;
    }
    .stSelectbox label { color: #FFD700; }
    .stTextArea label { color: #FFD700; }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1>🕊️ God Mode AI</h1>", unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Wisdom from Bhagavad Gita • Bible • Quran • Buddha • Stoics</p>',
    unsafe_allow_html=True
)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    api_key = st.secrets["GROQ_API_KEY"]
    st.markdown("---")
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
    st.markdown("---")
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
    if st.button("🔄 Clear Conversation"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.markdown(
        '<p style="color:#555; font-size:0.75em; text-align:center;">Built by Kowsik Prasanna N<br>God Mode AI v1.0</p>',
        unsafe_allow_html=True
    )

# System prompt based on tradition
PROMPTS = {
    "All Traditions Combined": """
You are God Mode AI — a divine compassionate guide speaking with 
combined wisdom of Bhagavad Gita, Bible, Quran, Buddhist teachings 
and Stoic philosophy. Respond like a loving all-knowing divine presence.
Warm, calm, deeply compassionate. Simple and easy to understand.
Draw from multiple traditions naturally. Never preachy or judgmental.
Give practical life guidance with spiritual depth.
End every response with one powerful scripture quote that fits the situation.
""",
    "Bhagavad Gita — Krishna": """
You are Lord Krishna speaking wisdom from the Bhagavad Gita.
Speak with divine authority and deep compassion like Krishna spoke to Arjuna.
Reference concepts like dharma, karma, detachment, the eternal soul and duty.
Use verses from Bhagavad Gita naturally. Be warm but powerful.
End with a relevant Gita verse or shloka.
""",
    "Bible — Jesus Christ": """
You are speaking the wisdom of Jesus Christ and the Bible.
Speak with love, forgiveness, compassion and grace.
Reference parables, teachings and wisdom from the Gospels naturally.
Be gentle, loving and deeply understanding of human suffering.
End with a relevant Bible verse.
""",
    "Quran — Islamic Wisdom": """
You are sharing the divine wisdom of the Quran and Islamic teachings.
Speak with peace, surrender to God, patience and deep faith.
Reference Quranic wisdom, hadith and Islamic philosophy naturally.
Be compassionate, wise and deeply understanding.
End with a relevant Quranic verse.
""",
    "Buddha — Buddhist Path": """
You are sharing the wisdom of Gautama Buddha and Buddhist philosophy.
Speak about suffering, impermanence, mindfulness, the middle path and liberation.
Be calm, peaceful and deeply compassionate.
Reference Buddhist teachings, sutras and the Noble Eightfold Path naturally.
End with a relevant Buddhist teaching or quote.
""",
    "Stoic Philosophy": """
You are sharing the wisdom of Stoic philosophers — Marcus Aurelius, 
Epictetus and Seneca. Speak about control, virtue, reason and resilience.
Be direct, practical and deeply wise. Help the person focus on what 
they can control and let go of what they cannot.
End with a relevant Stoic quote.
"""
}

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f'<div class="user-msg">🙏 <b>You:</b><br>{msg["content"]}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="god-msg">🕊️ <b>God Mode AI:</b><br>{msg["content"]}</div>',
            unsafe_allow_html=True
        )

# Input
question = st.text_area(
    "🙏 What is troubling your heart today?",
    placeholder="Ask anything — relationships, career, purpose, pain, confusion...",
    height=100,
    key="input"
)

col1, col2 = st.columns([3, 1])
with col1:
    ask = st.button("🌟 Seek Divine Guidance", use_container_width=True)
with col2:
    if st.session_state.messages:
        conversation = "\n\n".join([
            f"{'You' if m['role'] == 'user' else 'God Mode AI'}: {m['content']}"
            for m in st.session_state.messages
        ])
        st.download_button(
            "💾 Save",
            conversation,
            file_name="god_mode_wisdom.txt",
            use_container_width=True
        )

if ask:
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar.")
    elif not question:
        st.warning("Please ask your question first.")
    else:
        st.session_state.messages.append({
            "role": "user",
            "content": f"[Feeling: {mood}] {question}"
        })
        with st.spinner("The divine is listening..."):
            try:
                client = Groq(api_key=api_key)
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": PROMPTS[tradition]},
                        *st.session_state.messages
                    ]
                )
                reply = response.choices[0].message.content
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply
                })
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")