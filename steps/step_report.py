import streamlit as st
import openai

# Retrieve API Key from Streamlit secrets
try:
    api_key = st.secrets["ai"]["api_key"]
except KeyError:
    st.error("API Key not found. Please add your OpenAI API key to secrets.toml.")
    st.stop()

# Verify that API Key is correctly formatted
if not api_key.startswith("ai_"):
    st.error("Invalid API Key format. Please check your API key.")
    st.stop()

# Set the custom API base URL for Cosmo Consult AI
base_url = "https://apis.ai.cosmoconsult.com/openai/v1"

def run_step_report():
    st.header("7. Final AI-Generated Project Report")
    st.write("Review all collected data and generate a final summary or 'Exposé' using AI.")

    # Check if data is available
    if 'data' not in st.session_state or not st.session_state.data:
        st.warning("No data found in session_state. Please complete previous steps first.")
        return

    # Optional: Show collected data for debugging
    if st.checkbox("Show collected data (debug)"):
        st.json(st.session_state.data)

    # Generate AI Report Button
    if st.button("Generate AI Report"):
        data = st.session_state.data
        roi = data.get("ROI", "N/A")
        amortization_time = data.get("Amortization Time", "N/A")
        break_even = data.get("Break-Even Point", "N/A")

        # Extract risks from JSON
        risks = "\n".join([f"- {risk['name']} (Probability: {risk['probability']}, Impact: {risk['impact']}, Expected Risk: {risk['expected_risk']})" for risk in data.get('Risks', [])])

        # Construct AI prompt
        messages = [
            {"role": "system", "content": "You are an AI assistant that generates structured project reports enriched with deep insights, industry knowledge, and critical analysis."},
            {"role": "user", "content": f"""
            You are an AI business consultant analyzing an AI project. Generate a structured,
            professional report that classifies the project and provides insights into feasibility,
            financials, and risks. Use your knowledge and industry expertise to enhance the analysis,
            providing valuable insights beyond the given data.

            # **Summary**
            Provide a high-level summary of the project's potential impact, scalability, and feasibility.
            Offer an industry-specific comparison to similar AI initiatives and outline major advantages
            and challenges that should be considered.

            # **Project Overview**
            - **Project Name**: {data.get('Project Name')}
            - **Project Description**: {data.get('Project Description')}
            - **Idea Owner**: {data.get('Idea Owner')}
            - **Idea Team**: {data.get('Idea Team')}
            - **Innovation Manager**: {data.get('Innovation Manager')}
            - **Lagging Goals**: {', '.join(data.get('Lagging Goals', []))}
            - **Leading Goals**: {', '.join(data.get('Leading Goals', []))}
            - **Key Performance Indicators (KPIs)**: {', '.join(data.get('KPIs', []))}

            # **AI Integration**
            - **Type of AI Technology**: {data.get('Type of AI Technology')}
            - **Purpose of AI Usage**: {data.get('Purpose of AI Usage')}
            - **Application Area**: {data.get('Application Area')}
            - **Type of Innovation**: {data.get('Type of Innovation')}

            # **Financial Overview**
            - **Development Costs**: €{data.get('Development Costs')}
            - **Annual Costs**: €{data.get('Annual Costs')}
            - **Projected Annual Revenue**: €{data.get('Annual Revenue')}
            - **ROI**: {roi}%
            - **Amortization Time**: {amortization_time} years
            - **Break-Even Point**: {break_even} years

            # **Challenges and Risks**
            Provide a comparative risk assessment based on real-world AI project failures and successes.
            Highlight any missing considerations that could impact the success of this project.

            | Challenge/Risk | Description |
            |---------------|-------------|
            | **Identified Risks** | {risks if risks else 'No specific risks identified in the initial data.'} |
            | **Potential AI Risks** | AI bias, data privacy issues, model drift |
            | **Scalability Challenges** | Data dependency, computational requirements |
            | **Business Challenges** | Adoption barriers, ROI uncertainty |
            | **Industry Trends and Risks** | Similar AI projects face integration complexities and data management challenges. |

            # **Final Recommendation**
            Provide a professional evaluation of whether this AI project is viable, highlighting
            its strengths and critical risks. Suggest next steps for project refinement and offer
            strategies for overcoming potential barriers to success.
            """}
        ]

        # OpenAI API Request with Custom Base URL and Correct Headers
        client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=1500,
            temperature=0.7,
            extra_headers={"api-key": api_key}
        )

        # Retrieve AI-generated report
        report_text = response.choices[0].message.content.strip()

        # Display AI-generated Report
        st.subheader("AI-Generated Report")
        st.write(report_text)

# Run the report generation function
run_step_report()
