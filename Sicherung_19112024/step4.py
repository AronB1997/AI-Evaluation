# steps/step4.py
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def run_step4():
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
        st.subheader("4.3 Analysis and Visualizations")

        # Create time points with monthly intervals for more precise calculation
        time = np.linspace(0, years_to_analyze, num=years_to_analyze * 12 + 1)

        # Calculate cumulative costs and revenues
        cumulative_costs = total_fixed_costs + annual_costs * time
        cumulative_revenues = annual_revenue * time

        # Break-Even Calculation
        break_even_point = None
        for i in range(1, len(time)):
            if cumulative_revenues[i] >= cumulative_costs[i]:
                # Linear interpolation to find the exact break-even point
                y1 = cumulative_revenues[i-1] - cumulative_costs[i-1]
                y2 = cumulative_revenues[i] - cumulative_costs[i]
                x1 = time[i-1]
                x2 = time[i]
                if y2 - y1 != 0:
                    break_even_point = x1 - y1 * (x2 - x1) / (y2 - y1)
                else:
                    break_even_point = time[i]
                break

        # ROI Calculation
        total_revenue = cumulative_revenues[-1]
        total_costs = cumulative_costs[-1]
        estimated_profit = total_revenue - total_costs
        roi = (estimated_profit / total_costs * 100) if total_costs > 0 else 0

        # Plot: Break-Even Chart
        st.write("### Break-Even Chart")
        plt.figure(figsize=(8, 5))
        plt.plot(time, cumulative_revenues, label="Cumulative Revenues")
        plt.plot(time, cumulative_costs, label="Cumulative Costs", linestyle='--', color='red')
        if break_even_point is not None:
            plt.axvline(break_even_point, color='green', linestyle='--', label=f"Break-Even (Year {break_even_point:.2f})")
        plt.title("Break-Even Analysis")
        plt.xlabel("Years")
        plt.ylabel("Euros (€)")
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)

        # Break-Even Point Display
        if break_even_point is not None:
            st.write(f"### Break-Even Point")
            st.write(f"The project reaches the break-even point in **year {break_even_point:.2f}**.")
        else:
            st.write("### Break-Even Point")
            st.write("The project does not reach the break-even point within the specified time frame.")

        # Key Financial Insights
        st.write("### Key Financial Insights")
        st.metric("Total Costs", f"{total_costs:.2f} €")
        st.metric("Total Revenue", f"{total_revenue:.2f} €")
        st.metric("Estimated Profit", f"{estimated_profit:.2f} €")
        st.metric("ROI", f"{roi:.2f} %")
