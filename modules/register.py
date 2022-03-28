import streamlit as st
import gspread  # to write data to the DB
import pandas as pd
import pytz
from datetime import datetime

from .utils import (
    team_chosen,
    update_team_name,
    update_password,
    update_mentor,
    update_team_count,
    update_team_member,
    update_category,
    reset,
    submit_project,
    disable_widgets,
)

repo = ""
app = ""


def register_page(rows):
    st.title(":atom_symbol: Hackatón \"Quantum-Apps\" :atom_symbol:")

    if st.session_state["disabled"]:
        st.info("Vuelva a cargar esta página para habilitar el registro")

    st.subheader("Registra tu equipo aquí:")
    st.write(
        """El nombre de su equipo no puede tener espacios, si lo desea, puede usar un guión bajo (_) o
     guión (-) para separar palabras.

Por ejemplo: si el nombre de su equipo es "El equipo A", **El_equipo_A** O **El-equipo-A** son aceptables.

Si el nombre del equipo que ha elegido ya está en uso, elija un nombre diferente para asegurarse de que haya
    ¡no hay confusión cuando se anuncian los ganadores! """
    )

    # elegir un nombre de equipo
    team_name = st.text_input(
        "Nombre del equipo",
        value=st.session_state.team,
        key="team_name",
        on_change=update_team_name,
        disabled=st.session_state.disabled
    )

    if len(team_name) > 0:
        # asegúrese de que no haya espacios
        if " " in team_name:
            st.warning("Elimina espacios en el nombre de tu equipo.")
            st.stop()
        # elimine guiones y guiones bajos y distinga entre mayúsculas y minúsculas para comparar
        # hace que no se distinga entre mayúsculas y minúsculas (A-team = a-team)
        team_short = team_name.replace("-", "").replace("_", "").casefold()

        # compare team name to those in database
        for row in rows:
            row_short = row.Team.replace("-", "").replace("_", "").casefold()
            if row_short == team_short:  # hace que no se distinga entre mayúsculas y minúsculas (A-team = a-team)
                st.warning("Ese nombre está tomado, elija un nombre de equipo diferente")
                st.stop()

        # si el nombre del equipo es válido, continúe creando una contraseña
        st.info("Nombre del equipo disponible, continúe")
        st.write(f"Has elegido un nombre de equipo de: **`{team_name}`**")
        st.button("¿Continuar con este nombre de equipo?", on_click=team_chosen, disabled=st.session_state.disabled)

    # crear contraseña para el equipo
    if st.session_state["team_chosen"]:
        # password field
        pass_1 = st.text_input(
            "Contraseña del equipo", value=st.session_state.pwd, type="password", disabled=st.session_state.disabled
        )
        # Verifique que no sea un error tipográfico.
        pass_2 = st.text_input(
            "Confirmar contraseña",
            value=st.session_state.pwd,
            type="password",
            key="password",
            disabled=st.session_state.disabled
        )

        if pass_1 and pass_2:
            # si no coinciden avisar al usuario
            if pass_1 != pass_2:
                st.warning("¡Las contraseñas no coinciden!")
                st.stop()
            else:
                # if they do, save the password
                update_password()
                st.write(f"La contraseña de tu equipo es **`{pass_1}`**")
                st.write(
                    "❗ Asegúrese de recordar el nombre y la contraseña de su equipo, se utilizarán para editar y enviar su proyecto"
                )
                st.write("---")

    # once a password is saved in state, the team details can be entered
    if st.session_state.pwd:
        # if the team has a mentor they can enter their name here
        with st.expander("Si su equipo tiene un mentor, ingrese los detalles aquí:"):
            mentor_name = st.text_input(
                "Ingrese el nombre del mentor",
                value=st.session_state.mentor,
                key="mentor_name",
                on_change=update_mentor,
                disabled=st.session_state.disabled
            )

        # a number input controls the number of text fields
        team_count = st.number_input(
            "Número de personas en el equipo:",
            1,
            4,
            value=st.session_state.num_teams,
            key="team_count",
            on_change=update_team_count,
            disabled=st.session_state.disabled
        )
        st.write("Ingrese el nombre completo de todos los participantes en su equipo:")

        # create correct number of input fields for members names
        member_list = []
        for x in range(1, int(team_count + 1)):

            if f"team_member_{x}" not in st.session_state:
                st.session_state[f"team_member_{x}"] = ""

            member = st.text_input(
                f"Nombre de la miembro del equipo {x}",
                value=st.session_state[f"team_member_{x}"],
                key=f"team_member_name_{x}",
                on_change=update_team_member,
                args=(x,),
                disabled=st.session_state.disabled
            )
            member_list.append(member)

        # Choose the category you want to make you app for
        category_dict = {
            "Quantum Phenomena": 0,
            "Water care and food sustainability": 1,
            "Visualization and management of data for the conservation of the environment": 2,
            "Use of artificial intelligence and data science in Chemistry": 3,
            "Fight emerging diseases": 4,
            "Chemistry teaching": 5,
        }
        category = st.radio(
            "Elige tu categoría:",
            category_dict.keys(),
            index=st.session_state.category_index,
            key="category",
            on_change=update_category,
            args=(category_dict,),
            disabled=st.session_state.disabled
        )
        st.write("---")

        # add details to session state
        st.session_state.members = str(member_list)
        # st.session_state.category = category

        # review entry and submit to google sheet
        st.write("Revisa y confirma tu entrada:")
        st.write(f"**Nombre del equipo: `{st.session_state.team_name}`**")
        st.write(f"**Miembros del equipo: `{st.session_state.members}`**")
        st.write(f"**Categoría: `{st.session_state.category}`**")
        st.write(f"**Contraseña: `{st.session_state.password}`**")

        if len(mentor_name) > 1:
            st.write(f"**Mentor: `{st.session_state.mentor}`**")

        submit = st.button("Confirmar entrada del equipo", on_click=team_chosen, disabled=st.session_state.disabled)

        if submit:
            # send to google sheet
            ## write results to google sheets
            gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
            sheet_url = st.secrets["private_gsheets_url"]
            data = gc.open_by_url(sheet_url).sheet1
            data.append_row(
                [
                    st.session_state.team_name,
                    st.session_state.password,
                    st.session_state.members,
                    st.session_state.mentor_name,
                    st.session_state.category,
                    repo,
                    app,
                    str(datetime.now(tz=pytz.utc)),
                ]
            )

            st.info("Información del equipo enviada")
            st.balloons()
            registration = pd.DataFrame(
                {
                    "Nombre del equipo": [st.session_state.team_name],
                    "Contraseña": [st.session_state.password],
                    "Miembros del equipo": [st.session_state.members],
                    "Mentor": [st.session_state.mentor_name],
                    "Categoría": [st.session_state.category],
                }
            )
            download = st.download_button(
                label="Descargar datos de registro",
                data=registration.to_csv(index=False).encode("utf-8"),
                file_name=f"{st.session_state.team_name}_registration_details.csv",
                mime="text/csv",
                on_click=reset,
            )

            st.info("Vuelva a cargar esta página si desea realizar otro registro")
