#steps/step2.py
import streamlit as st

def run_step2():
    st.header("2. Describe AI Usage")
    with st.expander("Instructions"):
        st.write("Describe the planned use of AI in this project.")
    ai_technology_options = ["", "Machine Learning", "Deep Learning", "Natural Language Processing", "Computer Vision", "Expert Systems", "Robotics", "Other"]
    with st.form(key='ai_usage'):
        ai_technology = st.selectbox(
            "2.1 Type of AI Technology:",
            ai_technology_options,
            index=ai_technology_options.index(st.session_state.data.get('Type of AI Technology', '')) if st.session_state.data.get('Type of AI Technology', '') in ai_technology_options else 0,
            help="Select the type of AI technology to be used in the project."
        )
        ai_purpose = st.text_area(
            "2.2 Purpose of AI Usage:",
            height=100,
            value=st.session_state.data.get('Purpose of AI Usage', ''),
            help="Describe what the AI usage aims to achieve."
        )
        application_area = st.text_input(
            "2.3 Application Area:",
            value=st.session_state.data.get('Application Area', ''),
            help="Specify the area where AI will be applied (e.g., production, sales, customer service)."
        )
        innovation_type_options = ["", "Completely New Solution", "Product Extension", "Process Improvement", "Optimization of Existing Systems"]
        innovation_type = st.selectbox(
            "2.4 Type of Innovation:",
            innovation_type_options,
            index=innovation_type_options.index(st.session_state.data.get('Type of Innovation', '')) if st.session_state.data.get('Type of Innovation', '') in innovation_type_options else 0,
            help="Select the type of innovation that the project represents."
        )
        submitted = st.form_submit_button("Save")
    if submitted:
        st.session_state.data['Type of AI Technology'] = ai_technology
        st.session_state.data['Purpose of AI Usage'] = ai_purpose
        st.session_state.data['Application Area'] = application_area
        st.session_state.data['Type of Innovation'] = innovation_type
        st.success("Data saved.")
