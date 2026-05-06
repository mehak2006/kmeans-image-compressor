import logging
import base64
from fastapi.responses import JSONResponse



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from fastapi import HTTPException
from kmeans import compress_image_kmeans
import numpy as np
import cv2
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return {"message":"Hello World"}



@app.post('/compress')
async def compress_image(file: UploadFile = File(...), k: int = 16):
    if k <= 1 or k > 64:
        raise HTTPException(status_code=400, detail="K must be between 2 and 64")
    contents = await file.read()

    np_arr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    
    if image is None:
        raise HTTPException(status_code=400, detail="Invalid image file")
    MAX_DIM = 1200

    h, w = image.shape[:2]

    scale = min(MAX_DIM / max(h, w), 1)

    new_w = int(w * scale)
    new_h = int(h * scale)

    image = cv2.resize(image, (new_w, new_h))

    logger.info(f"K value: {k}")
    logger.info(f"Image shape: {image.shape}")

    compressed, centroids = compress_image_kmeans(image, K=k)
    _, buffer = cv2.imencode(".jpg", compressed, [cv2.IMWRITE_JPEG_QUALITY, 85])
    img_base64 = base64.b64encode(buffer).decode("utf-8")

    return JSONResponse({
        "image": img_base64,
        "centroids": centroids.tolist()
    })