from crewai import Agent, Task, Crew, LLM
from litellm import completion


# Configure Ollama API Base (adjust if needed)
my_llm = LLM(
)

# Function to get LLM response
def get_llm_response(prompt):
    try:
        response = completion(
            model="ollama/llama3.1",
            messages=[{"content": prompt, "role": "user"}],
            api_base="http://localhost:11434"
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting LLM response: {str(e)}"

# Define agents for each task
def create_agent(role, goal, backstory):
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        llm=get_llm_response,  # Use the custom LLM function
        allow_delegation=False
    )

# Create specific agents
execution_agent = create_agent(
    role="Code Execution Agent",
    goal="To compile and execute code provided by the user, and return the output or any errors encountered during execution. You are very strict in following the syntaxes.",
    backstory="An expert in multiple programming languages, this agent can compile code efficiently and handle various execution environments."
)

summary_agent = create_agent(
    role="Code Summary Agent", 
    goal="Provide a concise and comprehensive summary of the given code, highlighting its purpose, structure, and key components.",
    backstory="A seasoned software developer with years of experience in understanding complex codebases and providing technical insights."
)

suggestion_agent = create_agent(
    role="Code Suggestion Agent",
    goal="To analyze the code and provide suggestions for improving its time complexity and efficiency, without altering the original logic.",
    backstory="A performance optimization specialist with a deep understanding of algorithms and data structures."
)

complexity_agent = create_agent(
    role="Time Complexity Estimation Agent",
    goal="To estimate the time complexity of the provided code, analyzing loops, recursion, and algorithm efficiency.",
    backstory="A competitive programmer and algorithm specialist capable of breaking down complex logic to understand performance bottlenecks."
)

# Function to create tasks and run the agents
def run_code_tasks(code_input):
    # Define the tasks for each agent
    task_execution = Task(
        description=f"Analyze and execute the following code:\n{code_input}",
        expected_output="The output of the compiled code or any runtime errors.",
        agent=execution_agent
    )
    
    task_summary = Task(
        description=f"Provide a summary of the following code:\n{code_input}",
        expected_output="A brief summary explaining what the code does and its structure.",
        agent=summary_agent
    )
    
    task_suggestions = Task(
        description=f"Provide performance suggestions for the following code:\n{code_input}",
        expected_output="Suggestions for improving time complexity and performance.",
        agent=suggestion_agent
    )
    
    task_complexity = Task(
        description=f"Estimate time complexity for the following code:\n{code_input}",
        expected_output="Estimated time complexity for the code, including analysis of loops and recursive structures.",
        agent=complexity_agent
    )
    
    # Create the crew to manage and run tasks
    crew = Crew(
        agents=[execution_agent, summary_agent, suggestion_agent, complexity_agent],
        tasks=[task_execution, task_summary, task_suggestions, task_complexity],
        verbose=1
    )
    
    # Run the tasks and get the output
    task_output = crew.kickoff()
    
    return task_output

# Optional: Test the setup
if __name__ == "__main__":
    print()