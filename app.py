from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import sys

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def run_code_interactively(code, user_input=None):
    try:
        process = subprocess.Popen(
            [sys.executable, "-c", code],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True
        )

        if user_input:
            process.stdin.write(user_input + "\n")
            process.stdin.flush()

        stdout, stderr = process.communicate()

        return {"stdout": stdout, "stderr": stderr}
    except Exception as e:
        return {"stdout": "", "stderr": str(e)}

@app.route('/run', methods=['POST'])
def run_python_code():
    data = request.json
    code = data.get("code", "")
    user_input = data.get("input", None)

    # Run the code and capture output
    result = run_code_interactively(code, user_input)
    stdout = result['stdout']
    stderr = result['stderr']

    return jsonify({
        "stdout": stdout or "no output.",
        "stderr": stderr or ""
    })

if __name__ == "__main__":
    app.run(debug=True)
