# state.py

from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class CollegeState(TypedDict, total=False):
    """
    The central memory structure for the College Admissions Agent.
    Stored persistently in MongoDB via the Checkpointer.
    """
    messages: Annotated[List[BaseMessage], add_messages] 

    # STUDENT PROFILE DATA (Extracted/Stored)
    student_name: str
    target_course: str
    student_marks: float

    # PREDICTION DATA (Tool Output)
    prediction_score: float     

    # AGENT DECISIONS (Output to Counselor)
    alert_needed: bool          
    alert_message: str          
    next_step: str
