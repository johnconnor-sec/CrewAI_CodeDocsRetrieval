# CrewAI_CodeDocsRetrieval
An experimental crew built to retrieve code documentation and write python code. 

This repo was modified from the code found at https://alejandro-ao.com/crew-ai-crash-course-step-by-step/. Thank you to Alejandro for putting together such a comprehensive introduction.

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

# To Run this file:

You will need to create a virtual environment and install dependencies.

`pip install crewai 'crewai[tools]'`

Then simply run `python3 main.py` and follow the prompts.

Please let me know what you think and how it can be improved. Thank you and God bless.
