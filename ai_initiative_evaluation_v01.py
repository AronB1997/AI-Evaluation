import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np
import base64
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="KI-Initiativen Bewertungsprogramm", layout="wide")

# Titel und Beschreibung
st.title("KI-Initiativen Bewertungsprogramm")
st.markdown("""
Dieses Programm hilft Ihnen dabei, eine spezifische KI-Initiative zu bewerten und zu entscheiden, ob das Projekt sinnvoll ist oder nicht.
Bitte geben Sie die erforderlichen Informationen zu Ihrem Projekt ein und durchlaufen Sie die Schritte zur Bewertung.
""")

# Sidebar für Navigation
st.sidebar.title("Navigation")
steps = [
    "0. Projektinformationen",
    "1. Geschäftsziele definieren",
    "2. KI-Einsatz beschreiben",
    "3. Technische Machbarkeit bewerten",
    "4. Kosten und Ressourcen schätzen",
    "5. Nutzen und ROI schätzen",
    "6. Risikobewertung",
    "7. Skalierbarkeit und Nachhaltigkeit",
    "8. Erfolgsmessung definieren",
    "9. Zusammenfassung der bisherigen Eingaben",
    "10. Entscheidungsfindung",
    "11. Implementierungsplanung",
    "12. Überwachung und Evaluierung",
    "Bericht generieren",
]

# Mapping von Schritten zu Indizes für die Navigation
step_indices = {step: index for index, step in enumerate(steps)}

if 'current_step' not in st.session_state:
    st.session_state.current_step = steps[0]

def next_step():
    current_index = step_indices[st.session_state.current_step]
    if current_index + 1 < len(steps):
        st.session_state.current_step = steps[current_index + 1]

def previous_step():
    current_index = step_indices[st.session_state.current_step]
    if current_index > 0:
        st.session_state.current_step = steps[current_index - 1]

selected_step = st.sidebar.radio("Schritte auswählen", steps, index=step_indices[st.session_state.current_step])

# Dictionaries zum Speichern der Eingaben
if "data" not in st.session_state:
    st.session_state.data = {}

# Funktionen für jeden Schritt

def step0():
    st.header("0. Projektinformationen")
    with st.expander("Anleitung"):
        st.write("Geben Sie grundlegende Informationen zu Ihrem KI-Projekt ein.")
    project_name = st.text_input("Projektname:", value=st.session_state.data.get('Projektname', ''), help="Geben Sie den Namen des Projekts ein.")
    project_description = st.text_area("Projektbeschreibung:", height=150, value=st.session_state.data.get('Projektbeschreibung', ''), help="Beschreiben Sie das Projekt und seine Ziele.")
    project_manager = st.text_input("Projektverantwortlicher:", value=st.session_state.data.get('Projektverantwortlicher', ''), help="Geben Sie den Namen des Projektverantwortlichen an.")
    if st.button("Speichern"):
        st.session_state.data['Projektname'] = project_name
        st.session_state.data['Projektbeschreibung'] = project_description
        st.session_state.data['Projektverantwortlicher'] = project_manager
        st.success("Daten gespeichert.")
        next_step()

def step1():
    st.header("1. Geschäftsziele definieren")
    with st.expander("Anleitung"):
        st.write("Definieren Sie die strategischen Ziele Ihres Unternehmens und wie dieses Projekt dazu beiträgt.")
    strategic_goals = st.text_area(
        "1.1 Strategische Ziele (jeweils in einer neuen Zeile):",
        height=150,
        value='\n'.join(st.session_state.data.get('Strategische Ziele', [])),
        help="Geben Sie die langfristigen strategischen Ziele Ihres Unternehmens an."
    )
    kpis = st.text_area(
        "1.2 Schlüsselkennzahlen (KPIs) (jeweils in einer neuen Zeile):",
        height=150,
        value='\n'.join(st.session_state.data.get('KPIs', [])),
        help="Definieren Sie die KPIs, die den Fortschritt in Richtung Ihrer Ziele messen."
    )
    alignment = st.text_area(
        "1.3 Ausrichtung des Projekts auf Geschäftsziele:",
        height=150,
        value=st.session_state.data.get('Ausrichtung auf Geschäftsziele', ''),
        help="Beschreiben Sie, wie dieses Projekt Ihre Geschäftsziele unterstützt."
    )
    if st.button("Speichern"):
        st.session_state.data['Strategische Ziele'] = strategic_goals.split('\n')
        st.session_state.data['KPIs'] = kpis.split('\n')
        st.session_state.data['Ausrichtung auf Geschäftsziele'] = alignment
        st.success("Daten gespeichert.")
        next_step()

