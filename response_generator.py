import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.8,
    google_api_key=GEMINI_API_KEY
)

prompt_template = ChatPromptTemplate.from_template(
    """
    You are an AI admission advisor.

    Student Name: {student_name}
    Target Course: {target_course}
    Marks: {student_marks}%
    Predicted Admission Probability: {prediction_score:.1%}

    Provide a personalized, encouraging, and motivating response.
    """
)

response_chain = prompt_template | llm | StrOutputParser()

def generate_response(student_name: str, target_course: str, student_marks: float, prediction_score: float):
    return response_chain.invoke({
        "student_name": student_name,
        "target_course": target_course,
        "student_marks": student_marks,
        "prediction_score": prediction_score
    })
