import streamlit as st
import requests

st.title("Divine Voice")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt=st.chat_input("Ask anything about the Magisterium")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
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
    with st.chat_message("Jesus"):
        st.markdown(assistant_message)

        if "citation" in result and result["citation"]:
            with st.expander("Citation", expanded=False):
                for cite in result["citations"]:
                    st.markdown(f"**{cite['document_title']}** (Ref {cite['document_reference']}): {cite['cited_text']}")

    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
