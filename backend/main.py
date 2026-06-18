from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import torch
from torchvision import transforms
from PIL import Image
import io
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ai_vision.model import DashboardLightCNN

app = FastAPI(title="RescueRoute Dispatch Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ACTIVE_REQUESTS = []

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'ai_vision', 'dashboard_cnn.pt')

CLASS_MAPPING = {
    0: "Battery System Alert",
    1: "Check Engine Warning",
    2: "Low Fuel Level Indicator",
    3: "Low Oil Pressure Critical Alert"
}

if not os.path.exists(MODEL_PATH):
    model = None
    print("Warning: Weights file missing.")
else:
    model = DashboardLightCNN(num_classes=4)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
    model.eval()
    print("AI Model loaded into FastAPI server successfully.")

inference_transforms = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

@app.post("/api/diagnose")
async def diagnose_dashboard(
    image: UploadFile = File(...), 
    location: str = Form(...)  
):
    if model is None:
        raise HTTPException(status_code=500, detail="AI engine offline.")

    try:
        image_bytes = await image.read()
        pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        tensor_image = inference_transforms(pil_image).unsqueeze(0)

        with torch.no_grad():
            outputs = model(tensor_image)
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            predicted_class_idx = torch.argmax(probabilities).item()
            confidence_score = probabilities[predicted_class_idx].item()

        diagnosis_text = CLASS_MAPPING.get(predicted_class_idx, "Unknown Malfunction")

        ticket_id = int(time.time() * 1000)
        dispatch_ticket = {
            "ticket_id": ticket_id,
            "location": location,
            "diagnosis": diagnosis_text,
            "confidence": f"{round(confidence_score * 100, 2)}%",
            "status": "Pending",
            "timestamp": time.strftime("%H:%M:%S")
        }
        
        ACTIVE_REQUESTS.append(dispatch_ticket)

        return {
            "status": "success",
            "ticket": dispatch_ticket,
            "message": f"AI Engine safely identified: {diagnosis_text}. Dispatched to providers."
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Inference failure: {str(e)}")

@app.get("/api/providers/requests")
async def get_provider_queue():
    """Returns the list of active breakdown emergency requests."""
    return ACTIVE_REQUESTS

@app.post("/api/providers/accept/{ticket_id}")
async def accept_ticket(ticket_id: int):
    """Updates ticket status once a mechanic claims the breakdown event."""
    for ticket in ACTIVE_REQUESTS:
        if ticket["ticket_id"] == ticket_id:
            ticket["status"] = "Dispatched"
            return {"status": "success", "ticket": ticket}
    raise HTTPException(status_code=404, detail="Ticket signature not found.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)