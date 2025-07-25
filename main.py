from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from models.chatbot import ChatbotSession

app = FastAPI()

# In-memory session store
sessions = {}

class QueryRequest(BaseModel):
    session_id: str
    query: str

@app.post("/start")
def start_session():
    session_id = str(uuid4())
    sessions[session_id] = ChatbotSession()
    return {"session_id": session_id, "message": "Session started"}

@app.post("/ask")
def ask_question(req: QueryRequest):
    session = sessions.get(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session.handle_question(req.query)

@app.post("/end")
def end_session(session_id: str):
    if session_id in sessions:
        del sessions[session_id]
        return {"message": "Session ended"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")

@app.get("/health")
def health():
    return {"status": "ok"}