def step2():
    st.header("2. KI-Einsatz beschreiben")
    with st.expander("Anleitung"):
        st.write("Beschreiben Sie den geplanten Einsatz von KI in diesem Projekt.")
    ai_technology_options = ["", "Maschinelles Lernen", "Deep Learning", "Natural Language Processing", "Computer Vision", "Expertensysteme", "Robotics", "Sonstiges"]
    ai_technology = st.selectbox(
        "2.1 Art der KI-Technologie:",
        ai_technology_options,
        index=ai_technology_options.index(st.session_state.data.get('Art der KI-Technologie', '')),
        help="Wählen Sie die Art der KI-Technologie, die im Projekt eingesetzt wird."
    )
    ai_purpose = st.text_area(
        "2.2 Zweck des KI-Einsatzes:",
        height=100,
        value=st.session_state.data.get('Zweck des KI-Einsatzes', ''),
        help="Beschreiben Sie, was mit dem Einsatz der KI erreicht werden soll."
    )
    application_area = st.text_input(
        "2.3 Anwendungsbereich:",
        value=st.session_state.data.get('Anwendungsbereich', ''),
        help="Geben Sie den Bereich an, in dem die KI eingesetzt wird (z.B. Produktion, Vertrieb, Kundenservice)."
    )
    innovation_type_options = ["", "Komplett neue Lösung", "Produkterweiterung", "Prozessverbesserung", "Optimierung bestehender Systeme"]
    innovation_type = st.selectbox(
        "2.4 Art der Innovation:",
        innovation_type_options,
        index=innovation_type_options.index(st.session_state.data.get('Art der Innovation', '')),
        help="Wählen Sie die Art der Innovation, die das Projekt darstellt."
    )
    if st.button("Speichern"):
        st.session_state.data['Art der KI-Technologie'] = ai_technology
        st.session_state.data['Zweck des KI-Einsatzes'] = ai_purpose
        st.session_state.data['Anwendungsbereich'] = application_area
        st.session_state.data['Art der Innovation'] = innovation_type
        st.success("Daten gespeichert.")
        next_step()

def step3():
    st.header("3. Technische Machbarkeit bewerten")
    with st.expander("Anleitung"):
        st.write("Bewerten Sie die Datenverfügbarkeit, technische Fähigkeiten und Technologiekompatibilität.")
    data_availability_options = ["Gut", "Mittel", "Schlecht"]
    data_availability = st.radio(
        "3.1 Datenverfügbarkeit und -qualität:",
        data_availability_options,
        index=data_availability_options.index(st.session_state.data.get('Datenverfügbarkeit', 'Gut')),
        help="Bewerten Sie die Verfügbarkeit und Qualität der erforderlichen Daten."
    )
    technical_skills_options = ["Ausreichend", "Teilweise", "Nicht ausreichend"]
    technical_skills = st.radio(
        "3.2 Technische Fähigkeiten im Team:",
        technical_skills_options,
        index=technical_skills_options.index(st.session_state.data.get('Technische Fähigkeiten', 'Ausreichend')),
        help="Bewerten Sie die technischen Fähigkeiten Ihres Teams zur Umsetzung des Projekts."
    )
    tech_compatibility_options = ["Hoch", "Mittel", "Niedrig"]
    tech_compatibility = st.radio(
        "3.3 Technologiekompatibilität mit bestehender IT-Infrastruktur:",
        tech_compatibility_options,
        index=tech_compatibility_options.index(st.session_state.data.get('Technologiekompatibilität', 'Hoch')),
        help="Bewerten Sie, wie gut das Projekt in Ihre bestehende IT-Infrastruktur passt."
    )
    if st.button("Speichern"):
        st.session_state.data['Datenverfügbarkeit'] = data_availability
        st.session_state.data['Technische Fähigkeiten'] = technical_skills
        st.session_state.data['Technologiekompatibilität'] = tech_compatibility
        st.success("Daten gespeichert.")
        next_step()

