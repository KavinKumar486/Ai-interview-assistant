import streamlit as st
from frontend.ui import render_chat_interface
from frontend.styles import apply_dark_theme
from frontend.welcome import render_welcome_screen
from utils.session_manager import initialize_session
from backend.processors import process_user_input, generate_next_question
from backend.storage import clear_chat_history, get_user_details

def main():
    st.set_page_config(
        page_title="AI Technical Interview Assistant",
        page_icon="🧑‍💻",
        layout="wide",
    )
    
    initialize_session()
    apply_dark_theme()
    
    if "show_welcome" not in st.session_state:
        st.session_state.show_welcome = True
    
    if render_welcome_screen():
        return
    
    tab_state = st.empty()
    tab_state.markdown("""
    <div id="tab-state-reporter"></div>
    <script>
        // Function to update tab state and notify Streamlit
        function updateTabState() {
            const isHidden = document.hidden;
            const state = isHidden ? 'hidden' : 'visible';
            document.getElementById('tab-state-reporter').setAttribute('data-state', state);
            
            // Store state in sessionStorage
            sessionStorage.setItem('tabState', state);
            
            // If tab is hidden, mark as switched
            if (isHidden) {
                sessionStorage.setItem('tabSwitched', 'true');
                
                // Add warning class to app container
                const appContainer = document.querySelector('.stApp');
                if (appContainer) {
                    appContainer.classList.add('warning-active');
                }
                
                // Show warning text
                const warningText = document.getElementById('tab-warning');
                if (warningText) {
                    warningText.classList.add('visible');
                }
                
                // Notify Streamlit about the switch
                if (window.parent && window.parent.postMessage) {
                    window.parent.postMessage({
                        type: "streamlit:tabSwitched",
                        value: true
                    }, "*");
                }
            }
        }
        
        document.addEventListener('visibilitychange', updateTabState);
        
        updateTabState();
        
        window.addEventListener('load', function() {
            if (sessionStorage.getItem('tabSwitched') === 'true') {
                // Show warning text
                const warningText = document.getElementById('tab-warning');
                if (warningText) {
                    warningText.classList.add('visible');
                }
                
                // Add warning class to app container
                const appContainer = document.querySelector('.stApp');
                if (appContainer) {appContainer.classList.add('warning-active');
                }
                
                // Set Streamlit session state through rerun
                if (window.parent && window.parent.postMessage) {
                    window.parent.postMessage({
                        type: "streamlit:tabSwitched",
                        value: true
                    }, "*");
                }
            }
        });
    </script>
    """, unsafe_allow_html=True)
    
    
    user_details = st.session_state.get("user_details", get_user_details())
    name = user_details.get("name", "Candidate")
    
    with st.sidebar:
        st.markdown(f"<h2 style='color: white;'>Welcome, {name}</h2>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: white;'>Interview Controls</h3>", unsafe_allow_html=True)
        
        question_count = st.session_state.get("question_count", 0)
        st.markdown(f"<p style='color: #AAA;'>Questions completed: {question_count}/10</p>", unsafe_allow_html=True)
        
        if st.session_state.get("interview_completed", False):
            if st.button("New Interview"):
                st.session_state.history = []
                st.session_state.question_count = 0
                st.session_state.difficulty = 0
                st.session_state.interview_completed = False
                st.session_state.processing = False
                clear_chat_history()
                st.rerun()
        
        if user_details:
            tech_stack = user_details.get("tech_stack", [])
            other_tech = user_details.get("other_tech", "").split(",")
            other_tech = [t.strip() for t in other_tech if t.strip()]
            
            all_tech = tech_stack + other_tech
            if all_tech:
                st.markdown("<p style='color: #AAA;'>Your technologies:</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: white;'>{', '.join(all_tech)}</p>", unsafe_allow_html=True)
            
            focus_areas = user_details.get("focus_areas", [])
            if focus_areas:
                st.markdown("<p style='color: #AAA;'>Focus areas:</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: white;'>{', '.join(focus_areas)}</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
       
        with col2:
            if st.button("Change Details"):
                st.session_state.show_welcome = True
                st.rerun()
        
        st.markdown("<h3 style='color: white; margin-top: 30px;'>Interview Integrity</h3>", unsafe_allow_html=True)
        
        check_switch_js = """
        <script>
        if (sessionStorage.getItem('tabSwitched') === 'true') {
            if (window.parent && window.parent.postMessage) {
                window.parent.postMessage({
                    type: "streamlit:tabSwitched",
                    value: true
                }, "*");
            }
        }
        </script>
        """
        st.markdown(check_switch_js, unsafe_allow_html=True)
        
        
        if st.session_state.get('tab_switched', False):
            st.error("⚠️ Tab switching detected! This would be flagged in a real interview.")
            if st.button("Clear Warning"):
                st.session_state.tab_switched = False
                st.markdown("""
                <script>
                sessionStorage.removeItem('tabSwitched');
                const appContainer = document.querySelector('.stApp');
                if (appContainer) {
                    appContainer.classList.remove('warning-active');
                }
                const warningText = document.getElementById('tab-warning');
                if (warningText) {
                    warningText.classList.remove('visible');
                }
                </script>
                """, unsafe_allow_html=True)
    
    render_chat_interface()
    
    handle_messages_js = """
    <script>
    // Listen for messages from Streamlit components
    window.addEventListener('message', function(event) {
        if (event.data.type === 'streamlit:tabSwitched' && event.data.value === true) {
            if (window.parent && window.parent.postMessage) {
                window.parent.postMessage({
                    type: "streamlit:setComponentValue",
                    value: true
                }, "*");
            }
        }
    });
    </script>
    """
    st.markdown(handle_messages_js, unsafe_allow_html=True)

if __name__ == "__main__":
    main()