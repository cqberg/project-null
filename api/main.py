from fastapi import FastAPI, File, UploadFile
import torch
from torchvision.transforms import v2
from models import ConvNN
from PIL import Image
import io

app = FastAPI()

def load_model():
    model = ConvNN()
    load = torch.load("model/weights.pth")
    model.load_state_dict(load)

    return model

model = load_model()
model.eval()

transforms = v2.Compose([
    v2.ToImage(),
    v2.Resize((128,128)),
    v2.ToDtype(torch.float32, scale=True),
    v2.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

@app.post("/root")
async def root():
    return {"message": "Hello World"}

@app.post("/uploadfile/")
async def predict(file: UploadFile = File(...)):
    file = file.file.read()
    img = Image.open(io.BytesIO(file)).convert("RGB")

    img = transforms(img).unsqueeze(0)

    print(img.shape)

    with torch.no_grad():
        output = model(img).squeeze()

    return {"age": f"{output.item():.1f}"}