def step4():
    st.header("4. Kosten und Ressourcen schätzen")
    with st.expander("Anleitung"):
        st.write("Schätzen Sie die Entwicklungskosten, Betriebskosten und das Risikobudget.")
    
    # Input für Entwicklungskosten, Betriebskosten und Risikobudget
    development_cost = st.number_input(
        "4.1 Entwicklungskosten (€):",
        min_value=0.0,
        step=1000.0,
        format="%.2f",
        value=st.session_state.data.get('Entwicklungskosten', 0.0),
        help="Einmalige Kosten für die Entwicklung des Projekts."
    )
    operational_cost = st.number_input(
        "4.2 Laufende Betriebskosten pro Jahr (€):",
        min_value=0.0,
        step=1000.0,
        format="%.2f",
        value=st.session_state.data.get('Laufende Betriebskosten', 0.0),
        help="Jährliche Kosten für den Betrieb und die Wartung des Projekts."
    )
    risk_budget = st.number_input(
        "4.3 Risikobudget (€):",
        min_value=0.0,
        step=1000.0,
        format="%.2f",
        value=st.session_state.data.get('Risikobudget', 0.0),
        help="Finanzieller Puffer für unvorhergesehene Kosten oder Risiken."
    )
    
    # Berechnung der Anfangsinvestition (Entwicklungskosten + Risikobudget)
    total_initial_cost = development_cost + risk_budget
    st.write(f"**Geschätzte Anfangsinvestition:** € {total_initial_cost:,.2f}")
    
    # Speichern der Daten
    if st.button("Speichern"):
        st.session_state.data['Entwicklungskosten'] = development_cost
        st.session_state.data['Laufende Betriebskosten'] = operational_cost
        st.session_state.data['Risikobudget'] = risk_budget
        st.session_state.data['Anfangsinvestition'] = total_initial_cost
        st.success("Daten gespeichert.")
        next_step()


