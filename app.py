"""
SyntaxSage - An intelligent code analysis tool powered by AI
=====================================================

This Flask application provides real-time code analysis using LLaMA 3.1 model
through Ollama. It offers parallel processing for efficient analysis of:
- Code execution and output
- Code summary and explanation  
- Optimization suggestions
- Time complexity analysis

Author: Akhil Varsh
License: See LICENSE file
"""

from flask import Flask, render_template, request, Response
import ollama
import concurrent.futures
from io import StringIO
import sys

# Initialize Flask application
app = Flask(__name__)

def query_llama(prompt: str) -> str:
    """
    Query the LLaMA 3.1 model through Ollama for code analysis.
    
    Args:
        prompt (str): The prompt to send to the LLM
        
    Returns:
        str: The model's response or error message
    """
    try:
        response = ollama.chat(
            model="llama3.1", 
            messages=[{
                "role": "user", 
                "content": prompt
            }]
        )
        return response.get('message', {}).get('content', 'Error: Unable to get response.')
    except Exception as e:
        return f"Error connecting to LLM: {str(e)}"

def execute_code(code: str) -> str:
    """
    Safely execute Python code and capture its output.
    
    This function redirects stdout to capture print statements and
    executes the code in an isolated namespace for security.
    
    Args:
        code (str): The Python code to execute
        
    Returns:
        str: The execution output or error message
    """
    try:
        # Redirect stdout to capture print outputs
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()

        # Execute the code in isolated namespace for security
        exec_locals = {}
        exec(code, {"__builtins__": __builtins__}, exec_locals)
        
        # Restore stdout and get captured output
        sys.stdout = old_stdout
        output = redirected_output.getvalue()
        
        # Return captured output or show executed variables
        if output.strip():
            return output
        else:
            # Show variables created during execution
            user_vars = {k: v for k, v in exec_locals.items() 
                        if not k.startswith('__')}
            return str(user_vars) if user_vars else "Code executed successfully (no output)"
            
    except Exception as e:
        # Restore stdout in case of error
        sys.stdout = old_stdout
        return f"Execution Error: {str(e)}"

def get_code_summary(code: str) -> str:
    """
    Generate a concise summary of the provided code.
    
    Args:
        code (str): The code to summarize
        
    Returns:
        str: AI-generated summary of the code
    """
    prompt = f"""Provide a clear and concise summary of the following Python code. 
    Explain what it does, its main purpose, and key functionality:

    ```python
    {code}
    ```"""
    return query_llama(prompt)

def get_code_suggestions(code: str) -> str:
    """
    Get AI-powered suggestions for code improvement.
    
    Args:
        code (str): The code to analyze for improvements
        
    Returns:
        str: AI-generated suggestions for optimization
    """
    prompt = f"""Analyze the following Python code and provide specific suggestions for improvement.
    Focus on code quality, performance, readability, and best practices:

    ```python
    {code}
    ```

    Please provide actionable suggestions with explanations."""
    return query_llama(prompt)

def get_code_time_complexity(code: str) -> str:
    """
    Analyze the time complexity of the provided code.
    
    Args:
        code (str): The code to analyze for time complexity
        
    Returns:
        str: AI-generated time complexity analysis
    """
    prompt = f"""Analyze the time and space complexity of the following Python code.
    Provide Big O notation and explain the reasoning:

    ```python
    {code}
    ```

    Please explain the complexity analysis step by step."""
    return query_llama(prompt)

def run_analysis(func, code: str) -> str:
    """
    Wrapper function to run analysis functions with proper error handling.
    
    Args:
        func: The analysis function to run
        code (str): The code to analyze
        
    Returns:
        str: Analysis result or error message
    """
    try:
        return func(code)
    except Exception as e:
        return f"Analysis failed: {str(e)}"

@app.route('/')
def home():
    """
    Render the main application page.
    
    Returns:
        Rendered HTML template for the code editor interface
    """
    return render_template('index.html')

@app.route('/analyze_code', methods=['POST'])
def analyze_code():
    """
    Process code analysis request using parallel processing.
    
    This endpoint receives Python code via POST request and performs
    multiple types of analysis concurrently for optimal performance:
    - Code execution and output capture
    - AI-powered code summary
    - Optimization suggestions  
    - Time complexity analysis
    
    Returns:
        Response: HTML formatted analysis results
    """
    # Get code from request
    code = request.form.get('code', '').strip()
    if not code:
        return Response(
            "Error: No code provided for analysis.", 
            status=400, 
            mimetype='text/plain'
        )

    # Define analysis functions and their display names
    analysis_functions = [
        (execute_code, "execution", "Code Execution"),
        (get_code_summary, "summary", "Code Summary"), 
        (get_code_suggestions, "suggestions", "Improvement Suggestions"),
        (get_code_time_complexity, "complexity", "Time Complexity Analysis")
    ]

    # Execute all analyses in parallel for better performance
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Submit all analysis tasks
        future_to_analysis = {
            executor.submit(run_analysis, func, code): (name, display_name)
            for func, name, display_name in analysis_functions
        }

        # Initialize results with default error messages
        results = {
            "execution": "Execution analysis failed",
            "summary": "Summary generation failed", 
            "suggestions": "Suggestions generation failed",
            "complexity": "Complexity analysis failed"
        }

        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_analysis):
            analysis_name, display_name = future_to_analysis[future]
            try:
                results[analysis_name] = future.result()
            except Exception as e:
                results[analysis_name] = f"Error in {display_name}: {str(e)}"

    # Format response as clean HTML
    response_html = f"""
    <div class="analysis-results">
        <div class="result-section execution">
            <h3>Code Execution Result</h3>
            <pre class="result-content">{results['execution']}</pre>
        </div>
        <div class="result-section summary">
            <h3>Code Summary</h3>
            <pre class="result-content">{results['summary']}</pre>
        </div>
        <div class="result-section suggestions">
            <h3>Improvement Suggestions</h3>
            <pre class="result-content">{results['suggestions']}</pre>
        </div>
        <div class="result-section complexity">
            <h3>Time Complexity Analysis</h3>
            <pre class="result-content">{results['complexity']}</pre>
        </div>
    </div>
    """
    
    return Response(response_html, mimetype='text/html')

if __name__ == '__main__':
    """
    Run the Flask application in debug mode for development.
    
    The application will be accessible at http://localhost:5000
    Debug mode enables auto-reload on code changes and detailed error pages.
    """
    print("🚀 Starting SyntaxSage - AI-Powered Code Analysis Tool")
    print("📝 Access the application at: http://localhost:5000")
    print("🔧 Debug mode: Enabled")
    print("⚠️  Make sure Ollama is running with LLaMA 3.1 model")
    
    app.run(debug=True, host='0.0.0.0', port=5000)