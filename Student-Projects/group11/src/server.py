from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api import get_ai_response   # AI response handler

app = FastAPI()

# Allow access from frontend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class UserMessage(BaseModel):
    prompt: str

# Generate AI response
@app.post("/generate")
def generate_response(data: UserMessage):
    reply = get_ai_response(data.prompt)
    return {"response": reply}

# Run server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
