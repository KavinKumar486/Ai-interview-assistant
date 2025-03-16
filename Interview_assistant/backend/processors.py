import re
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from backend.storage import save_chat_history

def extract_keywords(response):
    """Extract the top 3 keywords from a text response"""
    if not response or len(response.strip()) < 5:
        return []
    
    try:
        vectorizer = TfidfVectorizer(stop_words='english', min_df=1)
        tfidf_matrix = vectorizer.fit_transform([response])
        
        if len(vectorizer.get_feature_names_out()) == 0:
            return []
            
        feature_array = vectorizer.get_feature_names_out()
        tfidf_scores = tfidf_matrix.toarray()[0]
        
        num_keywords = min(3, len(feature_array))
        if num_keywords == 0:
            return []
            
        keywords = [feature_array[i] for i in tfidf_scores.argsort()[-num_keywords:][::-1]]
        return keywords
    except ValueError:
        return []

def process_user_input():
    """Process user input and add to history"""
    user_query = st.session_state.user_input.strip()
    if not user_query:
        return
    
    st.session_state.history.append({"origin": "human", "message": user_query})
    
    st.session_state.processing = True
    
    st.rerun()

def generate_next_question():
    """Generate the next interview question based on user's previous response"""
    if not st.session_state.processing:
        return
        
    last_user_message = next((msg["message"] for msg in reversed(st.session_state.history) 
                             if msg["origin"] == "human"), "")
    
    if not last_user_message:
        return
    
    if "question_count" not in st.session_state:
        st.session_state.question_count = 1 
    else:
        st.session_state.question_count += 1
    
    if st.session_state.question_count >= 10:
        thank_you_message = generate_interview_conclusion()
        st.session_state.history.append({"origin": "ai", "message": thank_you_message})
        st.session_state.interview_completed = True
        st.session_state.processing = False
        save_chat_history(st.session_state.history)
        return
    
    try:
        extracted_keywords = extract_keywords(last_user_message)
        difficulty = st.session_state.difficulty
        
        is_first_response = len([msg for msg in st.session_state.history if msg["origin"] == "human"]) == 1
        
        if is_first_response:
            followup_query = f"The candidate just introduced themselves. Ask them about a specific technical challenge they've faced."
        elif not extracted_keywords:
            followup_query = f"Generate a technical interview question at difficulty level {difficulty}/5. Focus on problem-solving skills."
        else:
            followup_query = f"The candidate mentioned {', '.join(extracted_keywords)}. Generate a relevant follow-up question at difficulty level {difficulty}/5."
        
        followup_question = st.session_state.llm_chain.invoke({"input": followup_query})
      
        followup_question = re.sub(r'^(Follow-up Question:|Question:)\s*', '', followup_question).strip()
        
        st.session_state.history.append({"origin": "ai", "message": followup_question})
        
        if not is_first_response:
            st.session_state.difficulty += 0.3
        
        save_chat_history(st.session_state.history)
    except Exception as e:
        print(f"Error generating question: {str(e)}")
        fallback_question = "Tell me about a challenging technical problem you've solved recently. What was your approach?"
        st.session_state.history.append({"origin": "ai", "message": fallback_question})
        save_chat_history(st.session_state.history)
    
    st.session_state.processing = False
def generate_interview_conclusion():
    """Generate a thank you message with feedback at the end of the interview"""
    user_details = st.session_state.get("user_details", {})
    name = user_details.get("name", "Candidate")
    
    user_responses = [msg["message"] for msg in st.session_state.history if msg["origin"] == "human"]
    avg_response_length = sum(len(response) for response in user_responses) / max(1, len(user_responses))
    
    detail_feedback = ""
    if avg_response_length < 50:
        detail_feedback = "Your responses were concise. In technical interviews, providing more details about your thought process can help interviewers understand your approach better."
    elif avg_response_length > 200:
        detail_feedback = "You provided detailed responses, which helps demonstrate your knowledge. Be mindful of keeping responses focused on the key points in time-limited interviews."
    else:
        detail_feedback = "Your responses were well-balanced in terms of detail and focus."
    
    thank_you_message = f"""
    <h3>Thank you, {name}!</h3>
    
    <p>We've completed our technical interview session. I appreciate your time and thoughtful responses to all the questions.</p>
    
    <p>{detail_feedback}</p>
    
    <p>Key areas covered in this interview:</p>
    <ul>
    """
    
    focus_areas = user_details.get("focus_areas", ["Technical Knowledge", "Problem Solving", "Communication"])
    for area in focus_areas:
        thank_you_message += f"<li>{area}</li>\n"
    
    thank_you_message += """
    </ul>
    
    <p>Your responses demonstrated technical knowledge and problem-solving skills. In a real interview setting, you would now have the opportunity to ask the interviewer questions about the role or company.</p>
    
    <p>If you'd like to continue practicing:</p>
    <ul>
    <li>Click "New Interview" to start a fresh session</li>
    <li>Click "Change Details" to modify your technical focus areas</li>
    </ul>
    
    <p>Best of luck with your future interviews!</p>
    """
    
    return thank_you_message