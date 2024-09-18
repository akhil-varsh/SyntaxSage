from flask import Flask, render_template, request, jsonify
from agents import run_code_tasks

app = Flask(__name__)

@app.route('/')
def index():
    # Render the main page with the code editor
    return render_template('index.html')

@app.route('/run_code', methods=['POST'])
def run_code():
    # Get the code input from the user
    code_input = request.form.get('code_input')

    if code_input:
        # Call the function that processes the code and gets results from agents
        task_output = run_code_tasks(code_input)
        
        # Return the result as JSON to update the frontend dynamically
        return jsonify(task_output)
    else:
        return jsonify({"error": "No code input provided."})

if __name__ == '__main__':
    app.run(debug=True)
