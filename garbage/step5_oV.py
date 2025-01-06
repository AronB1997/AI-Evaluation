# steps/step5_oV.py
import streamlit as st
import pandas as pd

def run_step5_oV():
    st.header("5. Advanced Utility Analysis and Overall Score")

    st.write("Please assign a weight between 1 and 10 for each criterion (1 = not important, 10 = very important).")

    # Weightings Form
    with st.form(key='weightings'):
        # Qualitative Criteria
        st.subheader("Weights for Qualitative Criteria")
        scalability_weight = st.slider("Weight for Scalability:", 1, 10, 5)
        sustainability_weight = st.slider("Weight for Sustainability:", 1, 10, 5)
        technical_feasability_weight = st.slider("Weight for Technical Feasability:", 1, 10, 5)
        data_availability_weight = st.slider("Weight for Data Availability and Quality:", 1, 10, 5)
        technical_skills_weight = st.slider("Weight for Technical Skills in the Team:", 1, 10, 5)
        tech_compatibility_weight = st.slider("Weight for Technology Compatibility:", 1, 10, 5)

        # Financial Criteria
        st.subheader("Weights for Financial Criteria")
        roi_weight = st.slider("Weight for ROI:", 1, 10, 5)
        break_even_weight = st.slider("Weight for Break-Even Point:", 1, 10, 5)
        profit_weight = st.slider("Weight for Estimated Profit:", 1, 10, 5)

        # Risk Criterion
        st.subheader("Weight for Risk Criterion")
        risk_weight = st.slider("Weight for Risk:", 1, 10, 5)

        submitted = st.form_submit_button("Calculate")

    if submitted:
        # Retrieve data from st.session_state
        data = st.session_state.data

        # Check if all necessary data is available
        required_fields = ['Scalability', 'Sustainability', 'Technical Feasability',
                           'Data Availability', 'Technical Skills', 'Technology Compatibility',
                           'Development Costs', 'Risk Buffer', 'Annual Costs',
                           'Annual Revenue', 'Years to Analyze', 'Risks']
        if not all(field in data for field in required_fields):
            st.error("Please ensure all previous steps are completed.")
            return

        # Qualitative Scores
        qualitative_scores = {
            'Scalability': (data['Scalability'], scalability_weight),
            'Sustainability': (data['Sustainability'], sustainability_weight),
            'Technical Feasability': (data['Technical Feasability'], technical_feasability_weight),
            'Data Availability and Quality': (data['Data Availability'], data_availability_weight),
            'Technical Skills in the Team': (data['Technical Skills'], technical_skills_weight),
            'Technology Compatibility': (data['Technology Compatibility'], tech_compatibility_weight)
        }

        # Financial Calculations
        total_fixed_costs = data['Development Costs'] + data['Risk Buffer']
        cumulative_costs = [total_fixed_costs + data['Annual Costs'] * year for year in range(data['Years to Analyze'] + 1)]
        cumulative_revenues = [data['Annual Revenue'] * year for year in range(data['Years to Analyze'] + 1)]
        total_costs = cumulative_costs[-1]
        total_revenue = cumulative_revenues[-1]
        estimated_profit = total_revenue - total_costs
        roi = (estimated_profit / total_costs * 100) if total_costs > 0 else 0

        # Calculate Break-Even Year
        break_even_year = None
        for year in range(1, data['Years to Analyze'] + 1):
            if cumulative_revenues[year] >= cumulative_costs[year]:
                break_even_year = year
                break

        # Normalize Financial Metrics
        financial_scores = {}

        # ROI Normalization
        if roi <= 0:
            roi_score = 1
        elif roi <= 10:
            roi_score = 3
        elif roi <= 20:
            roi_score = 5
        elif roi <= 30:
            roi_score = 7
        else:
            roi_score = 10
        financial_scores['ROI'] = (roi_score, roi_weight)

        # Break-Even Point Normalization
        if break_even_year:
            break_even_score = max(1, 11 - break_even_year)  # Earlier years are better
        else:
            break_even_score = 1
        financial_scores['Break-Even Point'] = (break_even_score, break_even_weight)

        # Estimated Profit Normalization
        profit_ratio = estimated_profit / total_costs if total_costs > 0 else 0
        if profit_ratio <= 0:
            profit_score = 1
        elif profit_ratio <= 0.1:
            profit_score = 3
        elif profit_ratio <= 0.2:
            profit_score = 5
        elif profit_ratio <= 0.3:
            profit_score = 7
        else:
            profit_score = 10
        financial_scores['Estimated Profit'] = (profit_score, profit_weight)

        # Risk Normalization
        risks = data.get('Risks', [])
        num_risks = len(risks)
        if num_risks > 0:
            max_total_risk = 100 * num_risks  # Max risk per risk item is 100 (10 probability * 10 impact)
            total_risk = sum(risk['probability'] * risk['impact'] for risk in risks)
            normalized_risk_score = 10 - (total_risk / max_total_risk * 10)
            normalized_risk_score = max(0, normalized_risk_score)  # Ensure score doesn't go negative
        else:
            normalized_risk_score = 10  # No risks means best possible score
        risk_scores = {'Risk': (normalized_risk_score, risk_weight)}

        # Calculate Total Utility Value
        total_weight = sum(weight for _, weight in list(qualitative_scores.values()) +
                           list(financial_scores.values()) + list(risk_scores.values()))
        total_score = 0

        st.write("### Detailed Results:")
        # Qualitative Criteria
        for criterion, (score, weight) in qualitative_scores.items():
            weighted_score = score * weight
            total_score += weighted_score
            st.write(f"- **{criterion}:** Score = {score}, Weight = {weight}, Utility Value = {weighted_score}")

        # Financial Criteria
        for criterion, (score, weight) in financial_scores.items():
            weighted_score = score * weight
            total_score += weighted_score
            st.write(f"- **{criterion}:** Normalized Score = {score}, Weight = {weight}, Utility Value = {weighted_score}")

        # Risk Criterion
        for criterion, (score, weight) in risk_scores.items():
            weighted_score = score * weight
            total_score += weighted_score
            st.write(f"- **{criterion}:** Normalized Score = {score:.2f}, Weight = {weight}, Utility Value = {weighted_score:.2f}")

        # Calculate Normalized Total Score
        normalized_total_score = total_score / total_weight

        st.success(f"The overall project score is: {normalized_total_score:.2f} out of 10")

        # Display Total Expected Risk
        if risks:
            total_expected_risk = sum(risk['expected_risk'] for risk in risks)
            st.write(f"### Total Risk:")
            st.write(f"- **Cumulative Expected Risk:** {total_expected_risk}")

