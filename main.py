import warnings
from market_research_agent.crew import market_research_agent
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")



def run():
    """
    Run the crew.
    """
    inputs = {
        "product_idea": "An AI powered tool that summarizes youtube videos on my channel and posts the summary on various social media platforms like LinkedIn, Instagram, Facebook,X, WhatsApp"
    }

    try:
        result=market_research_agent().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")