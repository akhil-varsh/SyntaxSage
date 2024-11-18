import streamlit as st
import ollama
import subprocess

# Define function to call the local Llama model via Ollama library
def query_llama(prompt):
    response = ollama.chat(model="llama3.1", messages=[{"role": "user", "content": prompt}])
    
    # Check the response structure
    if 'text' in response:
        return response['text']
    elif 'message' in response:
        return response['message']
    else:
        return f"Unexpected response structure: {response}"


# Define the four agent functions
def execute_code(code):
    try:
        exec_locals = {}
        exec(code, {}, exec_locals)
        return exec_locals
    except Exception as e:
        return str(e)

def get_code_summary(code):
    prompt = f"Provide a concise summary of the following code:\n{code}"
    return query_llama(prompt)

def get_code_suggestions(code):
    prompt = f"Provide suggestions for improving or optimizing the following code:\n{code}"
    return query_llama(prompt)

def get_code_time_complexity(code):
    prompt = f"Analyze the time complexity of the following code:\n{code}"
    return query_llama(prompt)

# Streamlit UI
def main():
    st.title("AI Code Analysis Tool")
    
    # User input: code text area
    code = st.text_area("Enter your code here:")

    if st.button('Analyze'):
        if code.strip():
            st.subheader("Code Execution Output:")
            execution_output = execute_code(code)
            st.write(execution_output)

            st.subheader("Code Summary:")
            code_summary = get_code_summary(code)
            st.write(code_summary)

            st.subheader("Code Suggestions:")
            code_suggestions = get_code_suggestions(code)
            st.write(code_suggestions)

            st.subheader("Code Time Complexity:")
            time_complexity = get_code_time_complexity(code)
            st.write(time_complexity)
        else:
            st.warning("Please enter some code to analyze.")

if __name__ == "__main__":
    main()
