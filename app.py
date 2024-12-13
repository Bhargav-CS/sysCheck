from flask import Flask, send_file, render_template, jsonify
import os
import google.generativeai as genai
import PIL.Image
import re

app = Flask(__name__)

def format_response(text):
    # Wrap code blocks in <pre><code> tags
    formatted_text = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', text, flags=re.DOTALL)
    # Wrap paragraphs in <p> tags
    formatted_text = re.sub(r'\n\n', r'</p><p>', formatted_text)
    formatted_text = f"<p>{formatted_text}</p>"
    # Ensure proper nesting of <p> tags
    formatted_text = formatted_text.replace('<p><pre>', '<pre>').replace('</pre></p>', '</pre>')
    return formatted_text

def capture_screenshot(filename="screenshot.png"):
    import mss
    with mss.mss() as sct:
        sct.shot(output=filename)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/screenshot", methods=["GET"])
def send_screenshot():
    capture_screenshot("screenshot.png")
    print("Screenshot captured")
    file_url = "/download/screenshot.png"
    
    return jsonify({"url": file_url})

@app.route("/download/screenshot.png", methods=["GET"])
def download_screenshot():
    file_path = os.path.abspath("screenshot.png")
    return send_file(file_path, mimetype="image/png")

@app.route("/generate", methods=["GET"])
def generate_description():
    with open("key.txt") as f:
        key = f.read().strip()

    genai.configure(api_key=key)

    image_path = "screenshot.png"
    sample_file = PIL.Image.open(image_path)

    model = genai.GenerativeModel(model_name="gemini-1.5-pro")

    prompt = """the image provided is going to be for the coding test. Your job is the understand the image and figure out what the function described in the image does.
        after that write well written code that complete the funtion according the imgage provided and the description that might be provided in the comments of the funtion.
        the code given by you should be well optimized and should all of the test cases provided in the test cases section, as well as hidden test cases that might be present.
        the code should be well commented and should be easy to understand by other developers. After giving the code, please write how the code given by you works.
        if the image is not that of a code or a code editor, please write a description of the image."""

    response = model.generate_content([prompt, sample_file])
    description = format_response(response.text)

    # Save the description to a file
    with open("description.txt", "w") as file:
        file.write(description)

    return jsonify({"description": description})

if __name__ == "__main__":
    print("Server is running. Access the screenshot at http://<your-ip>:5000")
    app.run(host="0.0.0.0", port=5000)