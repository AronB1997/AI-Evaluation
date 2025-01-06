import streamlit as st
from steps.step0 import run_step0
from steps.step1 import run_step1
from steps.step2 import run_step2
from steps.step3 import run_step3
from steps.step4 import run_step4
from steps.step5 import run_step5
#from steps.step6 import run_step6
#from steps.step7 import run_step7
#from steps.step8 import run_step8
#from steps.step9 import run_step9
#from steps.step10 import run_step10
#from steps.step11 import run_step11
#from steps.step12 import run_step12
#from steps.report import generate_report

# Globale Konfiguration
st.set_page_config(page_title="AI Initiative Evaluation", layout="wide")

# Fortschrittsanzeige initialisieren
if 'progress' not in st.session_state:
    st.session_state.progress = 0

if 'data' not in st.session_state:
    st.session_state.data = {}

if 'current_step' not in st.session_state:
    st.session_state.current_step = 0

# Schritte definieren
steps = [
    run_step0,
    run_step1,
    run_step2,
    run_step3,
    run_step4,
    run_step5,
    #run_step6,
    #run_step7,
    #run_step8,
    #run_step9,
    #run_step10,
    #run_step11,
    #run_step12,
    #generate_report,
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

# Fortschrittsanzeige und Navigation
st.sidebar.title("Navigation")
selected_step = st.sidebar.radio(
    "Schritte auswählen", range(len(steps)), format_func=lambda x: step_names[x]
)
st.sidebar.markdown("---")
st.sidebar.write(f"Fortschritt: {int((selected_step + 1) / len(steps) * 100)}%")
st.sidebar.progress((selected_step + 1) / len(steps))

# Starte den aktuellen Schritt
steps[selected_step]()
