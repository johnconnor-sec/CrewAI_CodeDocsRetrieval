import os
from exa_py import Exa
from tavily import TavilyClient
from langchain.agents import tool
from langchain_experimental.tools import PythonREPLTool
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import List
from crewai.agent import Agent
from crewai.task import Task
from crewai_tools import CodeDocsSearchTool

class CodeDocsSearch:
    @tool
    def code_docs_search(query: str):
        """This function returns a CodeDocsSearchTool instance with specified URLs."""
        urls = [
            "https://docs.crewai.com/",
            "https://python.langchain.com/",
        ]
        code_docs_tool = CodeDocsSearchTool(docs_url=urls)
        return code_docs_tool
    
    def tools():
        return [
            CodeDocsSearch.code_docs_search,
        ]

class ExaSearchTool:
    @tool
    def search(query: str):
        """Search for a webpage based on the query."""
        return ExaSearchTool._exa().search(
            f"{query}", use_autoprompt=True, num_results=3
        )

    @tool
    def find_similar(url: str):
        """Search for webpages similar to a given URL. The url passed in should be a URL returned from `search`."""
        return ExaSearchTool._exa().find_similar(url, num_results=3)

    @tool
    def get_contents(query: str, ids: str):
        """Get the contents of a webpage. The ids must be passed in as a list, a list of ids returned from `search`."""
        if isinstance(ids, str):
            try:
                ids = eval(ids)
            except Exception as e:
                raise ValueError("Failed to evaluate the ids string. Ensure it is a valid list representation.")
        
        if not isinstance(ids, list):
            raise ValueError("The ids must be passed in as a list of ids returned from `search`.")

        contents = str(ExaSearchTool._exa().get_contents(ids))
        print(contents)
        contents = contents.split("URL:")
        contents = [content[:2000] for content in contents]
        return "\n\n".join(contents)

    def tools():
        return [
            ExaSearchTool.search,
            ExaSearchTool.find_similar,
            ExaSearchTool.get_contents,
        ]

    def _exa():
        return Exa(api_key=os.environ["EXA_API_KEY"])

class TavilySearchTool:
    @tool
    def tavily_search(query: str, search_depth="advanced"):
        """Search for a webpage using an AI assistant based on the query."""
        tavily = TavilyClient(os.environ["TAVILY_API_KEY"])
        context = tavily.get_search_context(f"{query}", use_autoprompt=True, num_results=5, search_depth=search_depth)
        return context

    
    def tools():
        return [
            TavilySearchTool.tavily_search,
        ]

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

class AgentTools(BaseModel):
    """
    A class that represents the tools available to agents in a crew.

    Attributes:
        agents (List[Agent]): List of agents in this crew.
        i18n (I18N): Internationalization settings.
    """

    agents: List[Agent] = Field(description="List of agents in this crew.")

    def tools(self):
        """Returns a list of tools available to the agents in this crew."""
        tools = [
            StructuredTool.from_function(
                func=self.delegate_work,
                name="Delegate work to co-worker",
                description=self.i18n.tools("delegate_work").format(
                    coworkers=f"[{', '.join([f'{agent.role}' for agent in self.agents])}]"
                ),
            ),
            StructuredTool.from_function(
                func=self.ask_question,
                name="Ask question to co-worker",
                description=self.i18n.tools("ask_question").format(
                    coworkers=f"[{', '.join([f'{agent.role}' for agent in self.agents])}]"
                ),
            ),
            *ExaSearchTool.tools(),
            *CodeDocsSearch.tools(),
            *TavilySearchTool.tools(),
            *PythonREPLTool.tools(),  # New tool added here
        ]
        return tools

    def delegate_work(self, coworker: str, task: str, context: str):
        """Useful to delegate a specific task to a co-worker passing all necessary context and names."""
        return self._execute(coworker, task, context)

    def ask_question(self, coworker: str, question: str, context: str):
        """Useful to ask a question, opinion or take from a co-worker passing all necessary context and names."""
        return self._execute(coworker, question, context)

    def _execute(self, agent, task, context):
        """Execute the command."""
        try:
            agent = [
                available_agent
                for available_agent in self.agents
                if available_agent.role.casefold().strip() == agent.casefold().strip()
            ]
        except Exception:
            return self.i18n.errors("agent_tool_non-existant_coworker").format(
                coworkers="\n".join(
                    [f"- {agent.role.casefold()}" for agent in self.agents]
                )
            )

        if not agent:
            return self.i18n.errors("agent_tool_non-existant_coworker").format(
                coworkers="\n".join(
                    [f"- {agent.role.casefold()}" for agent in self.agents]
                )
            )

        agent = agent[0]
        task = Task(
            description=task,
            agent=agent,
            expected_output="Your best answer to your co-worker asking you this, accounting for the context shared.",
        )
        return agent.execute_task(task, context)
