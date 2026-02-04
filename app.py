from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    testcases = ""

    if request.method == "POST":
        requirement = request.form.get("requirement")

        # Try calling OpenAI API
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": f"Generate functional, negative and edge test cases for: {requirement}"
                }
            ]
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data
        )

        # DEMO MODE FALLBACK
        if response.status_code == 200:
            testcases = response.json()["choices"][0]["message"]["content"]
        else:
            testcases = """
Functional Test Cases:
1. Verify user can submit valid input.
2. Verify system processes request correctly.

Negative Test Cases:
1. Verify error for invalid input.
2. Verify system handles empty input.

Edge Test Cases:
1. Verify maximum input length.
2. Verify special characters handling.
"""

    return render_template("index.html", testcases=testcases)


if __name__ == "__main__":
    app.run(debug=True)
