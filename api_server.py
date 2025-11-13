from dotenv import load_dotenv
load_dotenv()  # Must be before importing tools/main

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage
from main import college_agent_app

app = FastAPI(title="AI Admission Advisor API", version="2.2")

class AdmissionRequest(BaseModel):
    student_name: str
    target_course: str
    student_marks: float

@app.get("/")
async def root():
    return {"message": "AI Admission Advisor API is running successfully!"}

@app.post("/predict")
async def predict_admission(data: AdmissionRequest):
    try:
        initial_state = {
            "messages": [HumanMessage(content=f"Hello, I got {data.student_marks}% marks. What are my chances for {data.target_course}?")],
            "student_name": data.student_name,
            "target_course": data.target_course,
            "student_marks": data.student_marks,
            "prediction_score": -1.0,
            "alert_message": "",
            "email_status": "",
            "next_step": "predict",
        }

        result = college_agent_app.invoke(
            initial_state,
            config={"configurable": {"thread_id": data.student_name.lower().replace(" ", "_")}}
        )

        final_response = result.get("final_response", "")
        if not final_response:
            last_msg = result["messages"][-1]
            final_response = last_msg.content if isinstance(last_msg, AIMessage) else str(last_msg)

        return JSONResponse(
            content={
                "student_name": donse,
            }
        )ata.student_name,
                "target_course": data.target_course,
                "student_marks": data.student_marks,
                "prediction_score": result.get("prediction_score", None),
                "alert_message": result.get("alert_message", ""),
                "email_status": result.get("email_status", ""),
                "final_response": final_resp

    except Exception as e:
        return JSONResponse(
            content={"error": str(e), "message": "Prediction process failed."},
            status_code=500,
        )