def step5():
    st.header("5. Nutzen und ROI schätzen")
    with st.expander("Anleitung"):
        st.write("Schätzen Sie den finanziellen Nutzen über die geplante Laufzeit des Projekts.")

    # Input für die Projektlaufzeit und Anlaufzeit
    project_duration = int(st.number_input(
        "Projektlaufzeit in Jahren:",
        min_value=1,
        step=1,
        value=st.session_state.data.get('Projektlaufzeit (Jahre)', 1),
        help="Anzahl der Jahre, über die das Projekt bewertet wird."
    ))
    ramp_up_time = st.number_input(
        "Anlaufzeit in Jahren:",
        min_value=0.0,
        max_value=float(project_duration),
        step=0.5,
        value=st.session_state.data.get('Anlaufzeit (Jahre)', 0.0),
        help="Zeitraum, in dem noch keine Erlöse oder Einsparungen erzielt werden."
    )

    # Dynamische Umsatzsteigerungen
    st.subheader("Dynamische Umsatzsteigerungen")
    num_periods = int(st.number_input(
        "Anzahl der Zeiträume mit unterschiedlichen Wachstumsraten:",
        min_value=1,
        step=1,
        value=st.session_state.data.get('Anzahl Wachstumsperioden', 1),
        help="Anzahl der Zeiträume, für die Sie unterschiedliche Wachstumsraten eingeben möchten."
    ))

    # Initialisieren oder Abrufen der Wachstumsratenperioden
    st.session_state.data['Anzahl Wachstumsperioden'] = num_periods
    existing_growth_periods = st.session_state.data.get('Dynamische Wachstumsraten', [])
    if len(existing_growth_periods) < num_periods:
        for _ in range(num_periods - len(existing_growth_periods)):
            existing_growth_periods.append({})
    elif len(existing_growth_periods) > num_periods:
        existing_growth_periods = existing_growth_periods[:num_periods]

    growth_periods = []
    valid_periods = True  # Flag für gültige Zeiträume
    for i in range(num_periods):
        st.markdown(f"**Zeitraum {i+1}**")
        col1, col2, col3 = st.columns(3)
        with col1:
            start_year = int(st.number_input(
                f"Startjahr für Zeitraum {i+1}:",
                min_value=1,
                max_value=project_duration,
                value=existing_growth_periods[i].get('start_year', 1),
                step=1,
                key=f"start_year_{i}"
            ))
        with col2:
            end_year = int(st.number_input(
                f"Endjahr für Zeitraum {i+1}:",
                min_value=start_year,
                max_value=project_duration,
                value=existing_growth_periods[i].get('end_year', project_duration),
                step=1,
                key=f"end_year_{i}"
            ))
        with col3:
            growth_rate = st.number_input(
                f"Wachstumsrate (%) für Zeitraum {i+1}:",
                step=0.1,
                format="%.2f",
                value=existing_growth_periods[i].get('growth_rate', 0.0),
                key=f"growth_rate_{i}"
            )

        # Überprüfen, ob der Start des aktuellen Zeitraums nach dem Ende des vorherigen Zeitraums liegt
        if i > 0 and start_year <= growth_periods[i - 1]["end_year"]:
            st.error(f"Zeitraum {i+1}: Startjahr muss nach dem Endjahr des vorherigen Zeitraums liegen.")
            valid_periods = False

        growth_periods.append({
            "start_year": start_year,
            "end_year": end_year,
            "growth_rate": growth_rate
        })

    # Wenn die Zeiträume nicht gültig sind, keine weiteren Berechnungen zulassen
    if not valid_periods:
        return

    # Input für Kosteneinsparungen, zusätzliche Betriebskosten und Basisumsatz
    cost_savings = st.number_input(
        "Geschätzte jährliche Kosteneinsparungen (€):",
        min_value=0.0,
        step=1000.0,
        format="%.2f",
        value=st.session_state.data.get('Jährliche Kosteneinsparungen (€)', 0.0),
        help="Erwartete jährliche Kosteneinsparungen durch das Projekt."
    )
    additional_operational_cost = st.number_input(
        "Zusätzliche jährliche Betriebskosten (€):",
        min_value=0.0,
        step=1000.0,
        format="%.2f",
        value=st.session_state.data.get('Zusätzliche Betriebskosten (€)', 0.0),
        help="Zusätzliche jährliche Betriebskosten, die durch das Projekt entstehen."
    )
    basisumsatz = st.number_input(
        "Basisumsatz im ersten Jahr (€):",
        min_value=0.0,
        step=1000.0,
        format="%.2f",
        value=st.session_state.data.get('Basisumsatz (€)', 0.0),
        help="Der Ausgangsumsatz, auf den die Wachstumsraten angewendet werden."
    )

    # Berechnung der jährlichen Umsätze unter Berücksichtigung des Wachstums
    years = np.arange(1, project_duration + 1)
    revenue = np.zeros(project_duration)
    revenue[0] = basisumsatz
    for i in range(1, project_duration):
        for period in growth_periods:
            if period["start_year"] <= years[i] <= period["end_year"]:
                growth_rate = period["growth_rate"]
                revenue[i] = revenue[i - 1] * (1 + growth_rate / 100)
                break

    # Gesamte Betriebskosten (laufende + zusätzliche)
    total_operational_cost = st.session_state.data.get('Laufende Betriebskosten', 0) + additional_operational_cost

    # Berechnung des jährlichen Nettonutzens
    net_benefit_annual = revenue + cost_savings - total_operational_cost

    # Berechnung der kumulierten Erträge und Kosten
    cumulative_benefit = np.zeros(project_duration + 1)
    cumulative_cost = np.zeros(project_duration + 1)
    cumulative_cost[0] = st.session_state.data.get('Anfangsinvestition', 0)

    for i in range(1, project_duration + 1):
        if i > ramp_up_time:
            cumulative_benefit[i] = cumulative_benefit[i - 1] + net_benefit_annual[i - 1]
        # Korrigierte kumulative Kostenberechnung
        cumulative_cost[i] = cumulative_cost[i - 1] + total_operational_cost

    total_net_benefit = cumulative_benefit[-1]
    total_cost = cumulative_cost[-1]

    st.write(f"**Geschätzter gesamter Nettonutzen über {project_duration} Jahr(e):** € {total_net_benefit:,.2f}")
    st.write(f"**Geschätzte Gesamtkosten über {project_duration} Jahr(e):** € {total_cost:,.2f}")

    # ROI Berechnung
    if total_cost > 0:
        roi = ((total_net_benefit - total_cost) / total_cost) * 100
        st.write(f"**Geschätzter ROI über die Projektlaufzeit:** {roi:.2f}%")
    else:
        st.warning("Bitte geben Sie zuerst die Gesamtkosten in Schritt 4 ein.")
        roi = None

    # Amortisationsdauer
    payback_period = None
    cumulative_net_cash_flow = cumulative_benefit - cumulative_cost
    if any(cumulative_net_cash_flow >= 0):
        payback_period_index = np.where(cumulative_net_cash_flow >= 0)[0][0]
        payback_period = years[payback_period_index - 1]  # Subtrahiere 1, da cumulative arrays Länge project_duration + 1 haben
        st.write(f"**Amortisationsdauer (Break-Even):** {payback_period:.2f} Jahre")
    else:
        st.warning("Die Investition amortisiert sich innerhalb der Projektlaufzeit nicht.")

    # Visualisierungen
    st.subheader("Visualisierung")
    if roi is not None:
        st.markdown("**ROI Visualisierung**")
        fig_roi, ax_roi = plt.subplots()
        ax_roi.bar(['ROI'], [roi], color='green')
        ax_roi.set_ylabel('ROI (%)')
        st.pyplot(fig_roi)

    if payback_period is not None:
        st.markdown("**Amortisationsdiagramm**")
        fig_am, ax_am = plt.subplots()
        ax_am.plot(np.arange(0, project_duration + 1), cumulative_benefit, label='Kumulativer Nutzen', marker='o')
        ax_am.plot(np.arange(0, project_duration + 1), cumulative_cost, label='Kumulative Kosten', marker='o')
        ax_am.axvline(x=payback_period, color='grey', linestyle='--', label=f'Break-Even-Punkt ({payback_period:.2f} Jahre)')
        ax_am.legend()
        st.pyplot(fig_am)

    if st.button("Speichern"):
        st.session_state.data['Projektlaufzeit (Jahre)'] = project_duration
        st.session_state.data['Anlaufzeit (Jahre)'] = ramp_up_time
        st.session_state.data['Dynamische Wachstumsraten'] = growth_periods
        st.session_state.data['Basisumsatz (€)'] = basisumsatz
        st.session_state.data['Jährliche Kosteneinsparungen (€)'] = cost_savings
        st.session_state.data['Zusätzliche Betriebskosten (€)'] = additional_operational_cost
        st.session_state.data['Jährlicher Nettonutzen (€)'] = list(net_benefit_annual)
        st.session_state.data['Gesamter Nettonutzen (€)'] = total_net_benefit
        st.session_state.data['Gesamtkosten (€)'] = total_cost
        st.session_state.data['ROI (%)'] = roi
        st.session_state.data['Amortisationsdauer (Jahre)'] = payback_period
        st.success("Daten gespeichert.")
        next_step()


