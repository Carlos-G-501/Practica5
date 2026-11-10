import streamlit as st
from config.conexion import obtener_conexion


def mostrar_venta():
    st.header("Registrar venta")

    with st.form("form_venta"):
        producto = st.text_input(
            "Nombre del producto"
        )
        cantidad = st.number_input(
            "Cantidad",
            min_value=1,
            step=1
        )
        guardar = st.form_submit_button(
            "Guardar venta"
        )

    if guardar:
        if producto.strip() == "":
            st.warning(
                "Debe ingresar el nombre del producto."
            )
        else:
            conexion = None
            cursor = None
            try:
                conexion = obtener_conexion()
                if conexion is None:
                    return

                cursor = conexion.cursor()
