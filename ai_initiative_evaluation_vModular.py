import streamlit as st

# Set page configuration at the very top
st.set_page_config(page_title="AI Initiative Evaluation", layout="wide")

# Import JSON functions from utils.py
from steps.utils import load_data_from_json, save_data_to_json

# Import steps
from steps.step0 import run_step0
from steps.step1 import run_step1
from steps.step2 import run_step2
from steps.step3 import run_step3
from steps.step4 import run_step4
from steps.step5 import run_step5
from steps.step_report import run_step_report
# from steps.step6 import run_step6
# from steps.step7 import run_step7
# from steps.step8 import run_step8
# from steps.step9 import run_step9
# ... ggf. weitere Steps ...

# Ensure Streamlit initializes the session state correctly
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0  # Start at step 0 on first run

if 'progress' not in st.session_state:
    st.session_state.progress = 0  # Initialize progress

# Load session data if available
if 'data' not in st.session_state:
    loaded_data = load_data_from_json()  # <--- nutzt unsere Hilfsfunktion
    st.session_state.data = loaded_data if loaded_data else {}

# Schritte definieren
steps = [
    run_step0,
    run_step1,
    run_step2,
    run_step3,
    run_step4,
    run_step5,
    run_step_report,
    # run_step6,
    # run_step7,
    # ...
    # generate_report,
]

step_names = [
    "0. Project Information",
    "1. Define Business Objectives",
    "2. Describe AI Usage",
    "3. Scalability, Sustainability, Feasibility and Risks",
    "4. Estimate Revenue, Costs, and ROI",
    "5. Cost-Benefit Analysis",
    "6. Generate Report"
]

# Ensure state updates correctly after first run
if "force_reset" not in st.session_state:
    st.session_state.force_reset = True  # Prevents auto-jumping to last step
    st.session_state.current_step = 0  # Forces starting at step 0

# Fortschrittsanzeige und Navigation
st.sidebar.title("Navigation")
selected_step = st.sidebar.radio(
    "Schritte auswählen", 
    range(len(steps)), 
    index=st.session_state.current_step,  # Ensure correct step on start
    format_func=lambda x: step_names[x]
)

# Update current step when selection changes
st.session_state.current_step = selected_step

# Fortschrittsanzeige
st.sidebar.markdown("---")
st.sidebar.write(f"Fortschritt: {int((selected_step + 1) / len(steps) * 100)}%")
st.sidebar.progress((selected_step + 1) / len(steps))

# Starte den aktuellen Schritt
steps[selected_step]()