def step6():
    st.header("6. Risikobewertung")
    with st.expander("Anleitung"):
        st.write("Identifizieren Sie potenzielle Risiken und bewerten Sie deren Auswirkungen.")
    risks = st.text_area(
        "6.1 Potenzielle Risiken (jeweils in einer neuen Zeile):",
        height=150,
        value='\n'.join(st.session_state.data.get('Potenzielle Risiken', [])),
        help="Listen Sie mögliche Risiken auf, die das Projekt beeinflussen könnten."
    )
    risk_mitigation = st.text_area(
        "6.2 Risikominderungsstrategien:",
        height=150,
        value=st.session_state.data.get('Risikominderungsstrategien', ''),
        help="Beschreiben Sie Strategien zur Minimierung der identifizierten Risiken."
    )
    if st.button("Speichern"):
        st.session_state.data['Potenzielle Risiken'] = risks.split('\n')
        st.session_state.data['Risikominderungsstrategien'] = risk_mitigation
        st.success("Daten gespeichert.")
        next_step()

def step7():
    st.header("7. Skalierbarkeit und Nachhaltigkeit")
    with st.expander("Anleitung"):
        st.write("Bewerten Sie die Fähigkeit des Projekts, zukünftiges Wachstum zu bewältigen und langfristig nachhaltig zu sein.")
    scalability_options = ["Hoch", "Mittel", "Niedrig"]
    scalability = st.radio(
        "7.1 Skalierbarkeit des Projekts:",
        scalability_options,
        index=scalability_options.index(st.session_state.data.get('Skalierbarkeit', 'Mittel')),
        help="Bewerten Sie, wie gut das Projekt mit zunehmender Last umgehen kann."
    )
    sustainability_options = ["Hoch", "Mittel", "Niedrig"]
    sustainability = st.radio(
        "7.2 Nachhaltigkeit des Projekts:",
        sustainability_options,
        index=sustainability_options.index(st.session_state.data.get('Nachhaltigkeit', 'Mittel')),
        help="Bewerten Sie die langfristige Tragfähigkeit des Projekts."
    )
    if st.button("Speichern"):
        st.session_state.data['Skalierbarkeit'] = scalability
        st.session_state.data['Nachhaltigkeit'] = sustainability
        st.success("Daten gespeichert.")
        next_step()

