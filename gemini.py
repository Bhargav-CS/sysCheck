import os
import google.generativeai as genai
import PIL.Image

with open("key.txt") as f:
    key = f.read().strip()

genai.configure(api_key=key)

image_path = "screenshot.png"
sample_file = PIL.Image.open(image_path)

model = genai.GenerativeModel(model_name="gemini-1.5-pro")

prompt = "can you describe this image?"

response = model.generate_content([prompt, sample_file])
print(response.text)