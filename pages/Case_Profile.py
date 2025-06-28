# Step 2 of the Ghost Policy Detector.
# This page:
# - Collects case info (description, summary, clarifying Q&A).
# - Sends it to the LLaMA model to infer:
#     - Possible LIC policy type.
#     - Suggested steps for the family.
#     - Claim/recovery guidance.
#     - Estimated likelihood (%) of policy existence.
# - Displays the response and a visual likelihood bar.

import streamlit as st                          # For UI
import re                                       # To extract numeric score
from llama_api import query_llama               # Calls the local LLaMA model

# PAGE SETUP
st.set_page_config(page_title="Step 2: Insurance Guidance", page_icon="📄")
st.title("📄 Step 2: Insurance Guidance")

# CHECK STEP 1 DATA
required_keys = ["case_text", "case_summary", "clarifying_question", "answer_to_question"]
if not all(k in st.session_state for k in required_keys):
    st.warning("⚠️ No case data found. Please complete Step 1 first.")
    st.stop()

# BUILD FULL CONTEXT FOR MODEL
full_context = f"""
Case Summary:
{st.session_state.case_summary}

Clarifying Question:
{st.session_state.clarifying_question}

User's Answer:
{st.session_state.answer_to_question}
"""

# QUERY LLM ONCE
if "policy_profile" not in st.session_state or "policy_likelihood" not in st.session_state:
    with st.spinner("🔍 Analyzing and generating guidance..."):
        profile = query_llama(f"""
You are an insurance assistant.

Given the situation below, provide:
1. The possible type of LIC policy involved.
2. Suggested next steps for the family.
3. Guidance to recover documents or make a claim.
4. A [Likelihood Score] from 0 to 100 indicating how likely it is that a policy exists.

Format like this:

[Policy Analysis]
...

[Next Steps]
...

[Likelihood Score]
<number>

Case Info:
{full_context}
""")
        st.session_state.policy_profile = profile

        # EXTRACT likelihood score
        match = re.search(r"\[Likelihood Score\]\s*(\d{1,3})", profile)
        if match:
            likelihood = int(match.group(1))
        else:
            likelihood = 60  # default fallback
        st.session_state.policy_likelihood = likelihood

# DISPLAY POLICY OUTPUT
profile_text = st.session_state.policy_profile.split("[Likelihood Score]")[0]
likelihood = st.session_state.policy_likelihood

st.markdown("### 📝 Policy Profile & Guidance")
st.write(profile_text.strip())

# DISPLAY LIKELIHOOD BAR
st.markdown("### 📊 Estimated Likelihood of Policy")
st.progress(likelihood / 100)
st.write(f"**Estimated Likelihood:** {likelihood}%")

# NAVIGATION
st.page_link("pages/Email_Drafter.py", label="➡️ Next: Draft Email", icon="✉️")
