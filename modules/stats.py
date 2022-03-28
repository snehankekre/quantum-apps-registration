import streamlit as st
import plotly.express as px
import pandas as pd

def stats_page(rows):
    st.title(":atom_symbol: Hackatón \"Quantum-Apps\" :atom_symbol:")
    st.subheader("¡Echa un vistazo a los equipos actuales!")

    team_number = 0
    team_members = []
    team_size = []
    team_hist = {1: 0, 2: 0, 3: 0, 4: 0}
    category = {
        "Quantum Phenomena": 0,
        "Water care and food sustainability": 0,
        "Visualization and management of data for the conservation of the environment": 0,
        "Use of artificial intelligence and data science in Chemistry": 0,
        "Fight emerging diseases": 0,
        "Chemistry teaching": 0,
    }
    for row in rows:
        team_number += 1
        team_size.append(len(row.Participants.split(",")))
        team_hist[team_size[-1]] += 1
        category[row.Category] += 1
        # st.write(row)

    st.write(f"**¡Actualmente hay {team_number} equipos participando!** :tada:")
    st.write("¡Veamos algunas de las estadísticas de los equipos participantes!")

    st.subheader("Distribución de Equipos:")

    team_hist_list = list(team_hist.items())
    df_team_hist = pd.DataFrame(
        team_hist_list, columns=["Número de participantes por equipo", "Contar"]
    )
    fig = px.bar(df_team_hist, x="Número de participantes por equipo", y="Contar")
    st.plotly_chart(fig)

    st.subheader("Equipos por Categoría:")
    category_list = list(category.items())
    df_category = pd.DataFrame(category_list, columns=["Categoría", "Número de equipos"])
    fig = px.bar(df_category, x="Categoría", y="Número de equipos")
    st.plotly_chart(fig)
