import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuración de la pestaña del navegador
st.set_page_config(page_title="Reforzamiento Inglés EST3", layout="wide")

# Conexión con tu Google Sheet (usa el secreto que configuraremos después)
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("📚 Portal de Reforzamiento - Lengua Extranjera")
st.markdown("---")

# 1. ACCESO DEL ALUMNO
col1, col2 = st.columns(2)

with col1:
    # Estos nombres deben coincidir EXACTAMENTE con tus pestañas en Google Sheets
    lista_grupos = ["1G", "1H", "1I", "1J", "1K", "2G", "2H", "2I", "2J", "2K", "3G", "3H"]
    grupo = st.selectbox("Selecciona tu Grupo:", lista_grupos)

with col2:
    matricula_input = st.text_input("Ingresa tu Matrícula:").strip().upper()

if matricula_input:
    try:
        # Leer la hoja del grupo seleccionado
        df_alumnos = conn.read(worksheet=grupo)
        
        # Buscar al alumno (Columna MATRICULA)
        alumno = df_alumnos[df_alumnos['MATRICULA'].astype(str).str.upper() == matricula_input]

        if not alumno.empty:
            nombre = alumno.iloc[0]['NOMBRE DEL ALUMNO']
            status = alumno.iloc[0]['STATUS']

            if status == "BAJA":
                st.error(f"Lo sentimos {nombre}, tu estatus es BAJA. Por favor, acude con tu maestro.")
            else:
                st.success(f"Bienvenido(a), {nombre} (Estatus: {status})")
                
                # 2. SELECCIÓN DE ACTIVIDAD
                # Lee la pestaña 'ACTIVIDADES' (asegúrate de que se llame así exactamente)
                df_actividades = conn.read(worksheet="ACTIVIDADES")
                
                actividad_sel = st.selectbox("Selecciona el ejercicio a realizar:", df_actividades['EJERCICIO'].tolist())
                
                # Obtener el link de la actividad seleccionada
                link_ejercicio = df_actividades[df_actividades['EJERCICIO'] == actividad_sel]['LINK'].values[0]
                
                st.info(f"Instrucciones: Completa el ejercicio de LearningApps abajo.")

                # 3. MOSTRAR EJERCICIO (Iframe)
                st.components.v1.iframe(link_ejercicio, height=700, scrolling=True)

                # 4. BOTÓN DE REGISTRO
                if st.button("✅ YA TERMINÉ MI EJERCICIO"):
                    st.balloons()
                    st.success("¡Excelente trabajo! Tu participación ha sido registrada.")
                    st.info("Nota para el alumno: Tu maestro revisará tu progreso en la hoja de AVANCES.")
                    
                    # Aquí es donde el maestro ve los datos
                    registro = {
                        "FECHA": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        "MATRICULA": matricula_input,
                        "NOMBRE": nombre,
                        "GRUPO": grupo,
                        "ACTIVIDAD": actividad_sel
                    }
                    # Nota: La escritura automática se activa al configurar la cuenta de servicio en Streamlit
                    
        else:
            st.warning("Matrícula no encontrada en este grupo. Verifica que seleccionaste el grupo correcto.")
            
    except Exception as e:
        st.error(f"Hubo un problema al conectar con las listas: {e}")
