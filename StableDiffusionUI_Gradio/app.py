import os
from io import BytesIO
import gradio as gr
import numpy as np
import torch
from diffusers import StableDiffusionImg2ImgPipeline, StableDiffusionPipeline
from PIL import Image
from authtoken import auth_token

print("hello")

device="cpu"

#Pipeline - Text to Image
prompt_pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", use_auth_token=True)
prompt_pipe.to(device)

#Pipeline - Image to Image
img_pipe = StableDiffusionImg2ImgPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", use_auth_token=True)
img_pipe.to(device)

source_img = gr.Image(source="upload", type="filepath", label="init_img | 512*512 px")
gallery = gr.Gallery(label="Generated images", show_label=False, elem_id="gallery").style(grid=[1], height="auto")
gallery_text = gr.Gallery(label="Generated images", show_label=False, elem_id="gallery").style(grid=[1], height="auto")


#Text to Imgage

def genarate_text(prompt): 
    images_list_text = prompt_pipe([prompt]* 1)
    images_text = []
    safe_image_text = Image.open(r"unsafe.png")
    for i, image in enumerate(images_list_text["images"]):
        if(images_list_text["nsfw_content_detected"][i]):
            images_text.append(safe_image_text)
        else:
            images_text.append(image)

    return images_text



# Resize init image to 512 x 512 

def resize(value,img):
  img = Image.open(img)
  img = img.resize((value,value), Image.Resampling.LANCZOS)
  
  return img

# Image to Image
def genarate_image(source_img, prompt, guide, steps, seed, strength):

    source_image = resize(512, source_img)
    source_image.save('source.png')
    
    images_list = img_pipe([prompt] * 1, init_image=source_image, strength=strength, guidance_scale=guide, num_inference_steps=steps)
    images = []
    safe_image = Image.open(r"unsafe.png")
    
    for i, image in enumerate(images_list["images"]):
        if(images_list["nsfw_content_detected"][i]):
            images.append(safe_image)
        else:
            images.append(image)    
    return images

    

print("Great! Everything is working fine !")

  
# Text to Image UI
app_text = gr.Interface(fn=genarate_text, 
inputs="text", 
outputs=gallery_text, allow_flagging="never",flagging_dir="flagged",
examples = ["Mythical monster creature haunted forest jungle fantasy colourful pixar cute", 
"A beautiful mansion beside a waterfall in the woods, by josef thoma, matte painting, trending on artstation HQ",
"Cute and adorable ferret wizard, wearing coat and suit, steampunk, lantern, anthromorphic, Jean paptiste monge, oil painting",
"Dynamic photography portrait female balloon rabbit magical world candy", 
"Movie poster science fiction action adventure famous actor award dinosaur", 
"Infinity expanse galaxy travel alien world adventure marvel stylised unknown",
"Medieval tribe knight ninja samurai castle bridge autumn temple", 
"Virtual production led wall lighting film visual effects cinema real-time",
"Abstract constellations 3d parallel geometric volume fractionated schematic"]).queue(max_size=10) 

# Image to Image UI
app_image = gr.Interface(fn=genarate_image, inputs=[source_img,"text",
    gr.Slider(2, 15, value = 7, label = 'Guidence Scale'),
    gr.Slider(10, 50, value = 25, step = 1, label = 'Number of Iterations'),
    gr.Slider(label = "Seed", minimum = 0, maximum = 2147483647, step = 1, randomize = True),
    gr.Slider(label='Strength', minimum = 0, maximum = 1, step = .05, value = .75)
    ],
    outputs=gallery,
    allow_flagging="never",
    flagging_dir="flagged",
    ).queue(max_size=100)


# Interface CSS
css = '''
.gradio-container {font-family: 'IBM Plex Sans', sans-serif;}
.gradio-container {background-color: #ffebf7;}   
.gr-button {
            color: white;
            border-color: white;
            background: #FFBBE4;
        }
        input[type='range'] {
            accent-color: black;
        }
        .dark input[type='range'] {
            accent-color: #dfdfdf;
        }
.gr-button {
            white-space: nowrap;
        }
.gr-button:hover {
            background: #AE92FF;
        }        
.gr-button:focus {
            border-color: rgb(147 197 253 / var(--tw-border-opacity));
            outline: none;
            box-shadow: var(--tw-ring-offset-shadow), var(--tw-ring-shadow), var(--tw-shadow, 0 0 #0000);
            --tw-border-opacity: 1;
            --tw-ring-offset-shadow: var(--tw-ring-inset) 0 0 0 var(--tw-ring-offset-width) var(--tw-ring-offset-color);
            --tw-ring-shadow: var(--tw-ring-inset) 0 0 0 calc(3px var(--tw-ring-offset-width)) var(--tw-ring-color);
            --tw-ring-color: rgb(191 219 254 / var(--tw-ring-opacity));
            --tw-ring-opacity: .5;
        }
        #advanced-btn {
            font-size: .6rem !important;
            line-height: 19px;
            margin-top: 12px;
            margin-bottom: 12px;
            padding: 2px 8px;
            border-radius: 14px !important;
        }
        #advanced-options {
            display: none;
            margin-bottom: 20px;
        }
.animate-spin {
            animation: spin 1s linear infinite;
        }        

'''


with gr.Blocks(css=css) as demo:
    gr.Markdown(
    """
    # 🖼 Stable Diffusion 🚀

    <description>
    <img> 
    <p> This application leverages the model trained by Stability AI and Runway ML to generate images using the Stable Diffusion Deep Learning model.
    <P> The best stable diffusion prompts will have this form: A [type of picture] of a [main subject], [style cues]
    <P> 💥 Image generation process will take approximately 3-5 minutes.
    """)
    gr.TabbedInterface([app_text, app_image], ["Text to Image", "Image to Image"])    


if __name__ == "__main__":
    demo.launch(enable_queue=True,share=True)




