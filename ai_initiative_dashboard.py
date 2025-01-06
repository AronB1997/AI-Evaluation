import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Beispielprojektdaten (könnten auch aus einer CSV-Datei gelesen werden)
df = pd.read_excel('example_projects.xlsx')

# Dashboard Titel
st.title("Investitionsentscheidungen Dashboard")

# Projektübersicht anzeigen
st.header("Projektübersicht")
st.write("Hier sehen Sie eine Übersicht der Projekte:")
st.dataframe(df)

# Abschnitt zur Auswahl der X- und Y-Achsen für die dynamischen Diagramme
st.header("Dynamische Diagramme")

# Mögliche Optionen für die Achsen
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

# Optionale Filter
st.sidebar.header("Filter")
risk_filter = st.sidebar.slider("Maximale Risikowahrscheinlichkeit", 0, 100, 100)
filtered_df = df[df["Expected Risk"] <= risk_filter]
st.sidebar.write(f"Anzahl der gefilterten Projekte: {len(filtered_df)}")

# Projekttabelle mit Filter anzeigen
st.header("Gefilterte Projekte")
st.dataframe(filtered_df)
