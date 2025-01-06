# steps/step4.py
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def run_step4():
    # Initialize session_state data
    if 'data' not in st.session_state:
        st.session_state.data = {}
    
    st.header("4. Cost, Revenue, and Profit Analysis with Break-Even Chart and ROI")
    with st.expander("Instructions"):
        st.write("""
            Enter the one-time and recurring costs as well as the annual revenue.
            Visualize the break-even point and analyze the ROI.
        """)

    with st.form(key='cost_revenue_form'):
        # Cost Structure
        st.subheader("4.1 Cost Structure")
        development_costs = st.number_input(
            "Development Costs (one-time, in €):",
            min_value=0.0,
            step=500.0,
            value=0.0,
            help="Costs for initial development."
        )
        risk_buffer = st.number_input(
            "Risk Buffer (one-time, in €):",
            min_value=0.0,
            step=500.0,
            value=0.0,
            help="Reserve for unexpected issues."
        )
        annual_costs = st.number_input(
            "Recurring Costs (per year, in €):",
            min_value=0.0,
            step=500.0,
            value=0.0,
            help="Annually recurring operational costs."
        )

        total_fixed_costs = development_costs + risk_buffer

        # Revenue
        st.subheader("4.2 Revenue")
        annual_revenue = st.number_input(
            "Estimated Revenue (per year, in €):",
            min_value=0.0,
            step=500.0,
            value=0.0,
            help="Annual revenue the project will generate."
        )

        # Time Span for Analysis
        years_to_analyze = st.slider(
            "Analysis Period (in years):",
            min_value=1,
            max_value=10,
            value=6
        )

        # Save button
        submitted = st.form_submit_button("Save")
    
    # Save data and perform calculations
    if submitted:
        st.session_state.data['Development Costs'] = development_costs
        st.session_state.data['Risk Buffer'] = risk_buffer
        st.session_state.data['Annual Costs'] = annual_costs
        st.session_state.data['Annual Revenue'] = annual_revenue
        st.session_state.data['Years to Analyze'] = years_to_analyze
        st.success("Data saved.")

    # Visualizations and Analysis
    if submitted:
        # Rest of your visualization code...
        pass  # Replace with your existing code
