from crewai import Agent, Task, Crew
from langchain_community.llms import Ollama

# Initialize the LLM (local model)
llm = Ollama(model='llama3.1:latest')

# Define agents for each task
execution_agent = Agent(
    llm=llm,
    role="Code Execution Agent",
    goal="To compile and execute code provided by the user, and return the output or any errors encountered during execution.You are very strict in following the syntaxes.",
    backstory="An expert in multiple programming languages, this agent can compile code efficiently and handle various execution environments.",
    allow_delegation=False
)

summary_agent = Agent(
    llm=llm,
    role="Code Summary Agent",
    goal="Provide a concise and comprehensive summary of the given code, highlighting its purpose, structure, and key components.",
    backstory="A seasoned software developer with years of experience in understanding complex codebases and providing technical insights.",
    allow_delegation=False
)

suggestion_agent = Agent(
    llm=llm,
    role="Code Suggestion Agent",
    goal="To analyze the code and provide suggestions for improving its time complexity and efficiency, without altering the original logic.",
    backstory="A performance optimization specialist with a deep understanding of algorithms and data structures.",
    allow_delegation=False
)

complexity_agent = Agent(
    llm=llm,
    role="Time Complexity Estimation Agent",
    goal="To estimate the time complexity of the provided code, analyzing loops, recursion, and algorithm efficiency.",
    backstory="A competitive programmer and algorithm specialist capable of breaking down complex logic to understand performance bottlenecks.",
    allow_delegation=False
)

# Function to create tasks and run the agents
def run_code_tasks(code_input):
    # Define the tasks for each agent
    task_execution = Task(
        description=code_input,
        expected_output="The output of the compiled code or any runtime errors.",
        agent=execution_agent
    )

    task_summary = Task(
        description=code_input,
        expected_output="A brief summary explaining what the code does and its structure.",
        agent=summary_agent
    )

    task_suggestions = Task(
        description=code_input,
        expected_output="Suggestions for improving time complexity and performance.",
        agent=suggestion_agent
    )

    task_complexity = Task(
        description=code_input,
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
