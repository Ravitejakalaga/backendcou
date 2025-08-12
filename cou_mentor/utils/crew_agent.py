import os
from crewai import Agent

os.environ["OPENAI_API_KEY"] = "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"
os.environ["OPENAI_MODEL"] = "deepseek/deepseek-prover-v2:free"
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

mentor_profile_agent = Agent(
    role="Mentor Selector",
    goal="Select the top mentors based on display name, bio, and expertise for the student's needs.",
    backstory=(
        "You are a career advisor helping students find the best mentors. "
        "You evaluate mentor profiles and select the most suitable matches."
    ),
    openai_api_key=os.environ["OPENAI_API_KEY"],
    openai_model=os.environ["OPENAI_MODEL"]
)
