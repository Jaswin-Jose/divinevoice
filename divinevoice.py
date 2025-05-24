import streamlit as st
import requests
import re
def replace_citation(match):
    number = match.group(1)
    return f'<sup>[<a href="#cite-{number}">{number}</a>]</sup>'

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
    
    styled_message = re.sub(r"\[\^(\d+)\]", replace_citation, assistant_message)

    with st.chat_message("Jesus"):
        st.markdown(assistant_message)

        citations = result.get("citations", [])
        if "citations":
            st.markdown("**Citations:**", unsafe_allow_html=True)
        for i, cite in enumerate(citations, start=1):
            title = cite.get("document_title", "Unknown Title")
            reference = cite.get("document_reference", "")
            source_url = cite.get("source_url", "")
            anchor = f'<a name="cite-{i}"></a>'
            if source_url:
                st.markdown(
                    f'{anchor}**[{i}]** [{title} (Ref {reference})]({source_url})',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'{anchor}**[{i}]** {title} (Ref {reference})',
                    unsafe_allow_html=True
                )

    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
