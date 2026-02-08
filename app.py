import streamlit as st
from market_research_agent.main import run
import datetime

# Page configuration
st.set_page_config(page_title="AI Market Researcher", page_icon="🚀")

st.title("🚀 Startup Market Research Agent")
st.markdown("Enter your startup idea below, and our AI agents will research the market, competitors, and strategy.")

# User Input
with st.form("research_form"):
    topic = st.text_input("What is your startup idea?", placeholder="e.g. An AI-powered Market Researcher ")
    submit_button = st.form_submit_button("Start Research")

if submit_button:
    if not topic:
        st.warning("Please enter an idea first!")
    else:
        st.info(f"Agents are now researching: **{topic}**...")
        
        # This captures the output from your crew
        try:
            # We pass the topic into the inputs dictionary your Crew expects
            inputs = {
                'topic': topic,
                'current_date': datetime.datetime.now().strftime("%Y-%m-%d")
            }
            
            # Assuming your main.py has a function that accepts inputs
            # If not, we might need to tweak your main.py slightly
            result = run() 
            
            st.success("Research Completed!")
            st.subheader("Final Report")
            st.markdown(result)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")