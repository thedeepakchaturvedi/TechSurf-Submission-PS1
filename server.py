from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates

import shutil
import os
import compress
import base64

# Initializing app
app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html",{"request":request})


@app.post("/compression_score")
def perform_compression(image: UploadFile = File(...)):
    temp_file = _save_file_to_disk(image, path="temp", save_as="temp")
    compression_extent = compress.do_compression(temp_file, 'temp.jpg')
    
    print("Compression Extend", compression_extent)
    print("Image Filename: ", image.filename)
    
    # Encoding the image to base64
    with open("./output/compressed.jpg", "rb") as img_file:
        b64_string = base64.b64encode(img_file.read())
        
    return {"compression_extent":compression_extent,
            "filename":image.filename,
            "fileBuffer": b64_string}


def _save_file_to_disk(uploaded_file, path=".",save_as="default"):  
    extension = os.path.splitext(uploaded_file.filename)[-1]
    
    if extension != '.jpg':
        extension = ".jpg"
        
    temp_file = os.path.join(path, save_as + extension)
    
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
        
    return temp_file