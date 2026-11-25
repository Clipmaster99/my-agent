import os
import streamlit as st
from agent import run_agent, FORMAT
from demo import SECTIONS, SUPPORTED_LANGUAGES

st.set_page_config(
    page_title="Adult Forum Story Rule Breakage Agent",
    page_icon="🛡️",
    layout="wide"
)

# Title & Explainer
st.title("🛡️ Adult Forum Story Rule Breakage Agent")
st.markdown("**An agent for ME (the moderator) that turns the complete story into a line-by-line rule breakdown against Rule A, Rule B, and Rule C.**")

# Adult forum context banner
st.caption("ℹ️ **Platform Scope:** Adult Site (consensual adult stories permitted). Moderation strictly enforces **Rule A (Interfaith)**, **Rule B (Underage under 18)**, and **Rule C (Rape, Gay, Gore, Doxxing, Caste)**.")

# Sample loader
sample_story_demo = (
    "Title: Interfaith Romance in Delhi\n\n"
    "Priya was wearing her sacred mangalsutra while sitting in the room. "
    "She spoke with her neighbor Rohan about their secret relationship. "
    "Later, they had passionate consensual sex in the bedroom until morning. "
    "If anyone wants more stories or cheap hotel rooms, call on WhatsApp +91-98765-43210. "
    "Her friend said this was forced sex and almost like rape."
)

if "story_text" not in st.session_state:
    st.session_state["story_text"] = sample_story_demo

def load_sample():
    st.session_state["story_text"] = sample_story_demo

col_btn, _ = st.columns([1, 4])
with col_btn:
    st.button("📋 Load Test Sample Story", on_click=load_sample)

# Text area
story_input = st.text_area(
    "Enter or paste the complete member story to review (in any Indian language or English):",
    key="story_text",
    height=180
)

run_clicked = st.button("🚀 Run Rule Review", type="primary")

if run_clicked:
    if not story_input.strip():
        st.error("Please enter or paste a story to review.")
    else:
        with st.spinner("Reviewing story against internet duplicates, Rule A, Rule B, and Rule C..."):
            results = run_agent(story_input)

        st.markdown("---")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Infractions", results["total_violations"])
        col2.metric("Rule A (Interfaith)", results["rule_counts"]["Rule A"])
        col3.metric("Rule B (Underage)", results["rule_counts"]["Rule B"])
        col4.metric("Rule C (Other)", results["rule_counts"]["Rule C"])

        st.markdown("---")
        st.subheader("📋 Moderation Breakdown Report")

        report = results["final_report"]

        # Display Sections
        for section_name in SECTIONS:
            with st.container(border=True):
                st.markdown(f"### {section_name}")
                if section_name in report:
                    content = report[section_name]
                    st.markdown(content)
                else:
                    st.write("Not enough information")

# Small footer
st.markdown("---")
st.caption("Built by Clipmaster99 at Zero to Live, Future Proof India")
