#steps/step0.py
import streamlit as st
from steps.utils import save_data_to_json


def run_step0():
    st.header("0. Project Information")
    with st.expander("Instructions"):
        st.write("Enter basic information about your AI project.")
    with st.form(key='projectinformation'):
        project_name = st.text_input("Project Name:", value=st.session_state.data.get('Project Name', ''), help="Enter the name of the project.")
        project_description = st.text_area("Project Description:", height=150, value=st.session_state.data.get('Project Description', ''), help="Describe the project and its objectives.")
        idea_owner = st.text_input("Idea Owner:", value=st.session_state.data.get('Idea Owner', ''), help="Enter the name of the Idea Owner.")
        idea_team = st.text_input("Idea Team:", value=st.session_state.data.get('Idea Team', ''), help="Enter the names of the Idea Team.")
        innovation_manager = st.text_input("Innovation Manager:", value=st.session_state.data.get('Innovation Manager', ''), help="Enter the name of the Innovation Manager.")
        submitted = st.form_submit_button("Save")
    if submitted:
        # Save data to session state
        st.session_state.data['Project Name'] = project_name
        st.session_state.data['Project Description'] = project_description
        st.session_state.data['Idea Owner'] = idea_owner
        st.session_state.data['Idea Team'] = idea_team
        st.session_state.data['Innovation Manager'] = innovation_manager
         # Hier kommt das Persistieren in die JSON-Datei:
        save_data_to_json(st.session_state.data)
        st.success("Data saved.")