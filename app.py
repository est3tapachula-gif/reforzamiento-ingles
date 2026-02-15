import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuración básica de la página
st.set_page_config(page_title="Portal Inglés EST3", layout="wide")

# Conexión con tu Google Sheet (usa la URL de tus Secrets)
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("📚 Portal de Reforzamiento - EST3")
st.markdown("---")

# 1. ENTRADA DE DATOS PARA EL ALUMNO
col1, col2 = st.columns(2)

with col1:
    # Lista de grupos limpia (asegúrate que así se llamen tus pestañas)
    lista_grupos = ["1G", "1H", "1I", "1J", "1K", "2G", "2H", "2I", "2J", "2K", "3G", "3H"]
    grupo_sel = st.selectbox("Selecciona tu Grupo:", lista_grupos)

with col2:
    matricula_input = st.text_input("Ingresa tu Matrícula:").strip().upper()

# 2. PROCESO DE VALIDACIÓN
if matricula_input:
    try:
        # Leer la pestaña del grupo seleccionado
        df_alumnos = conn.read(worksheet=grupo_sel)
        
        # Buscar al alumno en la columna 'MATRICULA'
        alumno = df_alumnos[df_alumnos['MATRICULA'].astype(str).str.strip().str.upper() == matricula_input]

        if not alumno.empty:
            nombre = alumno.iloc[0]['NOMBRE DEL ALUMNO']
            status = alumno.iloc[0]['STATUS']

            if status == "BAJA":
                st.error(f"Estatus: BAJA. El alumno(a) {nombre} debe acudir con el maestro.")
            else:
                st.success(f"Bienvenido(a), {nombre}")
                
                # 3. SECCIÓN DE ACTIVIDADES
                # Leemos la pestaña llamada ACTIVIDADES
                df_act = conn.read(worksheet="ACTIVIDADES")
                
                # Menú de ejercicios disponibles
                actividad_sel = st.selectbox("Selecciona el ejercicio a realizar:", df_act['EJERCICIO'].tolist())
                
                # Extraemos el link de la columna LINK
                link_ejercicio = df_act[df_act['EJERCICIO'] == actividad_sel]['LINK'].values[0]
                
                st.info(f"Instrucciones: Completa el ejercicio de LearningApps aquí abajo.")
                
                # Mostramos el juego/ejercicio
                st.components.v1.iframe(link_ejercicio, height=700, scrolling=True)

                if st.button("✅ YA TERMINÉ MI ACTIVIDAD"):
                    st.balloons()
                    st.success("¡Excelente trabajo! Tu progreso ha sido registrado.")
        else:
            st.warning("Matrícula no encontrada en este grupo. Revisa tus datos.")
            
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        st.info("Revisa que tus 'Secrets' en Streamlit tengan la URL correcta de la hoja.")
