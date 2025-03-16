# frontend/welcome.py
import streamlit as st
import os
from backend.storage import save_user_details, get_user_details
from backend.models import USER_DETAILS_FILE

def render_welcome_screen():
    """Render the welcome screen with user details form"""
    if "show_welcome" not in st.session_state:
        
        st.session_state.show_welcome = True
    
    if not st.session_state.show_welcome:
        return False
    
    st.title("AI Technical Interview Assistant")
    
    existing_details = get_user_details()
    
    with st.container():
        st.markdown("""
        ## Welcome to your Technical Interview Practice Session!
        
        Please provide some information to personalize your interview experience.
        """)
        
        with st.form("user_details_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Your Name:", value=existing_details.get("name", ""))
            
            with col2:
                experience_level = st.selectbox(
                    "Experience Level:",
                    options=["Entry Level (0-2 years)", "Mid-Level (3-5 years)", "Senior (5+ years)"],
                    index=0 if not existing_details.get("experience_level") else 
                          ["Entry Level (0-2 years)", "Mid-Level (3-5 years)", "Senior (5+ years)"].index(existing_details.get("experience_level"))
                )
            
            tech_stack = st.multiselect(
                "Select your tech stack (up to 5):",
                options=["Python", "JavaScript", "Java", "C#", "C++", "Go", "Ruby", "PHP", "Swift", 
                         "Kotlin", "TypeScript", "React", "Angular", "Vue", "Node.js", "Django", 
                         "Flask", "Spring", "ASP.NET", "Ruby on Rails", "SQL", "NoSQL", "AWS", 
                         "Azure", "GCP", "Docker", "Kubernetes", "Machine Learning", "Data Science"],
                default=existing_details.get("tech_stack", []),
                max_selections=5
            )
            
            other_tech = st.text_input("Other technologies (comma separated):", 
                                      value=existing_details.get("other_tech", ""))
            
            focus_areas = st.multiselect(
                "What areas would you like to focus on?",
                options=["Algorithms", "Data Structures", "System Design", "Database Design", 
                         "Frontend Development", "Backend Development", "DevOps", "Testing", 
                         "Behavioral Questions", "Problem Solving", "Debugging", "Code Review"],
                default=existing_details.get("focus_areas", ["Algorithms", "Data Structures", "Problem Solving"])
            )            
            submitted = st.form_submit_button("Start Interview")
            
            if submitted:
                if not name.strip():
                    st.error("Please enter your name.")
                    return True
                    
                if not tech_stack and not other_tech.strip():
                    st.error("Please select at least one technology from your tech stack.")
                    return True
                
                
                user_details = {
                    "name": name.strip(),
                    "experience_level": experience_level,
                    "tech_stack": tech_stack,
                    "other_tech": other_tech.strip(),
                    "focus_areas": focus_areas,
                    
                }
                save_user_details(user_details)
                st.session_state.user_details = user_details
                
                st.session_state.show_welcome = False
                
                st.session_state.first_question = f"Welcome {name}! Please introduce yourself briefly, highlighting your technical prowess."
                
                st.rerun()
                
    return True