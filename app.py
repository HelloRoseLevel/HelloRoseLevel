import streamlit as st

from modules.auth import (
    init_session_state, logout
)
from modules import dashboard, ingresos, egresos, subir, reportes, configuracion, edicion, login, visor
from modules.data_loader import load_data, refresh_data
from modules.login import get_base64_image

import base64
from pathlib import Path
  
logo_path2 = Path(__file__).parent.parent / "assets" / "logo2.png"
logo_base642 = get_base64_image(logo_path2)

st.set_page_config(
    page_title="Panel Financiero - Rose Level",
    page_icon=logo_path2,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
    'Get Help': 'https://www.x.com/fercarstens',
    'Report a bug': "https://www.x.com/fercarstens",
    'About': "# Rose Level - Panel Financiero"}
)

init_session_state()

if not st.session_state["authentication_status"]:
    login.render()
else:
    st.sidebar.image(str(logo_path2), width=40)
    st.sidebar.title(f"Bienvenido, {st.session_state['name']}")
    st.sidebar.info(f"🔑 Usuario: {st.session_state['username']}")
    st.sidebar.divider()
    menu_options = [
        "📊 Dashboard",
        "💰 Ingresos",
        "💸 Egresos",
        "📄 Subida de Extractos",
        "📑 Visor de PDFs",
        "📈 Reportes",
        "📝 Edición Manual",
    ]
    menu = st.sidebar.radio("Navegación", menu_options)
    st.sidebar.divider()
    if st.sidebar.button("🚪 Cerrar sesión"):
        logout()
    if st.sidebar.button("🔄 Actualizar datos"):
        refresh_data()
        st.rerun()
    
    load_data()
    
    if st.session_state["movimientos_df"] is None or st.session_state["movimientos_df"].empty:
        st.info("No hay movimientos registrados en la base de datos.")
    else:
        if menu == "📊 Dashboard":
            dashboard.render(st.session_state["movimientos_df"], st.session_state["extractos_df"])
        elif menu == "💰 Ingresos":
            ingresos.render(st.session_state["movimientos_df"])
        elif menu == "💸 Egresos":
            egresos.render(st.session_state["movimientos_df"])
        elif menu == "📄 Subida de Extractos":
            subir.render(st.session_state["movimientos_df"])
        elif menu == "📑 Visor de PDFs":
            visor.render(st.session_state["movimientos_df"])
        elif menu == "📈 Reportes":
            reportes.render(st.session_state["movimientos_df"], st.session_state["extractos_df"])
        elif menu == "📝 Edición Manual":
            edicion.render(st.session_state["movimientos_df"])