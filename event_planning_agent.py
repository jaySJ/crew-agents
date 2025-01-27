"""
This script defines agents and tasks for planning an event using the crewAI framework.
It includes agents for venue coordination, logistics management, and marketing communications.
"""

import warnings
warnings.filterwarnings('ignore')

from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from crewai.tools import BaseTool
import json
from pprint import pprint

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
        response = docs_scrape_tool.run()
        return response
    
class MySearchTool(BaseTool):
    """
    Custom tool for searching the internet for relevant information.
    """
    name: str = "Search Tool"
    description: str = "Search the internet for relevant information."

    def _run(self) -> str:
        search_tool = SerperDevTool()        
        response = search_tool.run()
        return response
    
# Agent 1: Venue Coordination Agent
venue_coordination_agent = Agent(
    role="Venue Coordinator",
    goal="Find the best venue for the event"
        "based on the requirements and budget.",
    tools=[MySearchTool(), MyCustomScrapingTool()],
    verbose=True,
    backstory=(
        "With a keen sense of space and understanding of event logistics, "
        "you excel at finding and securing the perfect venue that fits the event's theme,"
        "audience, size, and budget constraints."
    ),
    llm=llm
)

# Agent 2: Logistics Manager
logistics_manager_agent = Agent(
    role="Logistics Manager",
    goal=(
        "Manage all logistics for the event, "
        "including transportation, equipment, and catering."
    ),
    tools=[MySearchTool(), MyCustomScrapingTool()],
    verbose=True,
    backstory=(
        "You're a master of organization and logistics, ensuring that everything "
        "runs smoothly and efficiently."
    ),
    llm=llm
)

# Agent 3: Marketing and Communications Manager
marketing_communications_agent = Agent(
    role="Marketing and Communications Manager",
    goal=(
        "Effectively market the event, create enthusiasm for potential participants and "
        "communicate with the participants."
    ),
    tools=[MySearchTool(), MyCustomScrapingTool()],
    verbose=True,
    backstory=(
        "You're a creative and communicative marketing expert with a "
        "knack for creating buzz and excitement "
        "around events to maximize event exposure and participation."
    ),
    llm=llm
)

from pydantic import BaseModel, Field
class VenueDetails(BaseModel):
    name: str
    address: str
    capacity: int
    price: int
    booking_status: str

venue_task = Task(
    description="Find a venue in {event_city} "
                "that meets the criteria for an event on {event_topic}.",
    expected_output="All the details of the venue you found to accommodate the event.",
    human_input=True,
    output_json=VenueDetails,
    output_file="venue_details.json",
    agent=venue_coordination_agent
)

logistics_task = Task(
    description="Coordinate the catering and equipment for an event "
                 "with {expected_participants} participants "
                 "on {tentative_date}.",
    expected_output="Confirmation of all logistics arrangements "
                    "including catering and equipment setup.",
    human_input=True,
    async_execution=True,
    agent=logistics_manager_agent
)

marketing_task = Task(
    description="Promote the event on {event_topic} "
                "aiming to engage at least {expected_participants} potential attendees.",
    expected_output="Report on marketing activities and attendee engagement formatted as markdown.",
    output_file="marketing_report.md",  # Outputs the report as a text file
    agent=marketing_communications_agent
)

event_management_crew = Crew(
    agents=[venue_coordination_agent, 
            logistics_manager_agent, 
            marketing_communications_agent],
    tasks=[venue_task, 
           logistics_task, 
           marketing_task],
    verbose=True
)

if __name__ == "__main__":
    # Run the event management crew
    event_details = {
        'event_topic': "Tech Innovation Conference",
        'event_description': "A gathering of tech innovators "
                            "and industry leaders "
                            "to explore future technologies.",
        'event_city': "San Francisco",
        'tentative_date': "2025-09-01",
        'expected_participants': 500,
        'budget': 20000,
        'venue_type': "Conference Hall"
    }

    result = event_management_crew.kickoff(inputs=event_details)

    with open('venue_details.json') as f:
        venue_details = json.load(f)
    pprint(venue_details)