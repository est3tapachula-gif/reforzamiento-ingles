import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Portal Inglés EST3", layout="wide")

# 2. Estilo Visual (Color Vino y Blanco)
st.markdown("""
    <style>
    .stApp { background-color: white; }
    h1 { color: #800020; text-align: center; border-bottom: 3px solid #800020; }
    .stButton>button { background-color: #800020; color: white; border-radius: 10px; width: 100%; }
    .stSelectbox label, .stTextInput label { color: #800020; font-weight: bold; }
    /* Estilo para la barra lateral */
    [data-testid="stSidebar"] { background-color: #f8f8f8; border-right: 2px solid #800020; }
    </style>
    """, unsafe_allow_index=True)

st.title("📚 PORTAL DE REFORZAMIENTO - EST3")

# URL Directa de tu hoja
SHEET_ID = "1ywiEIKJYqvDI8TH7I-HoyH8IUOAW_Dn8JA9rkNoQ1kU"

def leer_hoja(nombre_pestana):
    # Agregamos un truco para que no use caché y se actualice al instante
    import time
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={nombre_pestana}&t={int(time.time())}"
    return pd.read_csv(url)

# --- BARRA LATERAL (TOP 5) ---
with st.sidebar:
    st.markdown("<h2 style='color: #800020; text-align: center;'>🏆 TOP 5</h2>", unsafe_allow_index=True)
    try:
        # Intenta leer la pestaña AVANCES
        df_puntos = leer_hoja("AVANCES")
        # Ordena de mayor a menor y toma los primeros 5
        top_5 = df_puntos.sort_values(by="PUNTOS", ascending=False).head(5)
        
        for i, row in top_5.iterrows():
            st.info(f"🥇 **{row['NOMBRE']}**\n\n{row['PUNTOS']} Puntos")
    except:
        st.write("Cargando tabla de posiciones...")

# --- CUERPO PRINCIPAL ---
col1, col2 = st.columns(2)

with col1:
    lista_grupos = ["1G", "1H", "1I", "1J", "1K", "2G", "2H", "2I", "2J", "2K", "3G", "3H"]
    grupo_sel = st.selectbox("Selecciona tu Grupo:", lista_grupos)

with col2:
    matricula_input = st.text_input("Ingresa tu Matrícula:").strip().upper()

if matricula_input:
    try:
        df_alumnos = leer_hoja(grupo_sel)
        alumno = df_alumnos[df_alumnos['MATRICULA'].astype(str).str.strip().str.upper() == matricula_input]

        if not alumno.empty:
            nombre = alumno.iloc[0]['NOMBRE DEL ALUMNO']
            status = alumno.iloc[0]['STATUS']

            if status == "BAJA":
                st.error(f"Estatus: BAJA. Contacta al maestro.")
            else:
                st.success(f"Bienvenido(a), {nombre}")
                
                df_act = leer_hoja("ACTIVIDADES")
                actividad_sel = st.selectbox("Selecciona el ejercicio:", df_act['EJERCICIO'].tolist())
                
                link_ejercicio = df_act[df_act['EJERCICIO'] == actividad_sel]['LINK'].values[0]
                
                st.markdown(f"### Actividad: <span style='color:#800020'>{actividad_sel}</span>", unsafe_allow_index=True)
                st.components.v1.iframe(link_ejercicio, height=700, scrolling=True)
                
                if st.button("✅ REGISTRAR TÉRMINO"):
                    st.balloons()
                    st.success("¡Excelente! Tu participación ha sido registrada.")
        else:
            st.warning("Matrícula no encontrada.")
            
    except Exception as e:
        st.error(f"Error: {e}")
