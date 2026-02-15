import streamlit as st
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Portal Inglés EST3", layout="wide")

st.title("📚 Portal de Reforzamiento - EST3")
st.markdown("---")

# URL Directa de tu hoja (formato CSV para evitar errores de conexión)
SHEET_ID = "1ywiEIKJYqvDI8TH7I-HoyH8IUOAW_Dn8JA9rkNoQ1kU"

# Función para leer cualquier pestaña de tu hoja
def leer_hoja(nombre_pestana):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={nombre_pestana}"
    return pd.read_csv(url)

# 1. ENTRADA DE DATOS
col1, col2 = st.columns(2)

with col1:
    lista_grupos = ["1G", "1H", "1I", "1J", "1K", "2G", "2H", "2I", "2J", "2K", "3G", "3H"]
    grupo_sel = st.selectbox("Selecciona tu Grupo:", lista_grupos)

with col2:
    matricula_input = st.text_input("Ingresa tu Matrícula:").strip().upper()

if matricula_input:
    try:
        # Intentar leer la pestaña del grupo
        df_alumnos = leer_hoja(grupo_sel)
        
        # Buscar alumno
        alumno = df_alumnos[df_alumnos['MATRICULA'].astype(str).str.strip().str.upper() == matricula_input]

        if not alumno.empty:
            nombre = alumno.iloc[0]['NOMBRE DEL ALUMNO']
            status = alumno.iloc[0]['STATUS']

            if status == "BAJA":
                st.error(f"Estatus: BAJA. El alumno(a) {nombre} debe acudir con el maestro.")
            else:
                st.success(f"Bienvenido(a), {nombre}")
                
                # Leer pestaña ACTIVIDADES
                df_act = leer_hoja("ACTIVIDADES")
                actividad_sel = st.selectbox("Selecciona el ejercicio:", df_act['EJERCICIO'].tolist())
                
                link_ejercicio = df_act[df_act['EJERCICIO'] == actividad_sel]['LINK'].values[0]
                
                st.info(f"Realizando: {actividad_sel}")
                st.components.v1.iframe(link_ejercicio, height=700, scrolling=True)
        else:
            st.warning("Matrícula no encontrada.")
            
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        st.info("Verifica que el nombre de la pestaña en Excel sea idéntico al seleccionado.")
