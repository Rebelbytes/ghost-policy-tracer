# This page:
# - Takes user input describing an insurance-related case.
# - Uses an LLM (via `query_llama`) to summarize the case.
# - Asks ONE clarifying question to better understand the situation.
# - Stores everything in Streamlit session state for use in Step 2.

import streamlit as st  # Streamlit is used to create the interactive UI
from llama_api import query_llama #This function sends prompts to LLaMA via Ollama and returns the response

# Set up the page
st.set_page_config(page_title="Step 1: Describe Case", page_icon="🧠")
st.title("Step 1: Describe Your Case")

# Step 1: Text input for the user to describe their case
case_text = st.text_area("Please describe your case in detail...", height=200)

# Submit button to process the case
if st.button("Submit Case"):
    with st.spinner("Analyzing your case..."):
        # Store the raw case description
        st.session_state.case_text = case_text

        # Generate a short case summary using LLM
        summary = query_llama(f"""You're an insurance assistant.
Summarize and analyze the user's insurance case below (in 2-3 lines max):

{case_text}
""")
        st.session_state.case_summary = summary

        # Generate a single important follow-up question
        question = query_llama(f"""You're assisting with an insurance investigation.
Based on this user's case:

{case_text}

Ask only ONE important clarifying question to help understand the case better.
""")
        st.session_state.clarifying_question = question

    # Display results to user
    st.success("Case received and analyzed.")
    st.markdown("### Case Summary")
    st.write(st.session_state.case_summary)

    st.markdown("### Clarifying Question")
    st.write(st.session_state.clarifying_question)

# Step 2: User answers the clarifying question
if "clarifying_question" in st.session_state:
    user_answer = st.text_input("Your answer:")
    
    # If the user gives an answer, store it and offer to move to next step
    if user_answer:
        st.session_state.answer_to_question = user_answer
        st.page_link("pages/Case_Profile.py", label="Next: View Policy Guidance")
