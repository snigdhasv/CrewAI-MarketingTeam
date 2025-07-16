import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "project_crew", "src")))

import streamlit as st
from dotenv import load_dotenv
from project_crew import main as crew_main

load_dotenv()

st.title("CrewAI Instagram Content Strategy Generator")

st.write("""
This app runs your CrewAI pipeline to generate:
- Market research
- Content calendar
- Visual content descriptions
- Copywriting
- Final content strategy report
""")

description = st.text_area("Enter the Instagram page description:")
topic = st.text_input("Enter the topic of the week:")

st.markdown("### 🎯 Brand & Audience Information")

brand_tone = st.selectbox("Select brand tone:", ["Casual", "Professional", "Playful", "Inspirational", "Luxury", "Bold", "Minimalist", "Other"])
target_demographics = st.text_area("Describe your target audience demographics (age, gender, interests, location, etc.):")
brand_goals = st.multiselect("Select brand goals:", ["Increase Engagement", "Drive Conversions", "Grow Followers", "Raise Awareness", "Launch Product", "Other"])
custom_goals = st.text_input("Other goals (optional):")

if st.button("Run CrewAI Pipeline"):
    if not description or not topic:
        st.error("Please provide both the Instagram page description and the topic of the week.")
    else:
        with st.spinner("Running CrewAI pipeline. This may take a moment..."):
            # Patch input() to provide our values
            import builtins
            orig_input = builtins.input
            def fake_input(prompt):
                if "description" in prompt.lower():
                    return description
                elif "topic" in prompt.lower():
                    return topic
                elif "brand_tone" in prompt.lower():
                    return brand_tone
                elif "demographics" in prompt.lower():
                    return target_demographics
                elif "goal" in prompt.lower():
                    return ", ".join(brand_goals) + ("; " + custom_goals if custom_goals else "")
                return ""

            builtins.input = fake_input
            try:
                crew_main.run()
            except Exception as e:
                st.error(f"Error running CrewAI pipeline: {e}")
            finally:
                builtins.input = orig_input

        st.success("Pipeline complete! Displaying results:")

        # Display outputs
        output_files = [
            ("Market Research", "market_research.md"),
            ("Visual Content Descriptions", "visual-content.md"),
            ("Final Content Strategy Report", "final-content-strategy.md"),
        ]
        for label, path in output_files:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                st.subheader(label)
                st.markdown(content)
                st.download_button(f"Download {label}", content, file_name=os.path.basename(path))
            else:
                st.warning(f"{label} not found at {path}.") 