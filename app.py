import streamlit as st
import pandas as pd
import re

# Configuración de página
st.set_page_config(page_title="Innovatec: Presupuestos", layout="centered")

# FUNCIÓN MAESTRA PARA IMÁGENES DE DRIVE
def obtener_link_directo(url):
    if not isinstance(url, str) or "drive.google.com" not in url:
        return None
    try:
        # Extrae el ID del archivo de cualquier formato de link de Drive
        match = re.search(r'[-\w]{25,}', url)
        if match:
            return f"https://drive.google.com/uc?export=view&id={match.group()}"
    except:
        return None
    return None

# CARGAR Y LIMPIAR DATOS
@st.cache_data
def cargar_datos():
    df = pd.read_csv("productos.csv")
    # Limpia el precio eliminando "S/", comas y espacios para que no salga 0.0
    def limpiar_precio(valor):
        if isinstance(valor, str):
            valor = re.sub(r'[^\d.]', '', valor)
        try:
            return float(valor)
        except:
            return 0.0
            
    df["Precio_Unitario"] = df["Precio_Unitario"].apply(limpiar_precio)
    return df

try:
    df = cargar_datos()
    st.title("🛡️ Innovatec: Presupuestos")

    if 'carrito' not in st.session_state:
        st.session_state.carrito = []

    producto_sel = st.selectbox("Seleccione un producto:", df["Producto"].unique())
    datos = df[df["Producto"] == producto_sel].iloc[0]

    col1, col2 = st.columns([1, 1])

    with col1:
        foto_url = obtener_link_directo(datos["Foto"])
        if foto_url:
            # Forzamos la visualización de la imagen
            st.image(foto_url, width=300, caption=producto_sel)
        else:
            st.warning("⚠️ Sin imagen disponible")

    with col2:
        st.subheader(f"Precio: S/ {datos['Precio_Unitario']:.2f}")
        st.info(f"**Descripción:** {datos['Descripción']}")
        cantidad = st.number_input("Cantidad:", min_value=1, value=1, step=1)
        
        if st.button("🛒 Agregar al presupuesto"):
            st.session_state.carrito.append({
                "Producto": producto_sel,
                "Cantidad": cantidad,
                "Subtotal": cantidad * datos['Precio_Unitario']
            })
            st.success("¡Agregado!")

    if st.session_state.carrito:
        st.divider()
        st.subheader("📋 Resumen de Cotización")
        resumen_df = pd.DataFrame(st.session_state.carrito)
        st.table(resumen_df)
        total = resumen_df["Subtotal"].sum()
        st.header(f"Total: S/ {total:.2f}")
        
        if st.button("🗑️ Vaciar Carrito"):
            st.session_state.carrito = []
            st.rerun()

except Exception as e:
    st.error(f"Error cargando el archivo: {e}")
