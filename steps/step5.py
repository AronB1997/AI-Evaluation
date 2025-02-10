# steps/step5.py
import streamlit as st
import pandas as pd
from steps.utils import save_data_to_json  # <-- ACHTUNG: Funktion aus steps/utils.py importieren

def run_step5():
    st.header("5. Advanced Utility Analysis and Overall Score")

    st.write(
        "Please assign a weight between 0 and 100 to each criterion to indicate its importance "
        "for evaluating the project.\n"
        "A weight of 0 means the criterion is not important, while a weight of 100 means it is critically important."
    )

    # -- Gewichtungen erfassen -------------------------------------------
    with st.form(key='weightings'):
        st.subheader("Weights for Qualitative Criteria")
        alignment_weight = st.slider("Weight for Alignment with Business Objectives:", 0, 100, 50)
        time_capacity_weight = st.slider("Weight for Time Capacity:", 0, 100, 50)
        scalability_weight = st.slider("Weight for Scalability:", 0, 100, 50)
        sustainability_weight = st.slider("Weight for Sustainability:", 0, 100, 50)
        technical_feasability_weight = st.slider("Weight for Technical Feasibility:", 0, 100, 50)
        technical_skills_weight = st.slider("Weight for Technical Skills in the Company:", 0, 100, 50)
        tech_compatibility_weight = st.slider("Weight for Technology Compatibility:", 0, 100, 50)

        st.subheader("Weights for Data-related Criteria")
        data_availability_weight = st.slider("Weight for Data Availability:", 0, 100, 50)
        data_quality_weight = st.slider("Weight for Data Quality:", 0, 100, 50)

        st.subheader("Weights for Financial Criteria")
        roi_weight = st.slider("Weight for ROI:", 0, 100, 50)
        break_even_weight = st.slider("Weight for Break-Even Point:", 0, 100, 50)

        st.subheader("Weight for Risk Criterion")
        risk_weight = st.slider("Weight for Risk:", 0, 100, 50)

        submitted = st.form_submit_button("Calculate")

    if submitted:
        # -- Vorhandene Daten aus st.session_state holen -----------------
        data = st.session_state.data

        # -- Prüfen, ob alle erforderlichen Felder vorhanden sind -------
        required_fields = [
            'Alignment with Business Objectives', 'Time Capacity',
            'Scalability', 'Sustainability', 'Technical Feasability',
            'Technical Skills', 'Technology Compatibility',
            'Data Availability', 'Data Quality',
            'Development Costs', 'Risk Buffer',
            'Annual Costs', 'Annual Revenue', 'Years to Analyze', 'Risks'
        ]
        if not all(field in data for field in required_fields):
            st.error("Please ensure all previous steps are completed.")
            return

        # -- Red Flag Check (Step 3 Werte) ------------------------------
        step3_values = {
            "Alignment with Business Objectives": data.get('Alignment with Business Objectives', None),
            "Time Capacity": data.get('Time Capacity', None),
            "Scalability": data.get('Scalability', None),
            "Sustainability": data.get('Sustainability', None),
            "Technical Feasibility": data.get('Technical Feasability', None),
            "Technical Skills in the Company": data.get('Technical Skills', None),
            "Technology Compatibility": data.get('Technology Compatibility', None),
            "Data Availability": data.get('Data Availability', None),
            "Data Quality": data.get('Data Quality', None),
        }

        # Sammle alle Kategorien, die einen Wert von 0 haben
        zero_categories = [key for key, value in step3_values.items() if value == 0]

        if zero_categories:
            st.error(
                f"Red Flag: You have chosen '0' for the following Step 3 categories: {', '.join(zero_categories)}. "
                "Thereby, the project cannot be approved. Please go back to Step 3 and adjust these values."
            )
            return  # Stoppe, keine weitere Berechnung

        # -- Qualitative Scores -----------------------------------------
        qualitative_scores = {
            'Alignment with Business Objectives': (data['Alignment with Business Objectives'], alignment_weight),
            'Time Capacity': (data['Time Capacity'], time_capacity_weight),
            'Scalability': (data['Scalability'], scalability_weight),
            'Sustainability': (data['Sustainability'], sustainability_weight),
            'Technical Feasibility': (data['Technical Feasability'], technical_feasability_weight),
            'Technical Skills in the Company': (data['Technical Skills'], technical_skills_weight),
            'Technology Compatibility': (data['Technology Compatibility'], tech_compatibility_weight),
            'Data Availability': (data['Data Availability'], data_availability_weight),
            'Data Quality': (data['Data Quality'], data_quality_weight),
        }

        # -- Finanzielle Werte berechnen --------------------------------
        total_fixed_costs = data['Development Costs'] + data['Risk Buffer']
        cumulative_costs = [
            total_fixed_costs + data['Annual Costs'] * year
            for year in range(data['Years to Analyze'] + 1)
        ]
        cumulative_revenues = [
            data['Annual Revenue'] * year
            for year in range(data['Years to Analyze'] + 1)
        ]
        total_costs = cumulative_costs[-1]
        total_revenue = cumulative_revenues[-1]
        estimated_profit = total_revenue - total_costs

        roi = (estimated_profit / total_costs * 100) if total_costs > 0 else 0

        # -- Break-Even Year berechnen ----------------------------------
        break_even_year = None
        for year in range(1, data['Years to Analyze'] + 1):
            if cumulative_revenues[year] >= cumulative_costs[year]:
                break_even_year = year
                break

        # -- ROI Normalization ------------------------------------------
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

        # -- Break-Even Normalization -----------------------------------
        if break_even_year:
            # Je früher Break-Even erreicht wird, desto besser -> Score höher
            break_even_score = max(1, 11 - break_even_year)
        else:
            # Break-Even nie erreicht -> sehr schlecht
            break_even_score = 1

        financial_scores = {
            'ROI': (roi_score, roi_weight),
            'Break-Even Point': (break_even_score, break_even_weight),
        }

        # -- Risiko Normalisierung --------------------------------------
        risks = data.get('Risks', [])
        if risks:
            num_risks = len(risks)
            max_total_risk = 100 * num_risks  # 10 * 10 = 100 pro Risk, multipliziert mit Anzahl
            total_risk = sum(risk['probability'] * risk['impact'] for risk in risks)
            normalized_risk_score = 10 - (total_risk / max_total_risk * 10)
            normalized_risk_score = max(0, normalized_risk_score)  # Score nicht negativ werden lassen
        else:
            normalized_risk_score = 10  # Keine Risiken -> bester Score

        risk_scores = {
            'Risk': (normalized_risk_score, risk_weight)
        }

        # -- Gesamten Score berechnen -----------------------------------
        total_weight = 0
        total_score = 0

        # Details anzeigen
        st.write("### Detailed Results:")

        # Qualitative Scores berechnen
        for criterion, (score, weight) in qualitative_scores.items():
            weighted_score = score * weight
            total_score += weighted_score
            total_weight += weight
            st.write(f"- **{criterion}:** Score = {score}, Weight = {weight}, Utility Value = {weighted_score}")

        # Finanzielle Scores
        for criterion, (score, weight) in financial_scores.items():
            weighted_score = score * weight
            total_score += weighted_score
            total_weight += weight
            st.write(f"- **{criterion}:** Normalized Score = {score}, Weight = {weight}, Utility Value = {weighted_score}")

        # Risiko Score
        for criterion, (score, weight) in risk_scores.items():
            weighted_score = score * weight
            total_score += weighted_score
            total_weight += weight
            st.write(f"- **{criterion}:** Normalized Score = {score:.2f}, Weight = {weight}, Utility Value = {weighted_score:.2f}")

        # Normalized Total Score (0-10)
        normalized_total_score = total_score / total_weight if total_weight else 0
        st.success(f"The overall project score is: {normalized_total_score:.2f} out of 10")

        # -- Ergebnisse im Session State speichern + JSON-Update --------
        st.session_state.data['weights'] = {
            'Alignment with Business Objectives': alignment_weight,
            'Time Capacity': time_capacity_weight,
            'Scalability': scalability_weight,
            'Sustainability': sustainability_weight,
            'Technical Feasibility': technical_feasability_weight,
            'Technical Skills': technical_skills_weight,
            'Technology Compatibility': tech_compatibility_weight,
            'Data Availability': data_availability_weight,
            'Data Quality': data_quality_weight,
            'ROI': roi_weight,
            'Break-Even Point': break_even_weight,
            'Risk': risk_weight
        }
        st.session_state.data['final_score'] = normalized_total_score

        # Daten persistieren
        save_data_to_json(st.session_state.data)
        st.success("Final results and weights have been saved to JSON.")