def step8():
    st.header("8. Erfolgsmessung definieren")
    with st.expander("Anleitung"):
        st.write("Definieren Sie Metriken, um den Erfolg des Projekts zu messen.")
    metrics = st.text_area(
        "8.1 Metriken zur Erfolgsmessung (jeweils in einer neuen Zeile):",
        height=150,
        value='\n'.join(st.session_state.data.get('Erfolgsmessungsmetriken', [])),
        help="Listen Sie spezifische Metriken auf, die den Erfolg des Projekts messen."
    )
    targets = st.text_area(
        "8.2 Zielwerte für diese Metriken (jeweils in einer neuen Zeile):",
        height=150,
        value='\n'.join(st.session_state.data.get('Zielwerte', [])),
        help="Definieren Sie Zielwerte für die genannten Metriken."
    )
    if st.button("Speichern"):
        st.session_state.data['Erfolgsmessungsmetriken'] = metrics.split('\n')
        st.session_state.data['Zielwerte'] = targets.split('\n')
        st.success("Daten gespeichert.")
        next_step()

def step9():
    st.header("9. Zusammenfassung der bisherigen Eingaben")
    with st.expander("Anleitung"):
        st.write("Hier sehen Sie eine Übersicht Ihrer bisherigen Eingaben. Überprüfen Sie die Informationen und nutzen Sie diese Zusammenfassung als Grundlage für Ihre Entscheidungsfindung im nächsten Schritt.")
    if st.session_state.data:
        for key, value in st.session_state.data.items():
            if isinstance(value, list):
                value_display = ', '.join(str(v) for v in value)
            elif isinstance(value, dict):
                value_display = ', '.join([f"{k}: {v}" for k, v in value.items()])
            else:
                value_display = str(value)
            st.markdown(f"**{key}:** {value_display}")
    else:
        st.warning("Es sind keine Daten vorhanden. Bitte füllen Sie zuerst die vorherigen Schritte aus.")
    if st.button("Weiter zur Entscheidungsfindung"):
        next_step()

