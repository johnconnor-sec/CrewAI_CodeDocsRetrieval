from textwrap import dedent
from crewai import Task

class CrewTasks():
    def documentation_review_task(self, agent, documentation):
        return Task(
            description=dedent(f"""\
            You are tasked with reviewing the code documentation to identify potential solutions to complex coding problems. 
            This involves thoroughly reading through the provided documentation to find relevant sections that offer insights, 
            best practices, or solutions that can be applied to the current coding challenges.

            Instructions
            ------------
            1. Review the provided documentation thoroughly.
            2. Identify sections that are relevant to solving the current coding problems.
            3. Highlight any innovative solutions, best practices, or useful code snippets found in the documentation.

            ------------
            Documentation: {documentation}"""),
            expected_output=dedent(f"""\
            Your final deliverable should be a comprehensive report that includes:
            1. A summary of the relevant sections from the documentation.
            2. Highlighted potential solutions and innovative approaches found.
            3. Any useful code snippets or best practices identified in the documentation."""),
            agent=agent,
            async_execution=True
        )

    def solution_design_task(self, agent, documentation):
        return Task(description=dedent(f"""\
            You are responsible for leveraging the findings from the Documentation Analyst to design innovative and practical solutions 
            for coding problems. This involves creating a detailed design document that outlines the proposed solutions, including 
            pseudo-code and architectural diagrams, to ensure clear and efficient implementation.

            Instructions
            ------------
            1. Review the findings from the Documentation Analyst.
            2. Design comprehensive solutions based on these findings.
            3. Create detailed pseudo-code and architectural diagrams to illustrate the proposed solutions.
            ------------
            Documentation: {documentation}"""),
            expected_output=dedent(f"""\
            Your final deliverable should be a detailed design document that includes:
            1. An overview of the proposed solutions.
            2. Pseudo-code for the solutions.
            3. Architectural diagrams illustrating the design and structure of the solutions.
            4. Justifications for the chosen solutions and design approaches.
            """),
            agent=agent,
            async_execution=True
        )

    def solution_implementation_task(self, agent, design_document):
        return Task(description=dedent(f"""\
            You are responsible for transforming the solution designs from the Solution Architect into fully functional code. 
            This involves coding the solutions, testing for efficiency and effectiveness, and ensuring that the final product 
            meets all specified requirements and performs optimally in its intended environment.

            Instructions
            ------------
            1. Review the design document provided by the Solution Architect.
            2. Implement the solutions in code.
            3. Test the code for efficiency, effectiveness, and correctness.
            4. Ensure the code meets all requirements and performs well in its intended environment.

            ------------
            Documentation: {design_document}"""),
            expected_output=dedent(f"""\
            Your final deliverable should be:
            1. Fully functional code that implements the solutions as per the design document.
            2. Documentation for the code, including: 
                a. Explanation of how to deploy and use the code. 
                b. Details of any dependencies or setup required.
            3. Test results demonstrating the efficiency and effectiveness of the code.
            """),
            agent=agent,
            async_execution=True
        )
    def python_repl_execution_task(self, agent, python_code):
        return Task(
            description=dedent(f"""\
            You are responsible for writing, building, executing, and testing Python code using the PythonREPLTool. This involves taking the provided Python code, running it, and testing its functionality to ensure it works as intended.

            Instructions
            ------------
            1. Review the provided Python code.
            2. Build and execute the code using the PythonREPLTool.
            3. Test the code to ensure it functions correctly and meets the requirements.
            4. Debug and fix any issues that arise during execution.

            Python Code: {python_code}
            """),
            expected_output=dedent(f"""\
            Your final deliverable should include:
            1. The output of the executed Python code.
            2. A report detailing any issues found during execution and how they were resolved.
            3. Confirmation that the code meets the requirements and functions correctly.
            4. Any relevant test cases and their results.
            """),
            agent=agent
        )
        
    def code_review_task(self, agent, code):
        return Task(
            description=dedent(f"""\
            You are responsible for reviewing the code developed by the Code Developer. 
            This involves ensuring that the code adheres to coding standards, is free of bugs, 
            and is optimized for performance and security.

            Instructions
            ------------
            1. Review the provided code for adherence to coding standards.
            2. Identify and document any bugs or issues found in the code.
            3. Optimize the code for performance and security.
            4. Provide detailed feedback and recommendations for improvements.

            Code: {code}
            """),
            expected_output=dedent(f"""\
            Your final deliverable should include:
            1. A detailed report on the code review, including:
                a. Adherence to coding standards.
                b. Identified bugs or issues and their fixes.
                c. Performance and security optimizations.
            2. Feedback and recommendations for further improvements.
            3. Confirmation that the code is ready for deployment.
            """),
            agent=agent
        )