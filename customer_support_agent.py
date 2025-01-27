"""
This script defines agents and tasks for providing customer support using the crewAI framework.
It includes agents for support and quality assurance.
"""

import warnings
warnings.filterwarnings('ignore')

from crewai import Agent, Task, Crew, LLM
from crewai_tools import ScrapeWebsiteTool
from crewai.tools import BaseTool

llm_models = ["ollama/llama3.2", "ollama/deepseek-r1:8b"]
llm = LLM(llm_models[1], base_url="http://localhost:11434")

class MyCustomScrapingTool(BaseTool):
    """
    Custom tool for scraping a given website.
    """
    name: str = "Website Scraping Tool"
    description: str = "Scrape the given website."

    def _run(self) -> str:
        docs_scrape_tool = ScrapeWebsiteTool()        
        response = docs_scrape_tool.run(website_url="https://docs.crewai.com/how-to/Creating-a-Crew-and-kick-it-off/")
        return response
    
support_agent = Agent(
    role="Senior Support Representative",
    goal="Be the most friendly and helpful support "
    "representative in your team",
    backstory=(
        "You work at crewAI (https://crewai.com) and "
        "are now working on providing "
        "support to {customer}, a super important customer "
        "for your company."
        "You need to make sure that you provide the best support!"
        "Make sure to provide full complete answers, "
        "and make no assumptions."
    ),
    allow_delegation=False,
    verbose=True,
    llm=llm,
    tools=[MyCustomScrapingTool()],
)

support_quality_assurance_agent = Agent(
    role="Support Quality Assurance Specialist",
    goal="Get recognition for providing the "
    "best support quality assurance in your team",
    backstory=(
        "You work at crewAI (https://crewai.com) and "
        "are now working with your team "
        "on a request from {customer} ensuring that "
        "the support representative is "
        "providing the best support possible.\n"
        "You need to make sure that the support representative "
        "is providing full"
        "complete answers, and make no assumptions."
    ),
    allow_delegation=True,
    verbose=True,
    llm=llm
)

inquiry_resolution = Task(
    description=(
        "{customer} has reached out to the support team "
        "with a super important inquiry: {inquiry}. "
        "Make sure to use everything you know "
        "to provide the best support possible."
        "You must strive to provide a complete "
        "and accurate response to the customer's inquiry."
        "Include {person} and {customer} when writing the email response."
        "Response should include Subramaniam Jayanti as the support representative."
    ),
    expected_output= (
        "A detailed, informative response to the "
        "customer's inquiry that addresses "
        "all aspects of their question.\n"
        "The response should include references "
        "to everything you used to find the answer, "
        "including external data or solutions. "
        "Ensure the answer is complete, "
        "leaving no questions unanswered, and maintain a helpful and friendly "
        "tone throughout."
    ),
    agent=support_agent
)

quality_assurance_review = Task(
    description=("Review the response drafted by the Senior Support Representative for {customer}'s inquiry. "
        "Ensure that the answer is comprehensive, accurate, and adheres to the "
        "high-quality standards expected for customer support.\n"
        "Verify that all parts of the customer's inquiry "
        "have been addressed "
        "thoroughly, with a helpful and friendly tone.\n"
        "Check for references and sources used to "
        "find the information, "
        "ensuring the response is well-supported and "
        "leaves no questions unanswered."
    ),
    expected_output=(
        "A final, detailed, and informative email response "
        "ready to be sent to the customer. \n"
        "This response should fully address the "
        "customer's inquiry, incorporating all "
        "relevant feedback and improvements.\n"
        "Don't be too formal, we are a chill and cool company "
        "but maintain a professional and friendly tone throughout."
    ),
    agent=support_quality_assurance_agent
)

crew = Crew(
    agents=[support_agent, support_quality_assurance_agent],
    tasks=[inquiry_resolution, quality_assurance_review],
    verbose=True
)

if __name__ == "__main__":
    inputs = {
        "customer": "Shrewd Analytics LLC",
        "person": "Subramaniam Jayanti",
        "inquiry": "I need help with setting up a crew of agents"
                "and kicking it off. Can you provide guidance?"
    }
    result = crew.kickoff(inputs=inputs)
    print(result)