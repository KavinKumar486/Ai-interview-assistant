import streamlit as st
from streamlit.components.v1 import html

def tab_switch_detector():
    """
    Renders a component that detects tab switches and communicates with Streamlit
    """
    component_html = """
    <div id="tab-detector"></div>
    <script>
        const tabDetector = document.getElementById('tab-detector');
        
        // Function to send tab switch event to Streamlit
        function notifyTabSwitch(switched) {
            if (window.parent && window.parent.postMessage) {
                window.parent.postMessage({
                    type: "streamlit:tabSwitched",
                    switched: switched
                }, "*");
            }
        }
        
        // Listen for visibility changes
        document.addEventListener('visibilitychange', function() {
            if (document.hidden) {
                // User switched away from tab
                sessionStorage.setItem('tabSwitched', 'true');
                notifyTabSwitch(true);
            }
        });
        
        // Check on load if we need to report a switch
        if (sessionStorage.getItem('tabSwitched') === 'true') {
            notifyTabSwitch(true);
        }
        
        // Listen for messages from Streamlit
        window.addEventListener('message', function(event) {
            if (event.data.type === 'streamlit:clearTabSwitch') {
                sessionStorage.removeItem('tabSwitched');
            }
        });
    </script>
    """
    
    component = html(component_html, height=0)
    
    if st.session_state.get('tab_switched', False):
        with st.container():
            st.error("⚠️ Tab switching detected! This would be flagged in a real interview.")
            if st.button("Clear Warning"):
                st.session_state.tab_switched = False
                st.components.v1.html("""
                <script>
                sessionStorage.removeItem('tabSwitched');
                </script>
                """, height=0)
    
    return component