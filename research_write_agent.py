import warnings
warnings.filterwarnings('ignore')

from crewai import Agent, Task, Crew, LLM
import pkg_resources 

# Print version of CrewAI
crewai_version = pkg_resources.get_distribution("crewai").version
print(crewai_version)

# Tips for creating agents:
# - Provide agents with a `role`, `goal` and `backstory`.
# - It has been seen that LLMs perform better when they are role playing.
# Use multiple_strings instead of triple quotes for multi-line strings. 

# Create a local llm model for the agents
llm_models = ["ollama/llama3.2", "ollama/deepseek-r1:8b"]
llm = LLM(llm_models[1], base_url="http://localhost:11434")

# Agent 1: Planner
planner = Agent(
    role="Content Planner",
    goal="Plan engaging and factually accurate conent on {topic}",
    backstory="You're working on planning a blog article on {topic}. "
    "You need to plan the structure, headings, and subheadings for the article."
    "You collect information that helps the "
    "audience learn something "
    "and make informed decisions. "
    "Your work is the basis for "
    "the Content Writer to write an article on this topic.",
    expected_output="A comprehensive content plan document "
        "with an outline, audience analysis, "
        "SEO keywords, and resources.",
    allow_delegation=False,
    verbose=True,
    llm=llm  # Model for image-related tasks
)

# Agent 2: Writer
writer = Agent(
    role="Content Writer",
    goal="Write insightful and factually accurate opinion piece "
        "about the topic: {topic}",
    backstory="You're working on a writing "
              "a new opinion piece about the topic: {topic}. "
              "You base your writing on the work of "
              "the Content Planner, who provides an outline "
              "and relevant context about the topic. "
              "You follow the main objectives and "
              "direction of the outline, "
              "as provide by the Content Planner. "
              "You also provide objective and impartial insights "
              "and back them up with information "
              "provide by the Content Planner. "
              "You acknowledge in your opinion piece "
              "when your statements are opinions "
              "as opposed to objective statements.",
              expected_output="A well-written blog post in markdown format, "
                    "ready for publication, "
                    "each section should have 2 or 3 paragraphs.",
    allow_delegation=False,
    verbose=True,
    llm=llm
)

# Agent 3: Editor
editor = Agent(
    role="Content Editor",
    goal="Edit a given blog post to align with "
         "the writing style of the organization.",
    backstory="You are an editor who receives a blog post "
        "from the Content Writer. "
        "Your goal is to review the blog post "
        "to ensure that it follows journalistic best practices,"
        "provides balanced viewpoints "
        "when providing opinions or assertions, "
        "and also avoids major controversial topics "
        "or opinions when possible.",
        expected_output="A well-written blog post in markdown format, "
                    "ready for publication, " 
                    "each section should have 2 or 3 paragraphs.",
    allow_delegation=False,
    verbose=True,
    llm=llm
)

# Task: Plan, Write
plan = Task(
    description=("Plan a blog article on the topic: {topic}"
        "1. Prioritize the latest trends, key players, "
            "and noteworthy news on {topic}.\n"
        "2. Identify the target audience, considering "
            "their interests and pain points.\n"
        "3. Develop a detailed content outline including "
            "an introduction, key points, and a call to action.\n"
        "4. Include SEO keywords and relevant data or sources."
    ),
    expected_output="A comprehensive content plan document "
        "with an outline, audience analysis, "
        "SEO keywords, and resources.",
    agent=planner,
)

write = Task(
    description=(
        "1. Use the content plan to craft a compelling "
            "blog post on {topic}.\n"
        "2. Incorporate SEO keywords naturally.\n"
		"3. Sections/Subtitles are properly named "
            "in an engaging manner.\n"
        "4. Ensure the post is structured with an "
            "engaging introduction, insightful body, "
            "and a summarizing conclusion.\n"
        "5. Proofread for grammatical errors and "
            "alignment with the brand's voice.\n"
    ),
    expected_output="A well-written blog post "
        "in markdown format, ready for publication, "
        "each section should have 2 or 3 paragraphs.",
    agent=writer,
)

edit = Task(
    description=("Proofread the given blog post for "
                 "grammatical errors and "
                 "alignment with the brand's voice."),
    expected_output="A well-written blog post in markdown format, "
                    "ready for publication, "
                    "each section should have 2 or 3 paragraphs.",
    agent=editor
)

crew = Crew(
    agents = [planner, writer, editor],
    tasks = [plan, write, edit],
    verbose=True
)

# Run the crew
result = crew.kickoff(inputs={"topic": "Using LLMs for Design and Manufacturing of electronic and physical products"})
print(result)
