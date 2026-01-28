import streamlit as st
import pandas as pd

# Configuración básica
st.set_page_config(page_title="Innovatec: Presupuestos", layout="centered")

# Función para limpiar enlaces de Drive
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
        return "https://via.placeholder.com/300?text=Sin+Imagen"

# Cargar datos
@st.cache_data
def cargar_datos():
    df = pd.read_csv("productos.csv")
    # Aseguramos que el precio sea número
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
        url_limpia = convertir_enlace_drive(datos["Foto"])
        st.image(url_limpia, width=300)

    with col2:
        precio = datos['Precio_Unitario']
        st.subheader(f"Precio: S/ {precio}")
        st.write(f"**Descripción:** {datos['Descripción']}")
        cantidad = st.number_input("Cantidad:", min_value=1, value=1)
        
        if st.button("🛒 Agregar al presupuesto"):
            st.session_state.carrito.append({
                "Producto": producto_sel,
                "Cantidad": cantidad,
                "Subtotal": cantidad * precio
            })
            st.success("¡Añadido!")

    if st.session_state.carrito:
        st.divider()
        st.subheader("Resumen de Cotización")
        resumen_df = pd.DataFrame(st.session_state.carrito)
        st.table(resumen_df)
        
        total = resumen_df["Subtotal"].sum()
        st.header(f"Total: S/ {total}")
        
        if st.button("🗑️ Vaciar Todo"):
            st.session_state.carrito = []
            st.rerun()

except Exception as e:
    st.error(f"Asegúrate de que el archivo se llame productos.csv y no tenga errores. Error: {e}")
