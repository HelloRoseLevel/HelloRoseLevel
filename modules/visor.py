import streamlit as st
from modules.drive_utils import listar_pdfs_en_drive2
import pandas as pd


def render(movimientos_df):
    """Lista los PDFs en la carpeta 'Extractos' de Drive y muestra los movimientos asociados a cada PDF."""
    st.title("📑 Visor de PDFs en Google Drive")
    st.caption("Selecciona un PDF de la carpeta 'Extractos' en Drive para ver los movimientos asociados.")

    # Usar directamente el folder_id de secrets
    folder_id = st.secrets["google"]["drive_folder_id"]

    if not folder_id:
        st.info("No se encontró la carpeta 'Extractos' en Drive.")
        return

    pdfs = listar_pdfs_en_drive2(folder_id)
    if not pdfs:
        st.info("No se encontraron archivos PDF en la carpeta 'Extractos'.")
        return

    pdf_names = [pdf['name'] for pdf in pdfs]
    selected_pdf = st.selectbox("Selecciona un PDF", pdf_names)

    st.write(f"**Archivo seleccionado:** {selected_pdf}")

    if 'archivo' in movimientos_df.columns:
        movs_pdf = movimientos_df[movimientos_df['archivo'] == selected_pdf]
        if not movs_pdf.empty:
            st.subheader("Movimientos asociados a este PDF")
            columnas = ["fecha", "banco", "descripción", "categoría", "monto", "archivo"]
            for col in columnas:
                if col not in movs_pdf.columns:
                    movs_pdf[col] = ""
            st.dataframe(movs_pdf[columnas], use_container_width=True)
        else:
            st.info("No hay movimientos asociados a este PDF.")
    else:
        st.warning("No se encuentra la columna 'archivo' en los movimientos.")


# ...existing code...

    # --- Edición manual de movimientos asociados al PDF seleccionado ---
    st.markdown("---")
    st.subheader("Editar movimientos de este PDF")

    if not movs_pdf.empty:
        selected_edit = st.selectbox("Selecciona el ID de movimiento a editar", movs_pdf["id"].tolist(), key="edit_selectbox")
        if selected_edit:
            row = movs_pdf[movs_pdf["id"] == selected_edit].iloc[0]
            with st.form(f"form_edicion_pdf_{selected_edit}"):
                fecha = st.date_input("Fecha", pd.to_datetime(row["fecha"]), key=f"fecha_{selected_edit}")
                banco = st.text_input("Banco", row["banco"], key=f"banco_{selected_edit}")
                monto = st.number_input("Monto", value=float(row["monto"]), step=0.01, key=f"monto_{selected_edit}")
                tipo = st.selectbox("Tipo", ["ingreso", "egreso"], index=["ingreso", "egreso"].index(row["tipo"]), key=f"tipo_{selected_edit}")
                descripcion = st.text_input("Descripción", row["descripción"], key=f"desc_{selected_edit}")
                categoria = st.text_input("Categoría", row["categoría"], key=f"cat_{selected_edit}")
                extracto_id = st.text_input("Extracto ID", row.get("extracto_id", ""), key=f"extracto_{selected_edit}")
                origen_dato = st.text_input("Origen Dato", row.get("origen_dato", ""), key=f"origen_{selected_edit}")
                submit = st.form_submit_button("Guardar cambios")

            if submit:
                import datetime
                from gspread_dataframe import set_with_dataframe
                from modules.sheets_utils import get_google_sheets_client

                data_edit = {
                    "id": row["id"],
                    "fecha": fecha.strftime("%Y-%m-%d"),
                    "banco": banco,
                    "monto": monto,
                    "tipo": tipo,
                    "descripción": descripcion,
                    "categoría": categoria,
                    "extracto_id": extracto_id,
                    "origen_dato": origen_dato,
                    "editado_por": st.session_state.get("username", "anon"),
                    "fecha_edicion": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                # Actualizar en Google Sheets (nombre de hoja: "movimientos")
                gc = get_google_sheets_client()
                sheet_id = st.secrets["google"]["spreadsheet_id"]
                sh = gc.open_by_key(sheet_id)
                worksheet = sh.worksheet("movimientos")
                df_all = pd.DataFrame(worksheet.get_all_records())
                idx = df_all[df_all["id"] == row["id"]].index
                if not idx.empty:
                    for col in data_edit:
                        df_all.at[idx[0], col] = data_edit[col]
                    set_with_dataframe(worksheet, df_all)
                    st.success("¡Movimiento actualizado!")
                else:
                    st.error("No se encontró el movimiento para actualizar.")
    else:
        st.info("No hay movimientos para editar en este PDF.")