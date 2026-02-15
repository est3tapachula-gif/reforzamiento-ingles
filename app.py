import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Portal Inglés EST3", layout="wide")

# 2. Estilo Visual (Color Vino y Blanco)
st.markdown("""
    <style>
    .stApp { background-color: white; }
    h1 { color: #800020; text-align: center; border-bottom: 3px solid #800020; }
    .stSelectbox label, .stTextInput label { color: #800020; font-weight: bold; }
    /* Estilo para la barra lateral */
    [data-testid="stSidebar"] { background-color: #f8f8f8; border-right: 2px solid #800020; }
    /* Estilo del Botón de Registro tipo Banner */
    .boton-registro {
        background-color: #800020;
        color: white !important;
        padding: 20px;
        text-align: center;
        border-radius: 15px;
        font-weight: bold;
        font-size: 24px;
        text-decoration: none;
        display: block;
        margin-top: 30px;
        border: 2px solid #5a0016;
    }
    .boton-registro:hover {
        background-color: #a30029;
        transform: scale(1.02);
        transition: 0.3s;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📚 PORTAL DE REFORZAMIENTO - EST3")

# URL Directa de tu hoja de cálculo
SHEET_ID = "1ywiEIKJYqvDI8TH7I-HoyH8IUOAW_Dn8JA9rkNoQ1kU"

def leer_hoja(nombre_pestana):
    import time
    nombre_pestana = nombre_pestana.strip()
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={nombre_pestana}&t={int(time.time())}"
    return pd.read_csv(url)

# --- BARRA LATERAL (TOP 5) ---
with st.sidebar:
    st.markdown("<h2 style='color: #800020; text-align: center;'>🏆 TOP 5</h2>", unsafe_allow_html=True)
    try:
        df_puntos = leer_hoja("AVANCES")
        df_puntos['PUNTOS'] = pd.to_numeric(df_puntos['PUNTOS'], errors='coerce').fillna(0)
        top_5 = df_puntos.sort_values(by="PUNTOS", ascending=False).head(5)
        
        for i, row in top_5.iterrows():
            st.info(f"🥇 **{row['NOMBRE']}**\n\n{row['PUNTOS']} Puntos")
    except:
        st.write("Registra avances en la pestaña 'AVANCES' del Excel para ver el Top 5.")
    
    st.markdown("---")
    st.write("¡Sigue practicando para aparecer en el podio!")

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
        df_alumnos.columns = df_alumnos.columns.str.strip()
        
        alumno = df_alumnos[df_alumnos['MATRICULA'].astype(str).str.strip().str.upper() == matricula_input]

        if not alumno.empty:
            nombre = alumno.iloc[0]['NOMBRE DEL ALUMNO']
            status = alumno.iloc[0]['STATUS']

            if status == "BAJA":
                st.error(f"Estatus: BAJA. Contacta al maestro.")
            else:
                st.success(f"Bienvenido(a), {nombre}")
                
                df_act = leer_hoja("ACTIVIDADES")
                df_act.columns = df_act.columns.str.strip()
                actividad_sel = st.selectbox("Selecciona el ejercicio:", df_act['EJERCICIO'].tolist())
                
                link_ejercicio = df_act[df_act['EJERCICIO'] == actividad_sel]['LINK'].values[0]
                
                st.markdown(f"### Actividad: <span style='color:#800020'>{actividad_sel}</span>", unsafe_allow_html=True)
                
                # Iframe del ejercicio de LearningApps
                st.components.v1.iframe(link_ejercicio, height=700, scrolling=True)
                
                # --- BOTÓN DE REGISTRO (LINK AL GOOGLE FORM) ---
                st.markdown("---")
                st.markdown("<h4 style='text-align: center;'>Una vez que termines el ejercicio:</h4>", unsafe_allow_html=True)
                
                link_form = "https://docs.google.com/forms/d/e/1FAIpQLSejW9NzbMJHscg98b-ObjAgS4fRFA3G1nN6kpDDytE3uuYT8Q/viewform?usp=header"
                
                st.markdown(f'''
                    <a href="{link_form}" target="_blank" class="boton-registro">
                        ✅ CLIC AQUÍ PARA REGISTRAR QUE TERMINASTE
                    </a>
                ''', unsafe_allow_html=True)
                
        else:
            st.warning("Matrícula no encontrada en el grupo seleccionado.")
            
    except Exception as e:
        st.error(f"Cargando información del grupo...")
