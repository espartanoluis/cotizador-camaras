import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Innovatec: Presupuestos", layout="centered")

# Función mejorada para las fotos de Drive
def convertir_enlace_drive(url):
    try:
        if "drive.google.com" in str(url):
            if "/d/" in url:
                id_foto = url.split('/d/')[1].split('/')[0]
            else:
                id_foto = url.split('id=')[1].split('&')[0]
            return f"https://drive.google.com/uc?export=view&id={id_foto}"
        return url
    except:
        return "https://via.placeholder.com/300?text=Error+en+Enlace"

# Cargar datos
@st.cache_data
def cargar_datos():
    return pd.read_csv("productos.csv")

try:
    df = cargar_datos()
    st.title("🛡️ Innovatec: Presupuestos")

    if 'carrito' not in st.session_state:
        st.session_state.carrito = []

    producto_sel = st.selectbox("Buscar producto:", df["Producto"].unique())
    datos = df[df["Producto"] == producto_sel].iloc[0]

    col1, col2 = st.columns([1, 1])

    with col1:
        url_limpia = convertir_enlace_drive(datos["Foto"])
        st.image(url_limpia, width=300)

    with col2:
        st.write(f"### Precio: S/ {datos['Precio_Unitario']:.2f}")
        st.write(f"**Descripción:** {datos['Descripción']}")
        cantidad = st.number_input("Cantidad:", min_value=1, value=1)
        
        if st.button("🛒 Agregar al presupuesto"):
            st.session_state.carrito.append({
                "Producto": producto_sel,
                "Cantidad": cantidad,
                "Subtotal": cantidad * datos["Precio_Unitario"]
            })
            st.success("¡Añadido!")

    if st.session_state.carrito:
        st.divider()
        st.subheader("Resumen de Cotización")
        resumen_df = pd.DataFrame(st.session_state.carrito)
        st.table(resumen_df)
        
        total = resumen_df["Subtotal"].sum()
        # LÍNEA CORREGIDA AQUÍ ABAJO
        st.header(f"Total a Pagar: S/ {total:.2f}")
        
        if st.button("🗑️ Vaciar Presupuesto"):
            st.session_state.carrito = []
            st.rerun()

except Exception as e:
    st.error(f"Error: {e}")
