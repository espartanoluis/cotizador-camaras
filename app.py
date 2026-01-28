import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Innovatec: Presupuestos", layout="centered")

# FUNCIÓN DE IMAGEN MEJORADA
def obtener_link_directo(url):
    if "drive.google.com" in str(url):
        try:
            # Extraer el ID del archivo
            if "/d/" in url:
                file_id = url.split("/d/")[1].split("/")[0]
            else:
                file_id = url.split("id=")[1].split("&")[0]
            return f"https://drive.google.com/uc?export=view&id={file_id}"
        except:
            return None
    return url

# Cargar datos
@st.cache_data
def cargar_datos():
    # Asegúrate de que tu archivo en GitHub se llame productos.csv
    df = pd.read_csv("productos.csv")
    df["Precio_Unitario"] = pd.to_numeric(df["Precio_Unitario"], errors='coerce').fillna(0)
    return df

try:
    df = cargar_datos()
    st.title("🛡️ Innovatec: Presupuestos")

    if 'carrito' not in st.session_state:
        st.session_state.carrito = []

    producto_sel = st.selectbox("Buscar producto:", df["Producto"].unique())
    datos = df[df["Producto"] == producto_sel].iloc[0]

    col1, col2 = st.columns([1, 1])

    with col1:
        link_foto = obtener_link_directo(datos["Foto"])
        if link_foto:
            # Mostramos la imagen. Si falla, mostrará el texto alternativo
            st.image(link_foto, width=300, caption=producto_sel)
        else:
            st.warning("No se encontró el enlace de la imagen.")

    with col2:
        st.subheader(f"Precio: S/ {datos['Precio_Unitario']}")
        st.write(f"**Descripción:** {datos['Descripción']}")
        cantidad = st.number_input("Cantidad:", min_value=1, value=1)
        
        if st.button("🛒 Agregar al presupuesto"):
            st.session_state.carrito.append({
                "Producto": producto_sel,
                "Cantidad": cantidad,
                "Subtotal": cantidad * datos['Precio_Unitario']
            })
            st.success("¡Añadido!")

    if st.session_state.carrito:
        st.divider()
        st.subheader("Resumen de Cotización")
        resumen_df = pd.DataFrame(st.session_state.carrito)
        st.table(resumen_df)
        st.header(f"Total: S/ {resumen_df['Subtotal'].sum()}")
        
        if st.button("🗑️ Vaciar Todo"):
            st.session_state.carrito = []
            st.rerun()

except Exception as e:
    st.error(f"Error técnico: {e}")
