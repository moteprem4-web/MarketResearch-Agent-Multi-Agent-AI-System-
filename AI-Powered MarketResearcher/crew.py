from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os

#we provide the access of the webscrap  based on the current market trends
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, SeleniumScrapingTool
from dotenv import load_dotenv
from crewai import Agent, LLM

load_dotenv()

# create the tools for the agent
web_search_tool = SerperDevTool()
web_scraping_tool = ScrapeWebsiteTool()
selenium_scraping_tool = SeleniumScrapingTool()

#all code in the one variable so all the website and tools in the one variable
toolkit = [web_search_tool, web_scraping_tool, selenium_scraping_tool]
# 1. Define the Hugging Face LLM
hf_llm = LLM(
    model="huggingface/meta-llama/Llama-3.1-8B-Instruct", # Replace with your preferred model
    api_key=os.getenv("HF_TOKEN"),
    temperature=0.7
    
)
# define the crew class
@CrewBase
class market_research_agent():
    """MarketResearchCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # provide the path for configuration files
    agents_config = "config/agents.yaml" 
    tasks_config = "config/tasks.yaml"
    
    # ================ Agents ========================
    
    @agent
    #name of the agent
    def market_research_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["market_research_specialist"],
            tools=toolkit, #above all webscarping tools saved it in the toolkit varibale

             llm=hf_llm 
        )

    @agent
    def competitive_intelligence_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["competitive_intelligence_analyst"],
            tools=toolkit,
            llm=hf_llm 
            

        )
        
    @agent
    def customer_insights_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["customer_insights_researcher"],
            tools=toolkit,
            llm=hf_llm 
        )
        
    @agent
    def product_strategy_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config["product_strategy_advisor"],
            tools=toolkit,
            llm=hf_llm 
        )
        
    @agent
    def business_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["business_analyst"],
            tools=toolkit,
            llm=hf_llm 
        )
        
    # ================ Tasks ======================
    
    @task
    def market_research_task(self) -> Task:
        return Task(
            config=self.tasks_config["market_research_task"]
        )
        
    @task
    def competitive_intelligence_task(self) -> Task:
        return Task(
            config=self.tasks_config["competitive_intelligence_task"],
            context=[self.market_research_task()] #context is used to understand the context of the previous one
        )
        
    @task
    def customer_insights_task(self) -> Task:
        return Task(
            config=self.tasks_config["customer_insights_task"],
            context=[self.market_research_task(),
                     self.competitive_intelligence_task()]
        )
        
    @task
    def product_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config["product_strategy_task"],
            context=[self.market_research_task(),
                     self.competitive_intelligence_task(),
                     self.customer_insights_task()]
        )
        
    @task
    #all tool output done all the work ok
    def business_analyst_task(self) -> Task:
        return Task(
            config=self.tasks_config["business_analyst_task"],
            context=[self.market_research_task(),
                     self.competitive_intelligence_task(),
                     self.customer_insights_task(),
                     self.product_strategy_task()],
            output_file="reports/report.md"
        )
        
    # ================= Crew ===========================
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents, #all agents
            tasks=self.tasks, #all tools
            process=Process.sequential #name of the process

        )