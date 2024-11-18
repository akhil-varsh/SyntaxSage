from flask import Flask, render_template, request, Response
import ollama
import subprocess

app = Flask(__name__)

def query_llama(prompt):
    response = ollama.chat(model="llama3.1", messages=[{"role": "user", "content": prompt}])
    return response.get('text', 'Error: Unable to get response.')

def execute_code(code):
    try:
        exec_locals = {}
        exec(code, {}, exec_locals)
        return str(exec_locals)
    except Exception as e:
        return f"Error: {str(e)}"

def get_code_summary(code):
    prompt = f"Provide a concise summary of the following code:\n{code}"
    return query_llama(prompt)

def get_code_suggestions(code):
    prompt = f"Provide suggestions for improving or optimizing the following code:\n{code}"
    return query_llama(prompt)

def get_code_time_complexity(code):
    prompt = f"Analyze the time complexity of the following code:\n{code}"
    return query_llama(prompt)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze_code', methods=['POST'])
def analyze_code():
    code = request.form['code']
    if not code:
        return Response("No code provided.", status=400, mimetype='text/plain')
    
    execution_output = execute_code(code)
    code_summary = get_code_summary(code)
    code_suggestions = get_code_suggestions(code)
    time_complexity = get_code_time_complexity(code)
    
    response_html = f"""
    <div class="analysis-results">
        <div class="execution">
            <pre>{execution_output}</pre>
        </div>
        <div class="summary">
            <pre>{code_summary}</pre>
        </div>
        <div class="suggestions">
            <pre>{code_suggestions}</pre>
        </div>
        <div class="complexity">
            <pre>{time_complexity}</pre>
        </div>
    </div>
    """
    
    return Response(response_html, mimetype='text/html')

if __name__ == '__main__':
    app.run(debug=True)
# from flask import Flask, render_template, request, Response
# import ollama
# import subprocess

# app = Flask(__name__)

# def query_llama(prompt):
#     response = ollama.chat(model="llama3.1", messages=[{"role": "user", "content": prompt}])
#     return response.get('text', 'Error: Unable to get response.')

# def execute_code(code):
#     try:
#         exec_locals = {}
#         exec(code, {}, exec_locals)
#         return str(exec_locals)
#     except Exception as e:
#         return f"Error: {str(e)}"

# def get_code_summary(code):
#     prompt = f"Provide a concise summary of the following code:\n{code}"
#     return query_llama(prompt)

# def get_code_suggestions(code):
#     prompt = f"Provide suggestions for improving or optimizing the following code:\n{code}"
#     return query_llama(prompt)

# def get_code_time_complexity(code):
#     prompt = f"Analyze the time complexity of the following code:\n{code}"
#     return query_llama(prompt)

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/analyze_code', methods=['POST'])
# def analyze_code():
#     code = request.form['code']
#     if not code:
#         return Response("No code provided.", status=400, mimetype='text/plain')

#     execution_output = execute_code(code)
#     code_summary = get_code_summary(code)
#     code_suggestions = get_code_suggestions(code)
#     time_complexity = get_code_time_complexity(code)
    
#     output = f"""
#     Code Execution Output:
#     {execution_output}
    
#     Code Summary:
#     {code_summary}
    
#     Code Suggestions:
#     {code_suggestions}
    
#     Code Time Complexity:
#     {time_complexity}
#     """
    
#     return Response(output, mimetype='text/plain')

# if __name__ == '__main__':
#     app.run(debug=True)
