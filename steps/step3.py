import streamlit as st

def run_step3():
    st.header("3. Scalability, Sustainability, and Feasibility")
    with st.expander("Instructions"):
        st.write("Evaluate the project's ability to handle future growth, be sustainable in the long term, "
                 "and its technical feasibility on a scale from 0 to 10 (low to high).")

    # Custom scale descriptions for each slider category
    SCALE_DESCRIPTIONS = {
        "scalability": {
            0: "Cannot scale at all",
            10: "Scales perfectly to any growth"
        },
        "sustainability": {
            0: "Not sustainable at all",
            10: "Completely sustainable for the long term"
        },
        "technical_feasibility": {
            0: "Technically impossible",
            10: "Easily implementable"
        },
        "data_availability": {
            0: "No data available or poor quality",
            10: "Complete, high-quality data readily available"
        },
        "technical_skills": {
            0: "No relevant technical skills in the team",
            10: "Highly skilled technical team"
        },
        "tech_compatibility": {
            0: "Completely incompatible",
            10: "Fully compatible with existing infrastructure"
        }
    }

    # Formular für die Hauptbewertung
    with st.form(key='scalability_sustainability'):
        scalability = st.slider(
            "3.1 Scalability of the Project:",
            min_value=0,
            max_value=10,
            value=st.session_state.data.get('Scalability', 5),
            help=f"Scale: 0 = '{SCALE_DESCRIPTIONS['scalability'][0]}', "
                 f"10 = '{SCALE_DESCRIPTIONS['scalability'][10]}'"
        )
        sustainability = st.slider(
            "3.2 Sustainability of the Project:",
            min_value=0,
            max_value=10,
            value=st.session_state.data.get('Sustainability', 5),
            help=f"Scale: 0 = '{SCALE_DESCRIPTIONS['sustainability'][0]}', "
                 f"10 = '{SCALE_DESCRIPTIONS['sustainability'][10]}'"
        )
        technical_level = st.slider(
            "3.3 Technical Feasibility:",
            min_value=0,
            max_value=10,
            value=st.session_state.data.get('Technical Feasability', 5),
            help=f"Scale: 0 = '{SCALE_DESCRIPTIONS['technical_feasibility'][0]}', "
                 f"10 = '{SCALE_DESCRIPTIONS['technical_feasibility'][10]}'"
        )
        data_availability = st.slider(
            "3.4 Data Availability and Quality:",
            min_value=0,
            max_value=10,
            value=st.session_state.data.get('Data Availability', 5),
            help=f"Scale: 0 = '{SCALE_DESCRIPTIONS['data_availability'][0]}', "
                 f"10 = '{SCALE_DESCRIPTIONS['data_availability'][10]}'"
        )
        technical_skills = st.slider(
            "3.5 Technical Skills in the Team:",
            min_value=0,
            max_value=10,
            value=st.session_state.data.get('Technical Skills', 5),
            help=f"Scale: 0 = '{SCALE_DESCRIPTIONS['technical_skills'][0]}', "
                 f"10 = '{SCALE_DESCRIPTIONS['technical_skills'][10]}'"
        )
        tech_compatibility = st.slider(
            "3.6 Technology Compatibility with Existing IT Infrastructure:",
            min_value=0,
            max_value=10,
            value=st.session_state.data.get('Technology Compatibility', 5),
            help=f"Scale: 0 = '{SCALE_DESCRIPTIONS['tech_compatibility'][0]}', "
                 f"10 = '{SCALE_DESCRIPTIONS['tech_compatibility'][10]}'"
        )

        submitted = st.form_submit_button("Save")

    # Risiko-Abschnitt außerhalb des Formulars
    st.subheader("3.4 Risk Assessment")
    risks = st.session_state.data.get('Risks', [])
    if 'Risks' not in st.session_state.data:
        st.session_state.data['Risks'] = []

    # Neues Risiko hinzufügen
    with st.expander("Add New Risk"):
        new_risk_name = st.text_input("Risk Name:", help="Enter a description of the risk.")
        risk_probability = st.slider(
            "Probability (0-10):",
            min_value=0,
            max_value=10,
            value=5,
            help="Rate the probability of the risk occurring."
        )
        risk_impact = st.slider(
            "Impact (0-10):",
            min_value=0,
            max_value=10,
            value=5,
            help="Rate the impact of the risk if it occurs."
        )
        if st.button("Add Risk"):
            if new_risk_name:
                expected_risk = risk_probability * risk_impact
                risks.append({
                    'name': new_risk_name,
                    'probability': risk_probability,
                    'impact': risk_impact,
                    'expected_risk': expected_risk
                })
                st.session_state.data['Risks'] = risks
                st.success(f"Risk '{new_risk_name}' added.")
            else:
                st.error("Please provide a name for the risk.")

    # Vorhandene Risiken anzeigen und entfernen
    if risks:
        st.write("### Existing Risks")
        for idx, risk in enumerate(risks):
            st.write(f"**{idx+1}. {risk['name']}**")
            st.write(f"- Probability: {risk['probability']}")
            st.write(f"- Impact: {risk['impact']}")
            st.write(f"- **Expected Risk: {risk['expected_risk']}**")
            if st.button(f"Remove Risk {idx+1}", key=f"remove_risk_{idx}"):
                risks.pop(idx)
                st.session_state.data['Risks'] = risks
                st.success(f"Risk '{risk['name']}' removed.")
                st.stop()  # Stoppt die Ausführung und aktualisiert die Ansicht

    # Daten speichern
    if submitted:
        st.session_state.data['Scalability'] = scalability
        st.session_state.data['Sustainability'] = sustainability
        st.session_state.data['Technical Feasability'] = technical_level
        st.session_state.data['Data Availability'] = data_availability
        st.session_state.data['Technical Skills'] = technical_skills
        st.session_state.data['Technology Compatibility'] = tech_compatibility
        st.success("Data saved.")