def step10():
    st.header("10. Entscheidungsfindung")
    with st.expander("Anleitung"):
        st.write("Treffen Sie eine fundierte Entscheidung basierend auf den bisherigen Analysen.")
    decision_options = ["", "Projekt durchführen", "Projekt verschieben", "Projekt ablehnen"]
    decision = st.selectbox(
        "10.1 Entscheidung:",
        decision_options,
        index=decision_options.index(st.session_state.data.get('Entscheidung', '')),
        help="Wählen Sie eine Entscheidung basierend auf der Bewertung."
    )
    reasoning = st.text_area(
        "10.2 Begründung der Entscheidung:",
        height=150,
        value=st.session_state.data.get('Begründung', ''),
        help="Begründen Sie Ihre Entscheidung mit den wichtigsten Argumenten."
    )
    if st.button("Speichern"):
        st.session_state.data['Entscheidung'] = decision
        st.session_state.data['Begründung'] = reasoning
        st.success("Daten gespeichert.")
        next_step()

def step11():
    st.header("11. Implementierungsplanung")
    with st.expander("Anleitung"):
        st.write("Erstellen Sie einen detaillierten Plan für die Umsetzung des Projekts.")
    project_plan = st.text_area(
        "11.1 Projektplan (Phasen, Meilensteine, Zeitpläne):",
        height=150,
        value=st.session_state.data.get('Projektplan', ''),
        help="Skizzieren Sie den Projektplan mit Phasen und Meilensteinen."
    )
    roles = st.text_area(
        "11.2 Rollen und Verantwortlichkeiten (jeweils in einer neuen Zeile):",
        height=150,
        value='\n'.join(st.session_state.data.get('Rollen und Verantwortlichkeiten', [])),
        help="Definieren Sie die Rollen und Verantwortlichkeiten im Projektteam."
    )
    resources = st.text_area(
        "11.3 Benötigte Ressourcen:",
        height=150,
        value=st.session_state.data.get('Benötigte Ressourcen', ''),
        help="Listen Sie die Ressourcen auf, die für das Projekt benötigt werden."
    )
    if st.button("Speichern"):
        st.session_state.data['Projektplan'] = project_plan
        st.session_state.data['Rollen und Verantwortlichkeiten'] = roles.split('\n')
        st.session_state.data['Benötigte Ressourcen'] = resources
        st.success("Daten gespeichert.")
        next_step()

def step12():
    st.header("12. Überwachung und Evaluierung")
    with st.expander("Anleitung"):
        st.write("Planen Sie, wie Sie den Fortschritt und Erfolg des Projekts überwachen und bewerten werden.")
    monitoring = st.text_area(
        "12.1 Leistungsüberwachung (Methoden, Frequenz):",
        height=150,
        value=st.session_state.data.get('Leistungsüberwachung', ''),
        help="Beschreiben Sie, wie Sie die Leistung überwachen werden."
    )
    reviews = st.text_area(
        "12.2 Regelmäßige Überprüfungen (Zeitpläne, Verantwortliche):",
        height=150,
        value=st.session_state.data.get('Regelmäßige Überprüfungen', ''),
        help="Planen Sie regelmäßige Überprüfungen und wer daran beteiligt ist."
    )
    if st.button("Speichern"):
        st.session_state.data['Leistungsüberwachung'] = monitoring
        st.session_state.data['Regelmäßige Überprüfungen'] = reviews
        st.success("Daten gespeichert.")
        next_step()

