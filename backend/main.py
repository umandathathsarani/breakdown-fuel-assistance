from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="RescueRoute AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/diagnose")
async def diagnose_dashboard(image: UploadFile = File(...)):
    contents = await image.read()

    mock_prediction = "Check Engine Light"
    confidence = 0.88

    return {
        "status": "success",
        "filename": image.filename,
        "diagnosis": mock_prediction,
        "confidence": confidence,
        "message": f"AI identified: {mock_prediction}. Proceed with caution."
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)