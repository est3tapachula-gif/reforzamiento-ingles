import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Portal de Inglés EST3", layout="wide")

# 2. Conexión con Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("📚 Portal de Reforzamiento - Lengua Extranjera")
st.markdown("---")

# 3. Formulario de Acceso
col1, col2 = st.columns(2)

with col1:
    # Lista de grupos según tus pestañas
    lista_grupos = ["1G", "1H", "1I", "1J", "1K", "2G", "2H", "2I", "2J", "2K", "3G", "3H"]
    grupo_sel = st.selectbox("Selecciona tu Grupo:", lista_grupos)

with col2:
    matricula_input = st.text_input("Ingresa tu Matrícula:").strip().upper()

# 4. Lógica de validación
if matricula_input:
    try:
        # Leer la hoja del grupo seleccionado
        df_alumnos = conn.read(worksheet=grupo_sel)
        
        # Buscar al alumno (comparamos matrícula como texto para evitar errores)
        alumno = df_alumnos[df_alumnos['MATRICULA'].astype(str).str.strip().str.upper() == matricula_input]

        if not alumno.empty:
            nombre = alumno.iloc[0]['NOMBRE DEL ALUMNO']
            status = alumno.iloc[0]['STATUS']

            if status == "BAJA":
                st.error(f"Lo sentimos {nombre}, tu estatus es BAJA. Acude con tu maestro.")
            else:
                st.success(f"Bienvenido(a), {nombre} (Estatus: {status})")
                
                # Leer la pestaña de ACTIVIDADES (Corregido)
                df_act = conn.read(worksheet="ACTIVIDADES")
                
                # Selector de ejercicios
                lista_ejercicios = df_act['EJERCICIO'].tolist()
                actividad_sel = st.selectbox("Selecciona el ejercicio:", lista_ejercicios)
                
                # Obtener el link del ejercicio seleccionado
                link_ejercicio = df_act[df_act['EJERCICIO'] == actividad_sel]['LINK'].values[0]
                
                # Mostrar el ejercicio de LearningApps
                st.info(f"Realizando: {actividad_sel}")
                st.components.v1.iframe(link_ejercicio, height=700, scrolling=True)

                if st.button("✅ REGISTRAR TÉRMINO DE ACTIVIDAD"):
                    st.balloons()
                    st.success("¡Excelente! Tu participación ha sido notificada.")
                    
        else:
            st.warning("Matrícula no encontrada en este grupo. Revisa tus datos.")
            
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        st.info("Asegúrate de que la URL en 'Secrets' es correcta y que la hoja es pública.")
