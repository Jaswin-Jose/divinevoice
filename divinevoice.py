import streamlit as st
import requests
import re
st.set_page_config(layout="wide")
st.markdown('<img src="1725431126643.png" style="display: none;">', unsafe_allow_html=True)
def replace_citation(match):
    number = match.group(1)
    return f'<sup>[<a href="#cite-{number}">{number}</a>]</sup>'

st.markdown("""
    <style>
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        margin-top: 100px;
        padding: 1rem;
    }
    .chat-row {
        display: flex;
    }

    .chat-row.user {
        justify-content: flex-end;
    }

    .chat-row.assistant {
        justify-content: flex-start;
    }
    .chat-message {
        max-width: 70%;
        padding: 0.8rem 1.2rem;
        border-radius: 1.5rem;
        font-size: 1rem;
        line-height: 1.4;
        word-wrap: break-word;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }

    .chat-message.user {
        align-self: flex-end;
        background: #dcf2ff;
        color: #000;
        border-bottom-right-radius: 0.3rem;
    }

    .chat-message.assistant {
        align-self: flex-start;
        background: #f1f0f0;
        color: #000;
        border-bottom-left-radius: 0.3rem;
    }
    </style>
    <div class="chat-container">
""", unsafe_allow_html=True)
st.markdown("""
    <style>
    [data-testid="stChatMessageAvatarUser"] {
        background-color: transparent !important;
        background-image: url('static/1725431126643.png');
        background-size: cover;
        background-position: center;
        width: 40px;
        height: 40px;
        border-radius: 50%;
    }

    .st-emotion-cache-13o7eu2,
    .st-emotion-cache-vlxhtx,
    .chat-row.user,
    .chat-row.assistant,
    .st-emotion-cache-1flajlm,
    .st-emotion-cache-1c7y2kd {
        background-color: transparent !important;
        box-shadow: none !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main, .block-container {
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
    }

    .stAppHeader {
        background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
        } 

    .fixed-banner {
        position: fixed;
        top: 20px;
        left: 0;
        width: 100%;
        padding: 1.5rem 1rem;
        background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        z-index: 9999;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }

    .content {
        margin-top: 100px; /* Push content below the fixed banner */
        padding: 1rem;
    }
    
    </style>

    <div class="fixed-banner">Divine Voice</div>
    <div class="content">
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    role = message["role"]
    role_class = "user" if role == "user" else "assistant"
    
    st.markdown(
        f'''
        <div class="chat-row {role_class}">
            <div class="chat-message {role_class}">{message["content"]}</div>
        </div>
        ''',
        unsafe_allow_html=True
    )   

prompt=st.chat_input("Ask anything about the Magisterium")
if prompt:
    with st.chat_message("user"):
        st.markdown(
            f'''
        <div class="chat-row user">
            <div class="chat-message user">{prompt}</div><div class="chat-avatar user"><img src="https://static.vecteezy.com/system/resources/previews/028/794/709/non_2x/cartoon-cute-school-boy-photo.jpg" style="width: 40px; height: 40px; border-radius: 50%;"></div>
        </div>
        ''',
        unsafe_allow_html=True
        )
    st.session_state.messages.append({"role":"user","content":prompt})
    
    api_key=st.secrets["MAGESTERIUM_API_KEY"]
    url = "https://www.magisterium.com/api/v1/chat/completions"
    headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    }
    data = {
    "model": "magisterium-1",
    "messages": st.session_state.messages,
    "stream": False
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    assistant_message = result["choices"][0]["message"]["content"]
    
    styled_message = re.sub(r"\[\^(\d+)\]", replace_citation, assistant_message)

    with st.chat_message("Jesus"):
        st.markdown(
            f'''
        <div class="chat-row assistant">
            <div class="chat-message assistant">{styled_message}</div>
        </div>
        ''',
        unsafe_allow_html=True
        )

        citations = result.get("citations", [])
        if "citations" in result and result["citations"]:
            st.markdown("**Citations:**", unsafe_allow_html=True)
            for i, cite in enumerate(citations, start=1):
                title = cite.get("document_title", "Unknown Title")
                reference = cite.get("document_reference", "")
                source_url = cite.get("source_url", "")
                anchor = f'<a name="cite-{i}"></a>'
                if source_url:
                    st.markdown(
                        f'<p id="cite-{i}"><sup>{i}</sup> <a href="{source_url}" target="_blank">{title} ({reference})</a></p>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<p id="cite-{i}"><sup>{i}</sup> <a href="{source_url}" target="_blank">{title} ({reference})</a></p>',
                        unsafe_allow_html=True
                    )

    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
st.markdown("</div>", unsafe_allow_html=True)
