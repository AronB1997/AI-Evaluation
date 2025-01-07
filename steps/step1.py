# steps/step1.py
import streamlit as st

def run_step1():
    st.header("1. Define Business Objectives")
    with st.expander("Instructions"):
        st.write("Define your project's strategic objectives and how this project contributes to them.")
    with st.form(key='business_goals'):
        lagging_goals = st.text_area(
            "1.1 Lagging Goal/Strategic Goal (one per line):",
            height=150,
            value='\n'.join(st.session_state.data.get('Lagging Goals', [])),
            help="Enter your project's long-term strategic goals. Focus on the result (what you want to achieve)."
        )
        leading_goals = st.text_area(
            "1.2 Leading Goal/Operative Goal (one per line):",
            height=150,
            value='\n'.join(st.session_state.data.get('Leading Goals', [])),
            help="Enter your project's short-term operative goals. Focus on the process/actions (what you need to do to achieve the result)."
        )
        kpis = st.text_area(
            "1.3 Key Performance Indicators (KPIs) (one per line):",
            height=150,
            value='\n'.join(st.session_state.data.get('KPIs', [])),
            help="Define the KPIs that will measure progress toward your goals."
        )
        # Entfernt: Alignment of the Project with Business Objectives (1.4)
        
        frequency_review = st.text_area(
            "1.4 Frequency of the Target Review:",
            height=150,
            value=st.session_state.data.get('Frequency target review', ''),
            help="Describe how the targets of the project will be monitored over time."
        )
        submitted = st.form_submit_button("Save")
    
    if submitted:
        st.session_state.data['Lagging Goals'] = [goal.strip() for goal in lagging_goals.split('\n') if goal.strip()]
        st.session_state.data['Leading Goals'] = [goal.strip() for goal in leading_goals.split('\n') if goal.strip()]
        st.session_state.data['KPIs'] = [kpi.strip() for kpi in kpis.split('\n') if kpi.strip()]
        # Entfernt: st.session_state.data['Alignment with Business Objectives'] = alignment
        st.session_state.data['Frequency target review'] = frequency_review
        st.success("Data saved.")
