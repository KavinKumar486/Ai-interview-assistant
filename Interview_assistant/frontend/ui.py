import streamlit as st
from backend.processors import process_user_input, generate_next_question
from backend.storage import clear_chat_history

def render_chat_interface():
    
    st.title("AI Technical Interview Assistant")
    
    st.markdown("""
    <div id="tab-warning" class="warning-text">
        Warning: You switched away from this tab during the interview. 
        This could be considered cheating in a real interview situation.
        <button id="acknowledge-btn" style="background-color: #ff4040; color: white; border: none; padding: 5px 10px; margin-left: 10px; border-radius: 4px;">Acknowledge</button>
    </div>
    """, unsafe_allow_html=True)
    
    question_count = st.session_state.get("question_count", 0)
    progress_text = f"Question {question_count}/10" if question_count > 0 else "Interview Starting"
    
    st.markdown(f"""
    <div style="margin-bottom: 10px; color: #AAA;">
        <span>{progress_text}</span>
        <div style="background-color: #2D2D2D; height: 6px; border-radius: 3px; margin-top: 5px; width: 100%;">
            <div style="background-color: #2C5EF7; height: 6px; border-radius: 3px; width: {min(question_count * 10, 100)}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container" style="height: 40vh; margin-top: 20px;">', unsafe_allow_html=True)
        
        if not st.session_state.history:
            st.markdown(f"""
            <div class='chat-bubble ai-bubble'>{st.session_state.first_question}</div>
            """, unsafe_allow_html=True)
        
        for chat in st.session_state.history:
            if chat['origin'] == 'human':
                st.markdown(f"""
                <div class='human-container'>
                    <div class='chat-bubble human-bubble'>{chat['message']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='margin-bottom: 20px;'>
                    <div class='chat-bubble ai-bubble'>{chat['message']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        if st.session_state.processing:
            st.markdown("""
            <div class="thinking-container">
                <div class="thinking-dot"></div>
                <div class="thinking-dot"></div>
                <div class="thinking-dot"></div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.processing:
        generate_next_question()
        st.rerun()
    
    if not st.session_state.get("interview_completed", False):
        with st.container():
            with st.form("chat-form", clear_on_submit=True):
                st.text_area("Your response:", key="user_input", height=100)
                cols = st.columns([1, 1, 4])
                with cols[0]:
                    submit = st.form_submit_button("Submit", use_container_width=True)
                with cols[1]:
                    difficulty_indicator = st.session_state.difficulty
                
                if submit:
                    process_user_input()
    else:
        if st.button("New Interview", key="new_interview"):
            st.session_state.history = []
            st.session_state.question_count = 0
            st.session_state.difficulty = 0
            st.session_state.interview_completed = False
            st.session_state.processing = False
            clear_chat_history()
            st.rerun()