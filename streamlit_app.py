"""
SyntaxSage - AI-Powered Code Analysis Tool (Streamlit Version)
============================================================

This Streamlit application provides real-time code analysis using Gemma3 model
through Docker. It offers parallel processing for efficient analysis of:
- Code execution and output
- Code summary and explanation  
- Optimization suggestions
- Time complexity analysis

Author: Akhil Varsh
License: See LICENSE file
"""

import streamlit as st
import requests
import json
import concurrent.futures
from io import StringIO
import sys
import time
import traceback

# Configure Streamlit page
st.set_page_config(
    page_title="SyntaxSage - AI Code Analysis",
    page_icon="🧙‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .analysis-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
    }
    .execution-section {
        border-left-color: #28a745;
    }
    .summary-section {
        border-left-color: #17a2b8;
    }
    .suggestions-section {
        border-left-color: #ffc107;
    }
    .complexity-section {
        border-left-color: #dc3545;
    }
    .stCodeBlock {
        background-color: #2d2d2d;
    }
</style>
""", unsafe_allow_html=True)

class GemmaAPI:
    """Interface for interacting with Gemma3 model via Docker"""
    
    def __init__(self, base_url: str = "http://gemma3:8080"):
        self.base_url = base_url
        
    def query_model(self, prompt: str, max_retries: int = 3) -> str:
        """
        Query the Gemma3 model with retry logic
        
        Args:
            prompt (str): The prompt to send to the model
            max_retries (int): Maximum number of retry attempts
            
        Returns:
            str: The model's response or error message
        """
        for attempt in range(max_retries):
            try:
                payload = {
                    "prompt": prompt,
                    "max_tokens": 1000,
                    "temperature": 0.7,
                    "top_p": 0.9
                }
                
                response = requests.post(
                    f"{self.base_url}/generate",
                    json=payload,
                    timeout=30,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get('generated_text', 'No response generated')
                else:
                    st.error(f"API Error {response.status_code}: {response.text}")
                    
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    return f"Connection Error: Unable to reach Gemma3 model after {max_retries} attempts. {str(e)}"
                time.sleep(2 ** attempt)  # Exponential backoff
                
        return "Error: Maximum retry attempts exceeded"

def execute_code(code: str) -> str:
    """
    Safely execute Python code and capture its output.
    
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

def get_code_summary(gemma_api: GemmaAPI, code: str) -> str:
    """Generate a concise summary of the provided code."""
    prompt = f"""Analyze this Python code and provide a clear, concise summary explaining what it does, its main purpose, and key functionality:

```python
{code}
```

Please provide a well-structured summary in 2-3 paragraphs."""
    
    return gemma_api.query_model(prompt)

def get_code_suggestions(gemma_api: GemmaAPI, code: str) -> str:
    """Get AI-powered suggestions for code improvement."""
    prompt = f"""Analyze this Python code and provide specific, actionable suggestions for improvement. Focus on code quality, performance, readability, and best practices:

```python
{code}
```

Please provide:
1. Performance optimizations
2. Code quality improvements
3. Best practice recommendations
4. Potential bug fixes or edge cases"""
    
    return gemma_api.query_model(prompt)

def get_code_complexity(gemma_api: GemmaAPI, code: str) -> str:
    """Analyze the time complexity of the provided code."""
    prompt = f"""Analyze the time and space complexity of this Python code. Provide Big O notation and explain the reasoning step by step:

```python
{code}
```

Please provide:
1. Time complexity analysis with Big O notation
2. Space complexity analysis
3. Detailed explanation of the complexity reasoning
4. Suggestions for complexity improvements if applicable"""
    
    return gemma_api.query_model(prompt)

