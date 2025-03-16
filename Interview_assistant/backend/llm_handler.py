from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from backend.models import LLM_MODEL

def create_llm_chain():
    """Create and return the LLM chain for generating interview questions"""
    llm = Ollama(model=LLM_MODEL)
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an AI interviewer. Generate ONLY a single follow-up question based on the candidate's response. DO NOT include any explanations or commentary. Keep the questions moderately challenging and mix conceptual, coding, and scenario-based questions. The question should be direct and concise."),
        ("user", "Candidate response: {input}")
    ])
    return prompt_template | llm | StrOutputParser()

def create_conclusion_chain():
    """Create and return the LLM chain for generating interview conclusions"""
    llm = Ollama(model=LLM_MODEL)
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an AI technical interviewer concluding an interview. Generate a concise, professional conclusion with personalized feedback based on the candidate's performance. Your conclusion should be encouraging but also mention areas for improvement. Keep the tone professional and constructive."),
        ("user", "Candidate name: {name}\nTechnical areas: {tech_areas}\nExperience level: {experience}\nFocus areas: {focus_areas}")
    ])
    return prompt_template | llm | StrOutputParser()