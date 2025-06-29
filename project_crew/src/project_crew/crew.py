from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from project_crew.tools.custom_tool import search_internet, search_instagram, open_page

@CrewBase
class ProjectCrew():
    """ProjectCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def market_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['market_researcher'], # type: ignore[index]
            tools=[
                search_instagram,
                search_internet,
                open_page
            ],
            verbose=True
        )

    @agent
    def content_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['content_strategist'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def visual_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['visual_creator'],
            verbose=True,
            allow_delegation=False
        )
        
    @agent
    def copywriter(self) -> Agent:
        return Agent(
            config=self.agents_config['copywriter'],
            verbose=True
        )


    @task
    def market_research(self) -> Task:
        return Task(
            config=self.tasks_config["market_research"],
            agent=self.market_researcher(),
            output_file="market_research.md",
        )

    @task
    def content_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config["content_strategy"],
            agent=self.content_strategist(),
        )

    @task
    def visual_content_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config["visual_content_creation"],
            agent=self.visual_creator(),
            output_file="visual-content.md",
        )

    @task
    def copywriting_task(self) -> Task:
        return Task(
            config=self.tasks_config["copywriting"],
            agent=self.copywriter(),
        )

    @task
    def report_final_content_strategy(self) -> Task:
        return Task(
            config=self.tasks_config["report_final_content_strategy"],
            agent=self.content_strategist(),
            output_file="final-content-strategy.md",
        )



    @crew
    def crew(self) -> Crew:
        """Creates the ProjectCrew crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
