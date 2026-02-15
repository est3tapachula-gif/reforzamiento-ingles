import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Portal Inglés EST3", layout="wide")

# Conexión con Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("📚 Portal de Reforzamiento - EST3")
st.markdown("---")

# 1. ENTRADA DE DATOS
col1, col2 = st.columns(2)

with col1:
    # Estos son los nombres exactos de tus pestañas
    lista_grupos = ["1G", "1H", "1I", "1J", "1K", "2G", "2H", "2I", "2J", "2K", "3G", "3H"]
    grupo_sel = st.selectbox("Selecciona tu Grupo:", lista_grupos)

with col2:
    matricula_input = st.text_input("Ingresa tu Matrícula:").strip().upper()

if matricula_input:
    try:
        # Leer la hoja del grupo seleccionado
        df_alumnos = conn.read(worksheet=grupo_sel)
        
        # Buscar al alumno usando el nombre de columna exacto: 'MATRICULA'
        alumno = df_alumnos[df_alumnos['MATRICULA'].astype(str).str.strip().str.upper() == matricula_input]

        if not alumno.empty:
            # Usamos los nombres de columna de tu Excel: 'NOMBRE DEL ALUMNO' y 'STATUS'
            nombre = alumno.iloc[0]['NOMBRE DEL ALUMNO']
            status = alumno.iloc[0]['STATUS']

            if status == "BAJA":
                st.error(f"Estatus: BAJA. El alumno(a) {nombre} debe acudir con el maestro.")
            else:
                st.success(f"Bienvenido(a), {nombre}")
                
                # Leer la pestaña de ACTIVIDADES
                df_act = conn.read(worksheet="ACTIVIDADES")
                
                # Selector de ejercicios basado en tu columna 'EJERCICIO'
                actividad_sel = st.selectbox("Selecciona el ejercicio:", df_act['EJERCICIO'].tolist())
                
                # Obtener el link de la columna 'LINK'
                link_ejercicio = df_act[df_act['EJERCICIO'] == actividad_sel]['LINK'].values[0]
                
                st.info(f"Actividad: {actividad_sel}")
                st.components.v1.iframe(link_ejercicio, height=700, scrolling=True)

                if st.button("✅ REGISTRAR TÉRMINO"):
                    st.balloons()
                    st.success("¡Registro completado!")
        else:
            st.warning("Matrícula no encontrada en este grupo.")
            
    except Exception as e:
        st.error(f"Error de conexión: {e}")
