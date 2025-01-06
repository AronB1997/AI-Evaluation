import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Projektdaten in einem DataFrame simulieren (du kannst sie auch direkt laden)
data = {
    "Project ID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    "Datenverfügbarkeit und -qualität": [6, 9, 9, 5, 7, 7, 8, 5, 5, 8, 7, 8, 4, 7, 6],
    "Technische Fähigkeiten im Team": [8, 3, 4, 7, 5, 8, 3, 4, 9, 6, 4, 8, 4, 3, 6],
    "Technologiekompatibilität mit bestehender IT-Infrastruktur": [2, 4, 3, 9, 5, 2, 8, 2, 3, 6, 2, 7, 8, 3, 5],
    "Entwicklungskosten (€)": [110031, 249513, 217638, 58338, 278033, 178170, 177413, 130929, 285102, 152238, 269129, 145557, 98909, 241873, 188564],
    "Laufende Betriebskosten pro Jahr (€)": [33220, 49451, 47800, 37831, 23721, 24430, 33564, 15334, 17887, 13875, 10796, 48908, 15368, 18872, 36698],
    "Risikobudget (€)": [19863, 9940, 24014, 13195, 24012, 6950, 19416, 7689, 14449, 8767, 11408, 11635, 21163, 10226, 13984],
    "Projektlaufzeit (Jahre)": [1, 2, 3, 3, 4, 1, 2, 1, 1, 4, 1, 1, 4, 3, 4],
    "Anlaufzeit (Jahre)": [1.5, 0.8, 1.5, 0.9, 1.6, 1.1, 1.1, 1.2, 1.0, 1.7, 1.0, 0.9, 1.0, 2.0, 1.1],
    "Anzahl der Zeiträume mit unterschiedlichen Wachstumsraten": [3, 1, 2, 1, 2, 1, 1, 2, 1, 3, 3, 2, 2, 1, 2],
    "Basisumsatz (€)": [494193, 108094, 337810, 119226, 219077, 324561, 251585, 151357, 244611, 485074, 110142, 167457, 164853, 423663, 499702],
    "Risiken (Wahrscheinlichkeit)": [63, 40, 43, 27, 39, 55, 56, 77, 76, 52, 75, 46, 49, 47, 31],
    "Risiken (Auswirkung)": [7, 6, 5, 4, 7, 5, 4, 4, 5, 6, 4, 5, 3, 5, 5],
    "Expected Risk": [4.41, 2.4, 2.15, 1.08, 2.73, 2.75, 2.24, 3.08, 3.8, 3.12, 3.0, 2.3, 1.47, 2.35, 1.55],
    "Skalierbarkeit des Projekts": [8, 8, 5, 8, 4, 7, 5, 4, 6, 6, 4, 8, 6, 8, 7],
    "Nachhaltigkeit des Projekts": [7, 8, 8, 8, 4, 3, 6, 4, 3, 7, 3, 5, 8, 3, 7],
}

df = pd.DataFrame(data)

# Dashboard Titel
st.title("Investitionsentscheidungen Dashboard")

# Projektübersicht anzeigen
st.header("Projektübersicht")
st.write("Hier sehen Sie eine Übersicht der Projekte:")
st.dataframe(df)

# Filter für "Expected Risk" in der Sidebar
st.sidebar.header("Filter")
risk_filter = st.sidebar.slider("Maximales erwartetes Risiko", 0.0, 5.0, 5.0)
filtered_df = df[df["Expected Risk"] <= risk_filter]

st.sidebar.write(f"Anzahl der gefilterten Projekte: {len(filtered_df)}")

# Dynamische Diagramme
st.header("Dynamische Diagramme")

columns = df.columns[1:]  # exclude 'Project ID'

# Diagramm 1
st.subheader("Diagramm 1")
x_axis_1 = st.selectbox("Wähle X-Achse für Diagramm 1", columns, key='x1')
y_axis_1 = st.selectbox("Wähle Y-Achse für Diagramm 1", columns, key='y1')

fig1, ax1 = plt.subplots()
ax1.scatter(df[x_axis_1], df[y_axis_1], color='blue')
ax1.set_xlabel(x_axis_1)
ax1.set_ylabel(y_axis_1)
ax1.set_title(f"{x_axis_1} vs {y_axis_1}")
st.pyplot(fig1)

# Diagramm 2
st.subheader("Diagramm 2")
x_axis_2 = st.selectbox("Wähle X-Achse für Diagramm 2", columns, key='x2')
y_axis_2 = st.selectbox("Wähle Y-Achse für Diagramm 2", columns, key='y2')

fig2, ax2 = plt.subplots()
ax2.scatter(df[x_axis_2], df[y_axis_2], color='green')
ax2.set_xlabel(x_axis_2)
ax2.set_ylabel(y_axis_2)
ax2.set_title(f"{x_axis_2} vs {y_axis_2}")
st.pyplot(fig2)

# Diagramm 3
st.subheader("Diagramm 3")
x_axis_3 = st.selectbox("Wähle X-Achse für Diagramm 3", columns, key='x3')
y_axis_3 = st.selectbox("Wähle Y-Achse für Diagramm 3", columns, key='y3')

fig3, ax3 = plt.subplots()
ax3.scatter(df[x_axis_3], df[y_axis_3], color='red')
ax3.set_xlabel(x_axis_3)
ax3.set_ylabel(y_axis_3)
ax3.set_title(f"{x_axis_3} vs {y_axis_3}")
st.pyplot(fig3)

# Projekttabelle mit Filter anzeigen
st.header("Gefilterte Projekte")
st.dataframe(filtered_df)
