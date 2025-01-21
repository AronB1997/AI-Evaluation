# steps/step3.py
import streamlit as st

def run_step3():
    st.header("3. Scalability, Sustainability, and Feasibility")
    with st.expander("Instructions"):
        st.write("Evaluate the project's ability to handle future growth, be sustainable in the long term, "
                 "and its technical feasibility on a scale from 0 to 10 (low to high).")

    # Custom scale descriptions for each slider category
    SCALE_DESCRIPTIONS = {
        "alignment": {
            0:  (
                "No alignment with business objectives at all. "
                "The idea directly conflicts with strategic goals or offers no apparent benefit."
            ),
            5:  (
                "Partially aligns with some, but not all, business objectives. "
                "May support certain initiatives but requires additional justification."
            ),
            10: (
                "Fully aligns with core strategic goals and vision. "
                "Directly supports priority objectives with clear business value."
            )
        },
        "scalability": {
            0:  (
                "Cannot scale beyond a small pilot or localized use. "
                "Any attempt to increase usage (e.g., more users, higher data volume, "
                "additional locations) would result in performance or cost challenges "
                "that are not feasible to address."
            ),
            5:  (
                "Can handle moderate growth with some effort, such as increasing the user base "
                "by 2-3x or expanding to a few additional locations. "
                "Significant re-architecture or investment may be required for larger expansions."
            ),
            10: (
                "Can easily scale to large or even global usage (e.g., 5x-10x or more) "
                "with minimal changes. Architecture or design supports on-demand scaling "
                "of users, data, and operations without drastic cost or performance issues."
            )
        },
        "time_capacity": {
            0:  "No time capacity available (0 hours/week).",
            5:  (
                "Moderate time capacity (5 hours/week). The contributor(s) can allocate a "
                "few hours but may not be able to handle urgent or unexpected tasks."
            ),
            10: (
                "Maximum time capacity (10 hours/week). The contributor(s) can reliably "
                "dedicate time, handle new tasks quickly, and adjust if the project scope expands."
            )
        },
        "sustainability": {  # Economic sustainability only
            0:  (
                "Not economically viable. "
                "The cost structure or revenue model makes it financially unsustainable."
            ),
            5:  (
                "Moderately viable. "
                "The idea can be sustained if certain cost or revenue targets are met, "
                "but there's still risk of low profitability."
            ),
            10: (
                "Highly sustainable and profitable from an economic standpoint. "
                "The cost model is well-optimized, and the revenue model supports "
                "long-term growth and profitability."
            )
        },
        "technical_feasibility": {
            0:  (
                "No viable technical approach exists with current resources or technology. "
                "Requires breakthroughs or resources not currently available."
            ),
            5:  (
                "Moderately feasible. "
                "A workable solution exists but requires significant effort, specialized tools, "
                "or major changes to current practices."
            ),
            10: (
                "Easily implementable with existing technology and minimal changes "
                "to current processes. The team already has the know-how and resources."
            )
        },
        "data_availability": {
            0:  (
                "No relevant data available. "
                "Data either doesn't exist or cannot be accessed for legal or technical reasons."
            ),
            5:  (
                "Partial data available. "
                "Some relevant data sets can be accessed, but there are gaps or restrictions "
                "that limit overall coverage."
            ),
            10: (
                "Complete and readily accessible data. "
                "All essential data for the project is collected, well-organized, "
                "and available for immediate use."
            )
        },
        "data_quality": {
            0:  (
                "Extremely poor data quality (unreliable, inconsistent). "
                "Data would require extensive cleaning or may be too flawed to use at scale."
            ),
            5:  (
                "Moderate data quality. "
                "Some inconsistencies or missing values exist. "
                "Additional validation or cleaning is necessary but achievable."
            ),
            10: (
                "High-quality data (accurate, well-structured, validated). "
                "Minimal effort needed to integrate or analyze."
            )
        },
        "technical_skills": {
            0:  (
                "No relevant technical expertise available in the company. "
                "Would require external hires or consultants for any progress."
            ),
            5:  (
                "Some expertise available, but may require significant upskilling "
                "or external support for complex tasks."
            ),
            10: (
                "Strong in-house technical expertise covering all required areas. "
                "The team can handle complex issues or expansions with existing skills."
            )
        },
        "tech_compatibility": {
            0:  (
                "Completely incompatible with current systems/infrastructure. "
                "Extensive overhaul or replacement of existing systems required."
            ),
            5:  (
                "Partially compatible; moderate integration work needed. "
                "Current systems can adapt but may require bridging components or updates."
            ),
            10: (
                "Fully compatible with existing infrastructure. "
                "Only minimal configuration changes or upgrades are needed."
            )
        }
    }

    # Formular für die Hauptbewertung
    with st.form(key='scalability_sustainability'):
        alignment = st.slider(
            "3.1 Alignment with Business Objectives:",
            min_value=0,
            max_value=10,
            value=st.session_state.data.get('Alignment with Business Objectives', 5),
            help=f"Scale:  \n"
                f"0 = '{SCALE_DESCRIPTIONS['alignment'][0]}'  \n"
                f"5 = '{SCALE_DESCRIPTIONS['alignment'][5]}'  \n"
                f"10 = '{SCALE_DESCRIPTIONS['alignment'][10]}'"
        )
        time_capacity = st.slider(
            "3.2 Time Capacity for the Project:",
            min_value=0,
            max_value=10,
            value=st.session_state.data.get('Time Capacity', 5),
            help=f"Scale:  \n"
                f"0 = '{SCALE_DESCRIPTIONS['time_capacity'][0]}'  \n"
                f"5 = '{SCALE_DESCRIPTIONS['time_capacity'][5]}'  \n"
                f"10 = '{SCALE_DESCRIPTIONS['time_capacity'][10]}'"
        )
        scalability = st.slider(
            "3.3 Scalability of the Project:",
            min_value=0,
            max_value=10,
            value=st.session_state.data.get('Scalability', 5),
            help=f"Scale:  \n"
                f"0 = '{SCALE_DESCRIPTIONS['scalability'][0]}'  \n"
                f"5 = '{SCALE_DESCRIPTIONS['scalability'][5]}'  \n"
                f"10 = '{SCALE_DESCRIPTIONS['scalability'][10]}'"
        )
        sustainability = st.slider(
            "3.4 Sustainability of the Project:",
            min_value=0,
            max_value=10,
            value=st.session_state.data.get('Sustainability', 5),
            help=f"Scale:  \n"
                f"0 = '{SCALE_DESCRIPTIONS['sustainability'][0]}'  \n"
                f"5 = '{SCALE_DESCRIPTIONS['sustainability'][5]}'  \n"
                f"10 = '{SCALE_DESCRIPTIONS['sustainability'][10]}'"
        )
        technical_level = st.slider(
            "3.5 Technical Feasibility:",
            min_value=0,
            max_value=10,
            value=st.session_state.data.get('Technical Feasability', 5),
            help=f"Scale:  \n"
                f"0 = '{SCALE_DESCRIPTIONS['technical_feasibility'][0]}'  \n"
                f"5 = '{SCALE_DESCRIPTIONS['technical_feasibility'][5]}'  \n"
                f"10 = '{SCALE_DESCRIPTIONS['technical_feasibility'][10]}'"
        )
        technical_skills = st.slider(
            "3.6 Technical Skills in the Company:",
            min_value=0,
            max_value=10,
            value=st.session_state.data.get('Technical Skills', 5),
            help=f"Scale:  \n"
                f"0 = '{SCALE_DESCRIPTIONS['technical_skills'][0]}'  \n"
                f"5 = '{SCALE_DESCRIPTIONS['technical_skills'][5]}'  \n"
                f"10 = '{SCALE_DESCRIPTIONS['technical_skills'][10]}'"
        )
        tech_compatibility = st.slider(
            "3.7 Technology Compatibility with Existing IT Infrastructure:",
            min_value=0,
            max_value=10,
            value=st.session_state.data.get('Technology Compatibility', 5),
            help=f"Scale:  \n"
                f"0 = '{SCALE_DESCRIPTIONS['tech_compatibility'][0]}'  \n"
                f"5 = '{SCALE_DESCRIPTIONS['tech_compatibility'][5]}'  \n"
                f"10 = '{SCALE_DESCRIPTIONS['tech_compatibility'][10]}'"
        )
        data_availability = st.slider(
            "3.8 Data Availability:",
            min_value=0,
            max_value=10,
            value=st.session_state.data.get('Data Availability', 5),
            help=f"Scale:  \n"
                f"0 = '{SCALE_DESCRIPTIONS['data_availability'][0]}'  \n"
                f"5 = '{SCALE_DESCRIPTIONS['data_availability'][5]}'  \n"
                f"10 = '{SCALE_DESCRIPTIONS['data_availability'][10]}'"
        )
        data_quality = st.slider(
            "3.9 Data Quality:",
            min_value=0,
            max_value=10,
            value=st.session_state.data.get('Data Quality', 5),
            help=f"Scale:  \n"
                f"0 = '{SCALE_DESCRIPTIONS['data_quality'][0]}'  \n"
                f"5 = '{SCALE_DESCRIPTIONS['data_quality'][5]}'  \n"
                f"10 = '{SCALE_DESCRIPTIONS['data_quality'][10]}'"
        )
        
        submitted = st.form_submit_button("Save")

    # Risiko-Abschnitt außerhalb des Formulars
    st.subheader("3.10 Risk Assessment")
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
        st.session_state.data['Alignment with Business Objectives'] = alignment
        st.session_state.data['Time Capacity'] = time_capacity
        st.session_state.data['Scalability'] = scalability
        st.session_state.data['Sustainability'] = sustainability
        st.session_state.data['Technical Feasability'] = technical_level
        st.session_state.data['Technical Skills'] = technical_skills
        st.session_state.data['Technology Compatibility'] = tech_compatibility
        st.session_state.data['Data Availability'] = data_availability
        st.session_state.data['Data Quality'] = data_quality
        st.success("Data saved.")
