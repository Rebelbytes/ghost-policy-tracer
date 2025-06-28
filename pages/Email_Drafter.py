
# Step 3 of the Ghost Policy Detector.
# This page:
# - Uses case summary and policy profile to generate a formal email.
# - The email asks the insurer (e.g., LIC) to help verify if a policy exists.
# - User can copy or download the generated draft.

import streamlit as st                          # Streamlit for UI
from llama_api import query_llama               # Function to get response from LLaMA model

#  PAGE CONFIGURATION 
st.set_page_config(page_title="Step 3: Email Drafter", page_icon="✉️")
st.title("✉️ Step 3: Draft Email to Insurer")

#CHECK PRIOR DATA 
required_keys = ["case_text", "case_summary", "policy_profile"]
if not all(k in st.session_state for k in required_keys):
    st.warning("⚠️ No case data found. Please complete previous steps.")
    st.stop()

#GENERATE EMAIL (ONCE)
if "email_draft" not in st.session_state:
    with st.spinner("Drafting email..."):
        email = query_llama(f"""
You are an assistant helping someone write to an insurance company.

Write a formal email that:
- Explains the background briefly: {st.session_state['case_summary']}
- Says the family believes the deceased may have had a LIC policy, but details are missing.
- Requests help verifying if a policy exists.
- Asks for next steps or required documents.
- Does NOT mention any policy number since it is unknown.

Be professional and polite.
""")
        st.session_state["email_draft"] = email

# DISPLAY EMAIL
st.markdown("### 📧 Suggested Email")
st.text_area("Email Body", st.session_state["email_draft"], height=300)

# DOWNLOAD OPTION
st.download_button("📩 Download Email", st.session_state["email_draft"], file_name="insurance_email.txt")

#RETURN TO HOME PAGE
st.page_link("Home.py", label="🏠 Back to Home")
