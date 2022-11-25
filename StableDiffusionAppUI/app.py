import tkinter as tk
import customtkinter as ctk
from PIL import Image
from PIL import ImageTk
from authtoken import auth_token

import torch 
from diffusers import StableDiffusionPipeline 
from diffusers import StableDiffusionImg2ImgPipeline


# Create the app
app = tk.Tk()
app.geometry("532x632")
app.title("Lea") 
ctk.set_appearance_mode("dark") 

prompt = ctk.CTkEntry(height=40, width=512, text_font=("Arial", 20), text_color="black", fg_color="white") 
prompt.place(x=10, y=10)

lmain = ctk.CTkLabel(height=512, width=512)
lmain.place(x=10, y=110)

modelid = "CompVis/stable-diffusion-v1-4"
device = "mps"


pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
pipe = pipe.to(device)

pipe.enable_attention_slicing() 



def generate(): 
 with torch.cuda.amp.autocast(device):
    image = pipe(prompt.get()).images[0]                              
    image.show('generatedimage.png')
    image.save('generatedimage.png')
    img = ImageTk.PhotoImage(image)
    lmain.configure(image=img) 

trigger = ctk.CTkButton(height=40, width=120, text_font=("Arial", 20), text_color="white", fg_color="black", command=generate) 
trigger.configure(text="Generate") 
trigger.place(x=206, y=60) 

app.mainloop()