def run_parallel_analysis(gemma_api: GemmaAPI, code: str) -> dict:
    """
    Run all code analyses in parallel for optimal performance.
    
    Args:
        gemma_api: The Gemma API interface
        code (str): The code to analyze
        
    Returns:
        dict: Analysis results from all functions
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Submit all analysis tasks
        futures = {
            'execution': executor.submit(execute_code, code),
            'summary': executor.submit(get_code_summary, gemma_api, code),
            'suggestions': executor.submit(get_code_suggestions, gemma_api, code),
            'complexity': executor.submit(get_code_complexity, gemma_api, code)
        }
        
        # Collect results with timeout
        results = {}
        for analysis_type, future in futures.items():
            try:
                results[analysis_type] = future.result(timeout=60)
            except concurrent.futures.TimeoutError:
                results[analysis_type] = f"{analysis_type.title()} analysis timed out"
            except Exception as e:
                results[analysis_type] = f"Error in {analysis_type}: {str(e)}"
                
        return results

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">🧙‍♂️ SyntaxSage</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">AI-Powered Python Code Analysis Tool</p>', unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Gemma3 API configuration
        gemma_url = st.text_input(
            "Gemma3 API URL", 
            value="http://gemma3:8080",
            help="URL of the Gemma3 model API endpoint"
        )
        
        # Test connection
        if st.button("🔗 Test Connection"):
            gemma_api = GemmaAPI(gemma_url)
            test_result = gemma_api.query_model("Hello! Can you respond with 'Connection successful'?")
            if "Connection successful" in test_result or "Hello" in test_result:
                st.success("✅ Connection successful!")
            else:
                st.error("❌ Connection failed!")
                st.error(test_result)
        
        st.markdown("---")
        
        # Sample code examples
        st.header("📚 Code Examples")
        sample_codes = {
            "Fibonacci": """def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")""",
            
            "Bubble Sort": """def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

numbers = [64, 34, 25, 12, 22, 11, 90]
print("Original:", numbers)
sorted_numbers = bubble_sort(numbers.copy())
print("Sorted:", sorted_numbers)""",
            
            "List Comprehension": """# Generate squares of even numbers
numbers = range(1, 11)
even_squares = [x**2 for x in numbers if x % 2 == 0]
print("Even squares:", even_squares)

# Dictionary comprehension
word_lengths = {word: len(word) for word in ['python', 'streamlit', 'gemma', 'docker']}
print("Word lengths:", word_lengths)"""
        }
        
        selected_example = st.selectbox("Choose an example:", ["Custom"] + list(sample_codes.keys()))
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("💻 Python Code Editor")
        
        # Code input
        if selected_example != "Custom" and selected_example in sample_codes:
            default_code = sample_codes[selected_example]
        else:
            default_code = """# Write your Python code here
def hello_world():
    print("Hello, SyntaxSage!")
    return "Welcome to AI-powered code analysis!"

result = hello_world()
print(result)"""

        code_input = st.text_area(
            "Enter your Python code:",
            value=default_code,
            height=400,
            help="Write your Python code here. The AI will analyze it for execution, summary, suggestions, and complexity."
        )
        
        # Analysis button
        if st.button("🚀 Analyze Code with AI", type="primary", use_container_width=True):
            if not code_input.strip():
                st.error("Please enter some Python code to analyze!")
                return
            
            # Initialize Gemma API
            gemma_api = GemmaAPI(gemma_url)
            
            # Show analysis progress
            with st.spinner("🤖 AI is analyzing your code..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Run parallel analysis
                status_text.text("Running parallel analysis...")
                progress_bar.progress(25)
                
                results = run_parallel_analysis(gemma_api, code_input)
                progress_bar.progress(100)
                status_text.text("Analysis complete!")
                
                # Store results in session state
                st.session_state['analysis_results'] = results
                st.session_state['analyzed_code'] = code_input
    
    with col2:
        st.header("📊 Analysis Results")
        
        # Display results if available
        if 'analysis_results' in st.session_state:
            results = st.session_state['analysis_results']
            
            # Code Execution Results
            st.markdown('<div class="analysis-section execution-section">', unsafe_allow_html=True)
            st.subheader("⚡ Code Execution Result")
            st.code(results.get('execution', 'No execution result'), language='text')
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Code Summary
            st.markdown('<div class="analysis-section summary-section">', unsafe_allow_html=True)
            st.subheader("📝 Code Summary")
            st.write(results.get('summary', 'No summary available'))
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Improvement Suggestions
            st.markdown('<div class="analysis-section suggestions-section">', unsafe_allow_html=True)
            st.subheader("💡 Improvement Suggestions")
            st.write(results.get('suggestions', 'No suggestions available'))
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Complexity Analysis
            st.markdown('<div class="analysis-section complexity-section">', unsafe_allow_html=True)
            st.subheader("⏱️ Time Complexity Analysis")
            st.write(results.get('complexity', 'No complexity analysis available'))
            st.markdown('</div>', unsafe_allow_html=True)
            
        else:
            st.info("👈 Enter your Python code and click 'Analyze Code with AI' to see results here!")
            
            # Show feature preview
            st.markdown("""
            ### 🎯 What you'll get:
            
            - **⚡ Code Execution**: See your code's output in real-time
            - **📝 AI Summary**: Understand what your code does
            - **💡 Smart Suggestions**: Get optimization recommendations
            - **⏱️ Complexity Analysis**: Learn about performance characteristics
            
            ### 🚀 Powered by:
            - **Gemma3 AI Model** for intelligent analysis
            - **Parallel Processing** for fast results
            - **Docker Integration** for reliable deployment
            """)

if __name__ == "__main__":
    main()