import openai
import pdfplumber
from flask import Flask, request, jsonify

app = Flask(__name__)

OPENAI_API_KEY = "your-openai-api-key"
openai.api_key = OPENAI_API_KEY

def analyze_resume(resume_text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional HR specialist."},
            {"role": "user", "content": f"Review this resume:\n{resume_text}"}
        ]
    )
    return response["choices"][0]["message"]["content"]

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files["resume"]
    with pdfplumber.open(file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages])

    feedback = analyze_resume(text)
    return jsonify({"feedback": feedback})

if __name__ == "__main__":
    app.run(debug=True)
