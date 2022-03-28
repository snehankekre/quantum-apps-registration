import streamlit as st

def home_page(rows):
    st.image("images/logoUACH.png", use_column_width=True)
    st.title(":atom_symbol: Hackatón \"Quantum-Apps\"  :atom_symbol:")
    st.markdown(
        """Este hackatón está dirigido a los estudiantes de la Facultad de Ciencias Químicas 
        de la Universidad Autónoma de Chihuahua y, a estudiantes de áreas afines en otras
        facultades de la misma universidad, tanto de licenciatura como de posgrado. 

### :books: Requisitos:
- Podrán participar estudiantes inscritos o recientemente egresados (no más de seis meses de egreso).
- Registrarse llenando la solicitud en esta página.

### :1234: Reglas:
- Se permiten equipos de hasta 4 concursantes.
- Ser estudiante de licenciatura o posgrado de la UACH o no tener mas de 6 meses de egreso.
- Una misma persona no puede estar en más de un equipo.
- Cada equipo necesita un nombre y una contraseña únicos que todos los miembros del equipo conocen y
     tener acceso a. El nombre del equipo y la contraseña se utilizarán para ingresar, modificar y enviar el proyecto de hackatón.
"""
    )
    
    col1, col2 = st.columns(2)
    col1.image("images/logoFCQ.png", width=175)
    col2.image("images/logoCNS.jpg")
