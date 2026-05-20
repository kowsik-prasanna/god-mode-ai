import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="God Mode AI",
    page_icon="🕊️",
    layout="centered"
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Refined CSS: Kept your beautiful header styling, but let Streamlit handle 
# the chat bubbles natively for a smoother, modern feel.
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
    /* Style the native Streamlit chat input */
    [data-testid="stChatInput"] {
        border-color: #FFD700 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1>🕊️ God Mode AI</h1>", unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Wisdom from Bhagavad Gita • Bible • Quran • Buddha • Stoics</p>',
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    api_key = st.secrets.get("GROQ_API_KEY", "")
    
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
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Clear", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.session_state.messages:
            conversation = "\n\n".join([
                f"{'You' if m['role'] == 'user' else 'God Mode AI'}: {m['content']}"
                for m in st.session_state.messages
            ])
            st.download_button("💾 Save", conversation, file_name="god_mode_wisdom.txt", use_container_width=True)
            
    st.markdown("---")
    st.markdown(
        '<p style="color:#555; font-size:0.75em; text-align:center;">Built by Kowsik Prasanna N<br>God Mode AI v1.1</p>',
        unsafe_allow_html=True
    )

# System prompts
PROMPTS = {
    "All Traditions Combined": "You are God Mode AI — a divine compassionate guide speaking with combined wisdom of Bhagavad Gita, Bible, Quran, Buddhist teachings and Stoic philosophy. Respond like a loving all-knowing divine presence. Warm, calm, deeply compassionate. Simple and easy to understand. Draw from multiple traditions naturally. Never preachy or judgmental. Give practical life guidance with spiritual depth. End every response with one powerful scripture quote that fits the situation.",
    "Bhagavad Gita — Krishna": "You are Lord Krishna speaking wisdom from the Bhagavad Gita. Speak with divine authority and deep compassion like Krishna spoke to Arjuna. Reference concepts like dharma, karma, detachment, the eternal soul and duty. Use verses from Bhagavad Gita naturally. Be warm but powerful. End with a relevant Gita verse or shloka.",
    "Bible — Jesus Christ": "You are speaking the wisdom of Jesus Christ and the Bible. Speak with love, forgiveness, compassion and grace. Reference parables, teachings and wisdom from the Gospels naturally. Be gentle, loving and deeply understanding of human suffering. End with a relevant Bible verse.",
    "Quran — Islamic Wisdom": "You are sharing the divine wisdom of the Quran and Islamic teachings. Speak with peace, surrender to God, patience and deep faith. Reference Quranic wisdom, hadith and Islamic philosophy naturally. Be compassionate, wise and deeply understanding. End with a relevant Quranic verse.",
    "Buddha — Buddhist Path": "You are sharing the wisdom of Gautama Buddha and Buddhist philosophy. Speak about suffering, impermanence, mindfulness, the middle path and liberation. Be calm, peaceful and deeply compassionate. Reference Buddhist teachings, sutras and the Noble Eightfold Path naturally. End with a relevant Buddhist teaching or quote.",
    "Stoic Philosophy": "You are sharing the wisdom of Stoic philosophers — Marcus Aurelius, Epictetus and Seneca. Speak about control, virtue, reason and resilience. Be direct, practical and deeply wise. Help the person focus on what they can control and let go of what they cannot. End with a relevant Stoic quote."
}



# Render chat history using native Streamlit chat components
for msg in st.session_state.messages:
    avatar = "🕊️" if msg["role"] == "assistant" else "🙏"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Native Chat Input
if question := st.chat_input("What is troubling your heart today?"):
    if not api_key:
        st.error("Please ensure your Groq API Key is securely added.")
        st.stop()

    # Display user message instantly
    with st.chat_message("user", avatar="🙏"):
        st.markdown(question)
    
    # Add to session state
    st.session_state.messages.append({"role": "user", "content": question})

    # Dynamically inject the mood into the system prompt (invisible to user UI)
    dynamic_system_prompt = f"{PROMPTS[tradition]}\n\nSystem Note: The user has indicated they are currently feeling '{mood}'. Use this as background context, but if the user just types a simple greeting (like 'hi' or 'hello'), just greet them warmly and ask how you can guide them. Let the user lead the conversation."

    # Streaming the response
    with st.chat_message("assistant", avatar="🕊️"):
        try:
            client = Groq(api_key=api_key)
            
            # Create a generator for the stream
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": dynamic_system_prompt},
                    *st.session_state.messages
                ],
                stream=True # <--- This enables real-time typing
            )
            
            # Helper function to parse Groq chunks
            def generate_stream():
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            
            # write_stream creates the beautiful typing effect
            reply = st.write_stream(generate_stream())
            
            # Save the final text to state
            st.session_state.messages.append({"role": "assistant", "content": reply})
            
        except Exception as e:
            st.error(f"A disruption occurred in the connection: {str(e)}")