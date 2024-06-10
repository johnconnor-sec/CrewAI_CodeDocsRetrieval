from dotenv import load_dotenv
from crewai import Crew
from tasks import CrewTasks
from agents import CodeDocsAgents
from langchain_openai import ChatOpenAI

def main():
    load_dotenv()
    
    print("\033[1;32mWelcome to John Connor's Code Docs Search and Builder Tool\033[0m")
    print("-----------------------------------------------")
    participants = input("\033[1;32mDescribe the coding problem or task you need help with:\033[0m ")
    context = input("\033[1;32mExplain the specific requirements, constraints, and background information for this coding challenge:\033[0m ")
    objectives = input("\033[1;32mList the specific objectives, success criteria, features or outcomes you want to achieve with this task:\033[0m ")

    
    tasks = CrewTasks() # Use this class from tasks.py to create tasks. Pass the methods below.
    agents = CodeDocsAgents() # Use this class from agents.py to create agents. Pass the methods below.
    
    # create agents
    documentation_analyst = agents.documentation_analyst() # The methods from the CodeDocsAgents class in the agents.py file
    solution_architect = agents.solution_architect()
    code_developer = agents.code_developer()
    code_reviewer = agents.code_reviewer()
    
    # create tasks
    documentation_review_task = tasks.documentation_review_task(documentation_analyst, participants)
    solution_design_task = tasks.solution_design_task(solution_architect, context)
    solution_implementation_task = tasks.solution_implementation_task(code_reviewer, objectives)
    python_repl_execution_task = tasks.python_repl_execution_task(code_developer, code_reviewer)
    code_review_task = tasks.code_review_task(code_reviewer, participants)
    
    ## Set the context for each task
    solution_implementation_task.context = [documentation_review_task, solution_design_task]
    python_repl_execution_task.context = [solution_implementation_task, code_review_task]
    code_review_task.context = [python_repl_execution_task, solution_design_task]
    
    
    crew = Crew(
        agents=[
            documentation_analyst, 
            solution_architect, 
            code_developer, 
            code_reviewer
            ], 
        tasks=[
            documentation_review_task, 
            solution_design_task, 
            solution_implementation_task, 
            python_repl_execution_task, 
            code_review_task
            ], 
        verbose=2,
        manager_llm=ChatOpenAI(model_name="gpt-4o", temperature=0.2),
        process="hierarchical",
        memory=True
        )
    
    result = crew.kickoff()
    
    print(result)
    
if __name__ == "__main__":
    main()