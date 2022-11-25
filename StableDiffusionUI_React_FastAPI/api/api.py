from auth_token import auth_token
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import torch
from diffusers import StableDiffusionPipeline
from io import BytesIO
import base64 
from PIL import Image
import numpy as np
import gradio as gr

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_credentials=True, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

device = "mps"
model_id = "CompVis/stable-diffusion-v1-4"
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", use_auth_token=True)
pipe.to(device)


pipe.enable_attention_slicing() 



@app.get("/")
def generate(prompt: str): 
 image = pipe(prompt, guidance_scale=8.5).images[0]
 image.save("testimage.png")
 buffer = BytesIO()
 image.save(buffer, format="PNG")
 imgstr = base64.b64encode(buffer.getvalue())

 return Response(content=imgstr, media_type="image/png")

