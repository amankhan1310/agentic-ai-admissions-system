# AI-Powered Admission Prediction & Counseling Agent

An intelligent Agentic AI system built using LangGraph, LangChain, Gemini LLM, and FastAPI to automate college admission prediction, personalized counseling, and counselor alert workflows.

This project combines:

* AI-driven admission prediction
* LLM-powered personalized guidance
* Workflow orchestration using LangGraph
* Tool-based execution using LangChain
* Automated email alert system
* REST API deployment

---

# Features

* Admission probability prediction based on marks and target course
* Personalized AI-generated counseling responses using Gemini
* Agentic workflow orchestration with LangGraph
* Tool calling architecture using LangChain
* Automatic counselor email alerts for high-risk candidates
* FastAPI-based REST API backend
* Persistent checkpointing using MongoDB
* Modular and scalable AI architecture

---

# Tech Stack

## AI / Agentic Frameworks

* LangGraph
* LangChain
* Google Gemini 2.5 Flash

## Backend

* Python
* FastAPI
* REST APIs

## Database / Memory

* MongoDB
* LangGraph Checkpointer

## AI Features

* Prompt Engineering
* Tool Calling
* Stateful Agent Workflow

## Email Integration

* SendGrid API

## Development Tools

* Visual Studio Code
* Git
* GitHub

---

# System Architecture

```text
User Request
      ↓
FastAPI Endpoint
      ↓
LangGraph Workflow
      ↓
Ingestion Node
      ↓
Reasoning Agent Node
      ├── Admission Prediction Tool
      ├── Gemini LLM Response Generation
      ↓
Final Action Node
      ├── SendGrid Email Alert
      ↓
Final API Response
```

---

# Workflow Explanation

## 1. Ingestion Node

* Receives and validates student input
* Initializes state variables
* Prepares workflow state

## 2. Reasoning Agent Node

* Normalizes target course
* Calls prediction tool
* Calculates admission probability
* Sends contextual prompt to Gemini
* Generates personalized counseling response

## 3. Final Action Node

* Evaluates prediction score
* Triggers automated email alerts for low-probability candidates
* Returns final workflow response

---

# Tools Used

## 1. Admission Prediction Tool

Predicts admission probability using course-specific cutoff logic.

### Inputs

* Student Marks
* Target Course

### Output

* Admission Probability Score

---

## 2. Email Alert Tool

Sends automated counselor alerts using SendGrid.

### Trigger Condition

* Prediction score below threshold

---

# API Endpoint

## POST `/predict`

### Sample Request

```json
{
  "student_name": "Aman",
  "target_course": "CSE",
  "student_marks": 85
}
```

---

### Sample Response

```json
{
  "student_name": "Aman",
  "target_course": "CSE",
  "student_marks": 85,
  "prediction_score": 0.4,
  "alert_message": "Critical Email Alert Dispatched",
  "final_response": "You have a moderate chance of admission..."
}
```

---

# Project Structure

```text
├── main.py
├── api.py
├── tools.py
├── state.py
├── response_generator.py
├── requirements.txt
├── .env
└── README.md
```

---

# Environment Variables

Create a `.env` file and add:

```env
GEMINI_API_KEY=your_api_key
MONGO_URI=your_mongodb_uri
SENDGRID_API_KEY=your_sendgrid_key
SENDER_EMAIL=your_email
COUNSELOR_EMAIL=recipient_email
```

---

# Installation & Setup

## Clone Repository

```bash
git clone <your_repo_url>
cd project-folder
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run FastAPI Server

```bash
uvicorn api:app --reload
```

---

# Key Concepts Implemented

* Agentic AI Workflow
* Stateful AI Systems
* LLM Tool Calling
* Workflow Orchestration
* AI-based Decision Automation
* REST API Integration
* Persistent Memory Management

---

# Future Improvements

* Real ML model integration
* Multi-agent admission counseling
* Vector database integration
* Student profile memory
* Dashboard analytics
* RAG-based college recommendations

---

# Author

**Aman Yahya Khan**

AI & Machine Learning Engineer
MIT ADT University, Pune

GitHub: `github.com/amankhan1310`
LinkedIn: `linkedin.com/in/aman-khan-40804a283`