def generate_report():
    st.header("Bericht generieren")
    if st.session_state.data:
        st.subheader("Zusammenfassung der Eingaben")
        st.json(st.session_state.data)
        st.subheader("Exportieren")
        report_format = st.selectbox("Wählen Sie das Format für den Berichtsexport:", ["PDF", "JSON", "CSV"])
        if report_format == "PDF":
            if st.button("PDF Bericht generieren"):
                generate_pdf()
        elif report_format == "JSON":
            st.download_button("Download JSON", data=json.dumps(st.session_state.data, indent=4), file_name='bericht.json')
        elif report_format == "CSV":
            df = pd.DataFrame.from_dict(st.session_state.data, orient='index').reset_index()
            df.columns = ['Parameter', 'Wert']
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", data=csv, file_name='bericht.csv')
    else:
        st.warning("Es sind keine Daten vorhanden. Bitte füllen Sie zuerst die Schritte aus.")

def generate_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("KI-Projekt Bewertungsbericht", styles['Title']))
    elements.append(Spacer(1, 12))

    # Projektinformationen hinzufügen
    project_name = st.session_state.data.get('Projektname', 'Unbekanntes Projekt')
    project_manager = st.session_state.data.get('Projektverantwortlicher', 'Unbekannt')
    project_description = st.session_state.data.get('Projektbeschreibung', '')

    elements.append(Paragraph(f"<b>Projektname:</b> {project_name}", styles['Heading2']))
    elements.append(Paragraph(f"<b>Projektverantwortlicher:</b> {project_manager}", styles['Normal']))
    elements.append(Paragraph(f"<b>Projektbeschreibung:</b>", styles['Normal']))
    elements.append(Paragraph(project_description, styles['Normal']))
    elements.append(Spacer(1, 12))

    # Restliche Daten hinzufügen
    for key, value in st.session_state.data.items():
        if key in ['Projektname', 'Projektverantwortlicher', 'Projektbeschreibung']:
            continue  # Diese wurden bereits hinzugefügt
        if isinstance(value, list):
            value = ', '.join(str(v) for v in value)
        elif isinstance(value, dict):
            value = ', '.join([f"{k}: {v}" for k, v in value.items()])
        elements.append(Paragraph(f"<b>{key}:</b> {value}", styles['Normal']))
        elements.append(Spacer(1, 12))

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    b64 = base64.b64encode(pdf).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="Bericht_{project_name}.pdf">Download PDF Bericht</a>'
    st.markdown(href, unsafe_allow_html=True)

# Schritt auswählen und entsprechende Funktion aufrufen
if selected_step == "0. Projektinformationen":
    step0()
elif selected_step == "1. Geschäftsziele definieren":
    step1()
elif selected_step == "2. KI-Einsatz beschreiben":
    step2()
elif selected_step == "3. Technische Machbarkeit bewerten":
    step3()
elif selected_step == "4. Kosten und Ressourcen schätzen":
    step4()
elif selected_step == "5. Nutzen und ROI schätzen":
    step5()
elif selected_step == "6. Risikobewertung":
    step6()
elif selected_step == "7. Skalierbarkeit und Nachhaltigkeit":
    step7()
elif selected_step == "8. Erfolgsmessung definieren":
    step8()
elif selected_step == "9. Zusammenfassung der bisherigen Eingaben":
    step9()
elif selected_step == "10. Entscheidungsfindung":
    step10()
elif selected_step == "11. Implementierungsplanung":
    step11()
elif selected_step == "12. Überwachung und Evaluierung":
    step12()
elif selected_step == "Bericht generieren":
    generate_report()
else:
    st.header(selected_step)
    st.write("Dieser Schritt ist noch nicht implementiert.")

# Option zum Bericht generieren in der Sidebar
st.sidebar.markdown("---")
if st.sidebar.button("Bericht generieren"):
    st.session_state.current_step = "Bericht generieren"
