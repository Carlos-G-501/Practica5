import streamlit as st
from config.conexion import obtener_conexion


def registrar_producto(nombre, precio, stock):
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        if conexion is None:
            return False

        cursor = conexion.cursor()
        consulta = """
            INSERT INTO PRODUCTOS (Nombre, Precio, Stock)
            VALUES (%s, %s, %s)
        """
        cursor.execute(consulta, (nombre, float(precio), int(stock)))
        conexion.commit()
        return True

    except Exception as error:
        if conexion is not None:
            conexion.rollback()
        st.error(f"Error al registrar el producto: {error}")
        return False

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()


def obtener_productos():
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        if conexion is None:
            return []

        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT Id_Producto, Nombre, Precio, Stock
            FROM PRODUCTOS
            ORDER BY Id_Producto DESC
        """)
        return cursor.fetchall()

    except Exception as error:
        st.error(f"Error al obtener los productos: {error}")
        return []

    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()


def mostrar_productos():
    st.header("Gestión de productos")
    st.write("Registre nuevos productos y consulte el catálogo disponible.")

    with st.form("form_producto", clear_on_submit=True):
        nombre = st.text_input("Nombre del producto")
        precio = st.number_input("Precio ($)", min_value=0.01, step=0.50, format="%.2f")
        stock = st.number_input("Stock disponible", min_value=0, step=1)
        guardar = st.form_submit_button("Guardar producto")

    if guardar:
        if nombre.strip() == "":
            st.warning("Debe ingresar el nombre del producto.")
        else:
            if registrar_producto(nombre.strip(), precio, stock):
                st.success("Producto registrado correctamente.")

    st.subheader("Productos registrados")
    productos = obtener_productos()

    if productos:
        st.dataframe(productos, use_container_width=True, hide_index=True)
    else:
        st.info("Aún no hay productos registrados.")
      
