import streamlit as st
import pandas as pd

# 1. Configuración y carga de datos
st.set_page_config(page_title="Innovatec Presupuestos", layout="centered")

@st.cache_data
def load_data():
    return pd.read_csv("productos.csv")

df = load_data()

# 2. Función mágica para las fotos de Drive
def convertir_enlace_drive(url):
    if "drive.google.com" in str(url):
        # Extrae el ID del archivo del enlace de compartir
        if "file/d/" in url:
            id_foto = url.split('/')[-2]
        else:
            id_foto = url.split('id=')[-1].split('&')[0]
        return f"https://drive.google.com/uc?export=view&id={id_foto}"
    return url

st.title("🛡️ Innovatec: Presupuestos")

# 3. Carrito de compras
if 'carrito' not in st.session_state:
    st.session_state.carrito = []

# 4. Selector de productos
producto_sel = st.selectbox("Buscar producto:", df["Producto"].unique())
datos = df[df["Producto"] == producto_sel].iloc[0]

# 5. Mostrar Ficha Técnica
col1, col2 = st.columns([1, 1])

with col1:
    url_limpia = convertir_enlace_drive(datos["Foto"])
    # Aquí es donde ocurre la magia: ya no saldrá el icono roto
    st.image(url_limpia, width=250, caption=producto_sel)

with col2:
    st.write(f"### Precio: S/ {datos['Precio_Unitario']}")
    st.write(f"**Descripción:** {datos['Descripción']}")
    cantidad = st.number_input("Cantidad:", min_value=1, value=1)

if st.button("🛒 Agregar al presupuesto"):
    st.session_state.carrito.append({
        "Producto": producto_sel,
        "Cantidad": cantidad,
        "Subtotal": cantidad * datos["Precio_Unitario"]
    })
    st.success(f"¡{producto_sel} añadido!")

# 6. Tabla del presupuesto acumulado
if st.session_state.carrito:
    st.divider()
    st.subheader("Tu Presupuesto Actual")
    tabla_df = pd.DataFrame(st.session_state.carrito)
    st.table(tabla_df)
    st.header(f"Total: S/ {tabla_df['Subtotal'].sum():.2f}")
