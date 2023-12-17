import streamlit as st

import llm.ollama.service as ollama

# sidebar

def detect_model_change():
    st.session_state["current_system_prompt"] = ""
    selected_model = st.session_state["current_model"]
    if selected_model:
        system_prompt = ollama.get_system_prompt(selected_model)
        st.session_state["current_system_prompt"] = system_prompt

model_selection = st.sidebar.selectbox(
    label="Model:",
    index=None,
    placeholder="Choose a model...",
    options=ollama.list_model_names(),
    key="current_model",
    on_change=detect_model_change
)

system_prompt_text = st.sidebar.text_area(
    label="System prompt:",
    key="current_system_prompt"
)

# chat messages

if "chat" not in st.session_state:
    st.session_state["chat"] = []

if "full_response" not in st.session_state:
    st.session_state["full_response"] = ""

for message in st.session_state["chat"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def print_streamed_response(chunk):
    if not chunk.get("done"):
        st.session_state["full_response"] += chunk.get("response", "")
        st.session_state["placeholder"].markdown(st.session_state["full_response"] + "▌")

if prompt := st.chat_input("Talk to me"):
    st.session_state["chat"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        placeholder = st.empty()
        st.session_state["placeholder"] = placeholder
        st.session_state["full_response"] = ""
        ollama.generate_completion(
            model=st.session_state["current_model"],
            prompt=prompt,
            system=st.session_state["current_system_prompt"],
            callback=print_streamed_response
        )
        placeholder.markdown(st.session_state["full_response"])
    st.session_state["chat"].append({"role": "assistant", "content": st.session_state["full_response"]})