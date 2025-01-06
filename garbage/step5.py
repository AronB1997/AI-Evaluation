# steps/step5.py
import streamlit as st
import pandas as pd
import plotly.express as px

def run_step5():
    st.title("5. Erweiterte Nutzwertanalyse und Gesamtscore")

    st.write("Bitte weisen Sie jedem Kriterium eine Gewichtung zwischen 1 und 10 zu (1 = unwichtig, 10 = sehr wichtig).")

    # Seitenleiste für Gewichtungen
    st.sidebar.header("Gewichtungen")
    st.sidebar.write("**Qualitative Kriterien**")
    scalability_weight = st.sidebar.slider("Gewichtung für Skalierbarkeit:", 1, 10, 5)
    sustainability_weight = st.sidebar.slider("Gewichtung für Nachhaltigkeit:", 1, 10, 5)
    technical_feasibility_weight = st.sidebar.slider("Gewichtung für Technische Machbarkeit:", 1, 10, 5)
    data_availability_weight = st.sidebar.slider("Gewichtung für Datenverfügbarkeit und -qualität:", 1, 10, 5)
    technical_skills_weight = st.sidebar.slider("Gewichtung für Technische Fähigkeiten im Team:", 1, 10, 5)
    tech_compatibility_weight = st.sidebar.slider("Gewichtung für Technologiekompatibilität:", 1, 10, 5)

    st.sidebar.write("**Finanzielle Kriterien**")
    roi_weight = st.sidebar.slider("Gewichtung für ROI:", 1, 10, 5)
    break_even_weight = st.sidebar.slider("Gewichtung für Break-Even-Punkt:", 1, 10, 5)
    profit_weight = st.sidebar.slider("Gewichtung für Geschätzten Gewinn:", 1, 10, 5)

    st.sidebar.write("**Risikokriterium**")
    risk_weight = st.sidebar.slider("Gewichtung für Risiko:", 1, 10, 5)

    # Daten aus st.session_state abrufen
    data = st.session_state.data

    # Überprüfen, ob alle notwendigen Daten vorhanden sind
    required_fields = ['Scalability', 'Sustainability', 'Technical Feasibility',
                       'Data Availability', 'Technical Skills', 'Technology Compatibility',
                       'Development Costs', 'Risk Buffer', 'Annual Costs',
                       'Annual Revenue', 'Years to Analyze', 'Risks']
    if not all(field in data for field in required_fields):
        st.error("Bitte stellen Sie sicher, dass alle vorherigen Schritte ausgefüllt sind.")
        return

    # Qualitative Bewertungen abrufen
    qualitative_scores = {
        'Skalierbarkeit': (data['Scalability'], scalability_weight),
        'Nachhaltigkeit': (data['Sustainability'], sustainability_weight),
        'Technische Machbarkeit': (data['Technical Feasibility'], technical_feasibility_weight),
        'Datenverfügbarkeit und -qualität': (data['Data Availability'], data_availability_weight),
        'Technische Fähigkeiten im Team': (data['Technical Skills'], technical_skills_weight),
        'Technologiekompatibilität': (data['Technology Compatibility'], tech_compatibility_weight)
    }

    # Finanzielle Berechnungen
    total_fixed_costs = data['Development Costs'] + data['Risk Buffer']
    cumulative_costs = [total_fixed_costs + data['Annual Costs'] * year for year in range(data['Years to Analyze'] + 1)]
    cumulative_revenues = [data['Annual Revenue'] * year for year in range(data['Years to Analyze'] + 1)]
    total_costs = cumulative_costs[-1]
    total_revenue = cumulative_revenues[-1]
    estimated_profit = total_revenue - total_costs
    roi = (estimated_profit / total_costs * 100) if total_costs > 0 else 0

    # Break-Even-Jahr berechnen
    break_even_year = None
    for year in range(1, data['Years to Analyze'] + 1):
        if cumulative_revenues[year] >= cumulative_costs[year]:
            break_even_year = year
            break

    # Finanzielle Kennzahlen normieren
    financial_scores = {}

    # ROI Normierung
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

    # Break-Even-Punkt Normierung
    if break_even_year:
        break_even_score = max(1, 11 - break_even_year)  # Früheres Jahr ist besser
    else:
        break_even_score = 1
    financial_scores['Break-Even-Punkt'] = (break_even_score, break_even_weight)

    # Geschätzter Gewinn Normierung
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
    financial_scores['Geschätzter Gewinn'] = (profit_score, profit_weight)

    # Risiko Normierung
    risks = data.get('Risks', [])
    num_risks = len(risks)
    if num_risks > 0:
        max_total_risk = 100 * num_risks  # Maximalwert pro Risiko ist 100 (10 Wahrscheinlichkeit * 10 Auswirkung)
        total_risk = sum(risk['probability'] * risk['impact'] for risk in risks)
        normalized_risk_score = 10 - (total_risk / max_total_risk * 10)
        normalized_risk_score = max(0, normalized_risk_score)  # Score nicht negativ werden lassen
    else:
        normalized_risk_score = 10  # Keine Risiken bedeutet bester Score
    risk_scores = {'Risiko': (normalized_risk_score, risk_weight)}

    # Gesamtnutzwert berechnen
    total_weight = sum(weight for _, weight in list(qualitative_scores.values()) +
                       list(financial_scores.values()) + list(risk_scores.values()))
    total_score = 0

    # Daten für Visualisierung vorbereiten
    all_scores = {**qualitative_scores, **financial_scores, **risk_scores}

    # Dashboard-Layout erstellen
    st.write("## Dashboard")
    st.markdown("---")

    # Spaltenlayout für Gauges
    num_criteria = len(all_scores)
    cols = st.columns(3)  # Anpassen der Anzahl der Spalten nach Bedarf

    # Gauges für jedes Kriterium anzeigen
    for idx, (criterion, (score, weight)) in enumerate(all_scores.items()):
        weighted_score = score * weight
        total_score += weighted_score
        # Gauge erstellen
        fig = px.bar_polar(
            r=[score],
            theta=[criterion],
            range_r=[0, 10],
            title=f"{criterion} (Gewichtung: {weight})",
            color_discrete_sequence=['#1f77b4']
        )
        fig.update_layout(showlegend=False)
        # Gauge in passender Spalte anzeigen
        col = cols[idx % 3]
        with col:
            st.plotly_chart(fig, use_container_width=True)

    # Normalisierten Gesamtscore berechnen
    normalized_total_score = total_score / total_weight

    # Gesamtscore als großes Gauge anzeigen
    st.markdown("---")
    st.write("## Gesamtscore des Projekts")
    fig_total = px.bar_polar(
        r=[normalized_total_score],
        theta=["Gesamtscore"],
        range_r=[0, 10],
        title="Gesamtscore",
        color_discrete_sequence=['#ff7f0e']
    )
    fig_total.update_layout(showlegend=False)
    st.plotly_chart(fig_total, use_container_width=True)

    st.success(f"Der Gesamtscore des Projekts beträgt: {normalized_total_score:.2f} von maximal 10")

    # Gesamtrisiko anzeigen
    if risks:
        total_expected_risk = sum(risk['expected_risk'] for risk in risks)
        st.write(f"### Gesamtrisiko:")
        st.write(f"- **Kumuliertes erwartetes Risiko:** {total_expected_risk}")
