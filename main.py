import streamlit as st

import llm.ollama.service as ollama

def detect_model_change():
    st.session_state.current_system_prompt = ""
    selected_model = st.session_state.current_model
    if selected_model:
        system_prompt = ollama.get_system_prompt(selected_model)
        st.session_state.current_system_prompt = system_prompt

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