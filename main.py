import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from pymongo import MongoClient
from langgraph.checkpoint.mongodb import MongoDBSaver
from langgraph.checkpoint.memory import InMemorySaver
from state import CollegeState
from tools import get_admission_prediction, send_email_alert
from response_generator import generate_response
import logging

# ------------------- I. INIT -------------------
load_dotenv()
logging.basicConfig(level=logging.INFO)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found.")

LLM_MODEL = "gemini-2.5-flash"
tools = [get_admission_prediction, send_email_alert]

llm = ChatGoogleGenerativeAI(model=LLM_MODEL, temperature=0, google_api_key=GEMINI_API_KEY)
llm_with_tools = llm.bind_tools(tools)

# MongoDB checkpoint
MONGO_URI = os.getenv("MONGO_URI")
if MONGO_URI:
    try:
        mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        mongo_client.admin.command("ping")
        logging.info("✅ MongoDB Checkpointer initialized.")
        memory = MongoDBSaver(mongo_client, database_name="langgraph_checkpoints")
    except Exception as e:
        logging.warning(f"❌ MongoDB connection failed: {e}. Using InMemorySaver.")
        memory = InMemorySaver()
else:
    logging.info("❌ MONGO_URI not found. Using InMemorySaver.")
    memory = InMemorySaver()

# ------------------- II. NODES -------------------
def ingestion_node(state: CollegeState) -> CollegeState:
    logging.info("--- INGESTION NODE ---")
    state.update({
        "student_name": state.get("student_name", "Unknown"),
        "target_course": state.get("target_course", "Unknown"),
        "student_marks": state.get("student_marks", 0.0),
        "prediction_score": -1.0,
    })
    return state

def reasoning_agent_node(state: CollegeState) -> CollegeState:
    logging.info("--- REASONING AGENT NODE ---")
    
    # Prediction
    if state.get("prediction_score", -1.0) == -1.0:
        # Normalize course input
        target_course = state["target_course"].strip().lower()

        # Supported course list
        supported_courses = {
            "cse": "Computer Science and Engineering",
            "it": "Information Technology",
            "mechanical": "Mechanical Engineering",
            "entc": "Electronics and Telecommunication Engineering",
            "civil": "Civil Engineering",
            "electrical": "Electrical Engineering",
            "ai": "Artificial Intelligence",
            "b.tech ai": "B.Tech in Artificial Intelligence"
        }

        # Match course
        matched_course = supported_courses.get(target_course, state["target_course"])

        # Call prediction tool
        prediction_text = get_admission_prediction.invoke({
            "target_course": matched_course,
            "student_marks": state["student_marks"]
        })
        state["messages"].append(AIMessage(content=prediction_text))

        # Extract numeric probability from string
        try:
            score_part = prediction_text.split("Score Value:")[1].strip()
            state["prediction_score"] = float(score_part)
        except Exception:
            state["prediction_score"] = 0.0

    # Generate LLM response
    try:
        final_text = generate_response(
            student_name=state["student_name"],
            target_course=state["target_course"],
            student_marks=state["student_marks"],
            prediction_score=state["prediction_score"]
        )
        state["messages"].append(AIMessage(content=final_text))
        state["final_response"] = final_text
    except Exception as e:
        logging.error(f"⚠️ LLM failed: {e}")
        state["final_response"] = "AI could not generate a response."

    state["next_step"] = "final_action"
    return state


def final_action_node(state: CollegeState) -> CollegeState:
    logging.info("--- FINAL ACTION NODE ---")
    score = state.get("prediction_score", 0.0)
    alert_message = "No critical alert needed."

    if score < 0.6:
        alert_body = (
            f"URGENT LEAD: {state['student_name']} is a high-risk lead.\n"
            f"Predicted chance: {score*100:.1f}%.\nFollow-up needed for {state['target_course']}."
        )
        email_result = send_email_alert.invoke({
            "to_email": os.getenv("COUNSELOR_EMAIL"),
            "subject": f"HIGH RISK LEAD: {state['student_name']}",
            "body": alert_body
        })
        logging.info(f"[EMAIL TOOL RESULT] {email_result}")
        alert_message = "Critical Email Alert Dispatched to Counselor."

    state["alert_message"] = alert_message
    return state

# ------------------- ROUTING -------------------
def route_decision_logic(last_message) -> str:
    if isinstance(last_message, AIMessage) and getattr(last_message, "tool_calls", None):
        return "tool_executor"
    return "final_action"

# ------------------- BUILD GRAPH -------------------
def build_college_agent_graph():
    workflow = StateGraph(CollegeState)
    workflow.add_node("ingestion", ingestion_node)
    workflow.add_node("reasoning_agent", reasoning_agent_node)
    workflow.add_node("tool_executor", ToolNode(tools))
    workflow.add_node("final_action", final_action_node)
    workflow.add_edge(START, "ingestion")
    workflow.add_edge("ingestion", "reasoning_agent")
    workflow.add_conditional_edges(
        "reasoning_agent",
        route_decision_logic,
        {"tool_executor": "tool_executor", "final_action": "final_action"},
    )
    workflow.add_edge("tool_executor", "reasoning_agent")
    workflow.add_edge("final_action", END)
    return workflow.compile(checkpointer=memory)

college_agent_app = build_college_agent_graph()

# ------------------- EXECUTION -------------------
if __name__ == "__main__":
    print("\n🎓 COLLEGE ADMISSION AGENT")
    student_name = input("Enter student name: ").strip()
    target_course = input("Enter target course (CSE, IT, Mechanical, ENTC, Civil, Electrical, AI): ").strip()
    student_marks = float(input("Enter student marks: ").strip())

    initial_state = {
        "messages": [HumanMessage(content=f"Hello, I got {student_marks}% marks. What are my chances for {target_course}?")],
        "student_name": student_name,
        "target_course": target_course,
        "student_marks": student_marks,
        "prediction_score": -1.0,
        "alert_message": "",
        "next_step": "predict",
    }

    result = college_agent_app.invoke(
        initial_state,
        config={"configurable": {"thread_id": f"{student_name.lower()}_{int(student_marks)}"}}
    )

    final_response = result.get("final_response", "")
    print("\nFINAL OUTPUT")
    print(f"👩‍🎓 Student: {student_name}")
    print(f"🎯 Course: {target_course}")
    print(f"📊 Marks: {student_marks}")
    print(f"🧠 Prediction Score: {result.get('prediction_score')}")
    print(f"💬 Agent's Response: {final_response}")
    print(f"📧 Alert: {result.get('alert_message')}")
