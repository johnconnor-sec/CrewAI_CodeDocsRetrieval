# CrewAI_CodeDocsRetrieval
An experimental crew built to retrieve code documentation and write python code. 

This repo was modified from the code found at [[https://alejandro-ao.com/crew-ai-crash-course-step-by-step/|CrewAi Crash Course by Alejandro Ao]].

# CrewAI Setup
#### Example File Structure
```
my_crewai_project/ 
├── .env
|-- .gitignore 
├── agents.py 
├── tools.py 
├── tasks.py  
├── requirements.txt (or pyproject.toml if using Poetry) 
└── main.py

```

In order to set up this crew, we should consider the following concepts: agents, tools, tasks and processes.

1. **Tasks**: These are the tasks that our agents will perform. Each task will be assigned to an agent.
2. **Agents**: These are the AI agents that will be working for us. Each agent is an expert in a different task. In this case, we will have 4 agents.
3. **Tools**: These are the tools that our agents will use to perform their tasks. These can be, for example, a search engine, a summarizer, a translator, etc.
4. **Process**: A process dictates the way that our agents will work together. In this case, we will use a sequential process, which means that each agent will work one after the other. (More about this later).

### Agents Example 
```python
def research_agent(self):
  return Agent(
    role='Research Specialist',
    goal='Conduct thorough research on people and companies involved in the meeting',
    tools=ExaSearchTool.tools(),
    backstory=dedent("""\
        As a Research Specialist, your mission is to uncover detailed information
        about the individuals and entities participating in the meeting. Your insights
        will lay the groundwork for strategic meeting preparation."""),
    verbose=True
  )
```

### Tasks Example
```python
def research_task(self, agent, participants, meeting_context):
  return Task(
    description=dedent(f"""\
      Conduct comprehensive research on each of the individuals and companies
      involved in the upcoming meeting. Gather information on recent
      news, achievements, professional background, and any relevant
      business activities.

      Participants: {participants}
      Meeting Context: {meeting_context}"""),
    expected_output=dedent("""\
      A detailed report summarizing key findings about each participant
      and company, highlighting information that could be relevant for the meeting."""),
    async_execution=True,
    agent=agent
  )
```

### Tools Example
```python
from exa_py import Exa
from langchain.agents import tool

def search(query: str):
  """Search for a webpage based on the query."""
  return ExaSearchTool._exa().search(
      f"{query}", use_autoprompt=True, num_results=3
  )
```
Or the full toolset:
```python
import os
from exa_py import Exa
from langchain.agents import tool


class ExaSearchTool:
    @tool
    def search(query: str):
        """Search for a webpage based on the query."""
        return ExaSearchTool._exa().search(
            f"{query}", use_autoprompt=True, num_results=3
        )

    @tool
    def find_similar(url: str):
        """Search for webpages similar to a given URL.
        The url passed in should be a URL returned from `search`.
        """
        return ExaSearchTool._exa().find_similar(url, num_results=3)

    @tool
    def get_contents(ids: str):
        """Get the contents of a webpage.
        The ids must be passed in as a list, a list of ids returned from `search`.
        """

        print("ids from param:", ids)

        ids = eval(ids)
        print("eval ids:", ids)

        contents = str(ExaSearchTool._exa().get_contents(ids))
        print(contents)
        contents = contents.split("URL:")
        contents = [content[:1000] for content in contents]
        return "\n\n".join(contents)

    def tools():
        return [
            ExaSearchTool.search,
            ExaSearchTool.find_similar,
            ExaSearchTool.get_contents,
        ]

    def _exa():
        return Exa(api_key=os.environ["EXA_API_KEY"])

```

### Main.py Example  
```python
from dotenv import load_dotenv
load_dotenv()

from crewai import Crew

from tasks import MeetingPreparationTasks
from agents import MeetingPreparationAgents

tasks = MeetingPreparationTasks()
agents = MeetingPreparationAgents()

print("## Welcome to the Meeting Prep Crew ##")
participants = input("What are the names of the participants in the meeting?\n")
meeting_context = input("What is the context of the meeting?\n")
objective = input("What is your objective for this meeting?\n")

# Create Agents
researcher_agent = agents.research_agent()
industry_analyst_agent = agents.industry_analysis_agent()
meeting_strategy_agent = agents.meeting_strategy_agent()
summary_and_briefing_agent = agents.summary_and_briefing_agent()

# Create Tasks
research = tasks.research_task(researcher_agent, participants, meeting_context)
industry_analysis = tasks.industry_analysis_task(industry_analyst_agent, participants, meeting_context)
meeting_strategy = tasks.meeting_strategy_task(meeting_strategy_agent, context, objective)
summary_and_briefing = tasks.summary_and_briefing_task(summary_and_briefing_agent, context, objective)

meeting_strategy.context = [research, industry_analysis]
summary_and_briefing.context = [research, industry_analysis, meeting_strategy]

# Create Crew responsible for Copy
#######################################
# Below is the "Process" for the Crew #
#######################################
crew = Crew(
	agents=[
		researcher_agent,
		industry_analyst_agent,
		meeting_strategy_agent,
		summary_and_briefing_agent
	],
	tasks=[
		research,
		industry_analysis,
		meeting_strategy,
		summary_and_briefing
	]
)

result = crew.kickoff()


# Print results
print("## Here is the result")
print(result)
```

### Processes Example
See the highly commented code directly above for implementation. (Check out [[The Path/Tech/CodeDocs/docs.crewai.com/tools/CodeDocsSearchTool|CodeDocsSearchTool]] tool)
```python
from crewai import Crew
from crewai.process import Process
from langchain_openai import ChatOpenAI

# Example: Creating a crew with a sequential process
crew = Crew(
    agents=my_agents,
    tasks=my_tasks,
    process=Process.sequential
)

# Example: Creating a crew with a hierarchical process
# Ensure to provide a manager_llm
crew = Crew(
    agents=my_agents,
    tasks=my_tasks,
    process=Process.hierarchical,
    manager_llm=ChatOpenAI(model="gpt-4")
)
```

# Using PraisonAI to Quickly Create Agents
```python
export OPENAI_API_KEY="openai-api-key"
praisonai --init "Goal for agents"
```
This will create an `agents.yaml` file. The output of this tool, (`agents.yaml`) will look like the following:
```
topic: review the code documentation for creative solutions to the users coding problems
  and present those solutions in code
roles:
  documentation_analyst:
    backstory: Specializes in sifting through extensive documentation to reveal hidden
      gems of coding knowledge and innovative solutions.
    goal: Identify and understand code documentation that offers potential solutions.
    role: Documentation Analyst
    tasks:
      documentation_review:
        description: Review the code documentation thoroughly to identify potential
          solutions to complex coding problems.
        expected_output: A report highlighting relevant documentation sections with
          potential solutions.
    tools:
    - ''
  solution_architect:
    backstory: With a keen eye for detail and a creative mindset, transforms insights
      from documentation into viable coding strategies.
    goal: Design comprehensive and creative solutions.
    role: Solution Architect
    tasks:
      solution_design:
        description: Leverage findings from the Documentation Analyst to design innovative
          and practical solutions for coding problems.
        expected_output: A detailed design document outlining proposed solutions,
          including pseudo-code and architectural diagrams.
    tools:
    - ''
  code_developer:
    backstory: Experienced in various programming languages and environments, ready
      to turn solution designs into executable code.
    goal: Implement solutions in code.
    role: Code Developer
    tasks:
      solution_implementation:
        description: Transform the solution designs from the Solution Architect into
          working code, testing for efficiency and effectiveness.
        expected_output: Fully functional code that solves the users' coding problems,
          along with documentation for deployment and usage.
    tools:
    - ''
dependencies: []
```

You can use this file to quickly detail your agents and tasks files. Use chatGPT to load in the example files above (crewAI example files & praisonai `agents.yaml`) to quickly build the code. 

# Using [[The Path/Tech/CodeDocs/docs.phidata.com/index|phidata]] for easy tool integration

Based on the information provided in the search results, it is possible to use Phidata to create tools that can be integrated with CrewAI agents. Here's how you can approach this:

1. **Create a function in Phidata that performs the desired action**
Phidata allows you to define functions that can be used as tools by your AI assistant. These functions can perform various actions like making API calls, querying databases, sending emails, or any other task you need your CrewAI agent to be able to do. [1][2]

Example:
```python
from phi.assistant import Assistant

def search_wikipedia(query):
    # Code to search Wikipedia and return results
    return wikipedia_results

assistant = Assistant(tools=[search_wikipedia])
```

2. **Integrate the Phidata tool with CrewAI**
Once you have defined the function in Phidata, you can import and use it as a tool for your CrewAI agents. CrewAI provides a flexible way to integrate custom tools. [4]

Example:
```python
from crewai import Agent
from phi.assistant import Assistant

# Define Phidata tool
def search_wikipedia(query):
    ...

# Create Phidata assistant with the tool
phi_assistant = Assistant(tools=[search_wikipedia])

# Create CrewAI agent and pass the Phidata assistant as a tool
agent = Agent(tools=[phi_assistant])
```

3. **Use the tool within CrewAI tasks**
With the Phidata tool integrated, your CrewAI agent can now call and use that tool's functionality while executing tasks. [4]

```python
from crewai import Task, Crew

# Create task that uses the Phidata Wikipedia search tool
task = Task(agent=agent, description="Research Wikipedia for information on AI")

# Execute the task
crew = Crew(agents=[agent], tasks=[task])
crew.kickoff()
```

By leveraging Phidata's ability to define custom functions as tools and CrewAI's flexibility in integrating external tools, you can enhance your CrewAI agents with powerful capabilities tailored to your specific use case. This allows you to build more sophisticated and capable AI systems. [1][2][4]

Citations:
[1] https://www.youtube.com/watch?v=ZMBUVzhIQho
[2] https://www.youtube.com/watch?v=OiIPUxLKZ-w
[3] https://www.phidata.com
[4] https://docs.crewai.com/core-concepts/Tools/
[5] https://github.com/joaomdmoura/crewAI

----
----

Yes, you can create custom tools using Phidata and integrate them with CrewAI crews. Phidata is a powerful data processing library that allows you to build custom tools for various tasks, such as data extraction, transformation, and analysis.

To create a custom tool with Phidata and use it in a CrewAI crew, you can follow these general steps:

1. **Define the tool function**: Create a Python function that performs the desired task using Phidata. This function should take the necessary inputs and return the desired output.

2. **Wrap the function as a CrewAI tool**: Use the `@tool` decorator from CrewAI to wrap your Phidata function and turn it into a CrewAI tool. This decorator allows you to specify the tool's name, description, and input/output schemas.

Example:

```python
from crewai_tools import tool
import phidata as pd

@tool("My Phidata Tool", description="A tool that performs data processing using Phidata.")
def my_phidata_tool(input_data: str) -> str:
    # Use Phidata to process the input data
    processed_data = pd.process(input_data)
    
    # Return the processed data
    return str(processed_data)
```

3. **Create an Agent with the custom tool**: When creating a CrewAI Agent, include your custom Phidata tool in the `tools` list.

Example:

```python
from crewai import Agent

agent = Agent(
    role="Data Analyst",
    goal="Analyze and process data",
    tools=[my_phidata_tool],
    # Other agent configurations
)
```

4. **Use the tool in a Task**: Within a CrewAI Task, you can instruct the Agent to use the custom Phidata tool by including it in the task description or expected output.

Example:

```python
from crewai import Task

task = Task(
    description="Use the My Phidata Tool to process the given data.",
    expected_output="The processed data using the My Phidata Tool.",
    agent=agent
)
```

5. **Execute the Task**: Finally, execute the Task within a CrewAI Crew, and the Agent will use the custom Phidata tool as needed to complete the task.

By following these steps, you can leverage the power of Phidata to create custom data processing tools and seamlessly integrate them into your CrewAI crews, enabling your agents to perform more complex and specialized tasks.[1][2][3]

Citations:
[1] https://github.com/joaomdmoura/crewAI/issues/135
[2] https://docs.crewai.com/core-concepts/Tools/
[3] https://www.youtube.com/watch?v=wmcFEj1lXnk
[4] https://github.com/joaomdmoura/crewAI/issues/20
[5] https://stackoverflow.com/questions/78466708/crewai-not-finding-co-worker

# Using [[The Path/Tech/CodeDocs/python.langchain.com/v0.1/docs/modules/tools/custom_tools|langchain custom_tools]] in crewAI

CrewAI is built on Langchain. You can integrate the tools in langchain with CrewAI. The Langchain Toolset contains many tools. To integrate them, I imported the Langchain tool documentation into ChatGPT as well as a CrewAI sample tools.py file. 
```python
from langchain_openai import ChatOpenAI

manager_llm=ChatOpenAI(model_name="gpt-4o", temperature=0.2),
```

```python
from langchain.agents import tool
from langchain_experimental.tools import PythonREPLTool
from langchain.tools import StructuredTool

class PythonREPLTool:
	@tool
	def create_python_repl_tool(query: str):
	"""Useful for writing and testing python code."""

	def execute_python_code(code: str) -> str:
		tool = PythonREPLTool()
		return tool.run(code)

	return StructuredTool.from_function(
		func=execute_python_code,
		name="Execute Python Code",
		description="Executes Python code and returns the result. Useful for dynamically evaluating Python code."
		)

def tools():
	return [
		PythonREPLTool.create_python_repl_tool(),
	]
```

Make sure to follow LangChains documentation when implementing custom tools!
