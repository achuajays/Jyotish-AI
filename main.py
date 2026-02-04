from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.agent import app as agent_app

app = FastAPI(title="Astrology AI Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class horoscopeRequest(BaseModel):
    date_of_birth: str
    time_of_birth: str
    place_of_birth: str
    year_of_birth: str

@app.post("/api/horoscope")
async def get_horoscope(request: horoscopeRequest):
    try:
        inputs = {
            "date_of_birth": request.date_of_birth,
            "time_of_birth": request.time_of_birth,
            "place_of_birth": request.place_of_birth,
            "year_of_birth": request.year_of_birth,
            "reading": None
        }
        
        result = await agent_app.ainvoke(inputs)
        return {"reading": result["reading"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi.staticfiles import StaticFiles
import os
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
