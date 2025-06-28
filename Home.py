import streamlit as st

# Basic configuration
st.set_page_config(page_title="Ghost Policy Detector", layout="centered")

# Title and welcome
st.title(" Ghost Policy Detector - GenAI Agent")

st.markdown("""
Welcome to the **Ghost Policy Detector** — a tool designed to help families track down forgotten or unclaimed **life insurance policies**, especially when documents or policy numbers are missing.

We use AI to:
- Understand your case details
- Ask smart follow-up questions
- Suggest the most likely insurance profiles
- Draft a formal email to insurance companies

---

### Process Overview:
1. **Describe your case** in natural language  
2. **Answer a clarifying question**  
3. **Get insurance guidance and a draft email**

""")

# Start the flow
st.page_link("pages/Describe_Case.py", label="👉 Start with Describe Case")
