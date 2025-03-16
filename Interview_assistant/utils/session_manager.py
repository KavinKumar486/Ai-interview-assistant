import streamlit as st
from backend.storage import load_chat_history
from backend.llm_handler import create_llm_chain
import time

def initialize_session():
    if "question_count" not in st.session_state:
        st.session_state.question_count = 0
    
    if "interview_started" not in st.session_state:
        st.session_state.interview_started = False
    
    if "interview_completed" not in st.session_state:
        st.session_state.interview_completed = False
    
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()
    
    if "history" not in st.session_state:
        st.session_state.history = []
    
    if "difficulty" not in st.session_state:
        st.session_state.difficulty = 0
    
    if "processing" not in st.session_state:
        st.session_state.processing = False
        
    if "first_question" not in st.session_state:
        st.session_state.first_question = "Welcome to your technical interview! Please introduce yourself briefly, including your background and technical experience."
    
    if "tab_visible" not in st.session_state:
        st.session_state.tab_visible = True
    
    if "llm" not in st.session_state:
        try:
            st.session_state.llm_chain = create_llm_chain()
        except Exception as e:
            st.error(f"Error initializing LLM: {str(e)}")