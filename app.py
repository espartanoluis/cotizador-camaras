import streamlit as st
import pandas as pd

st.set_page_config(page_title="Innovatec App", layout="centered")

# Cargar datos
df = pd.read_csv("productos.csv")

st.title("🛡️ Innovatec: Presupuestos")

# Inicializar el carrito de compras si no existe
if 'carrito' not in st.session_state:
    st.session_state.carrito = []

# Selector de producto
producto_sel = st.selectbox("Buscar producto:", df["Producto"].unique())
datos = df[df["Producto"] == producto_sel].iloc[0]

# Mostrar información
col1, col2 = st.columns([1, 1])
with col1:
    # Ajuste para enlaces de Drive
    id_foto = datos["Foto"].split('/')[-2] if "file/d/" in datos["Foto"] else ""
    url_directa = f"https://drive.google.com/uc?export=view&id={id_foto}"
    st.image(url_directa, width=180)

with col2:
    st.write(f"**Precio:** S/ {datos['Precio_Unitario']}")
    st.caption(datos["Descripción"])
    cantidad = st.number_input("Cantidad:", min_value=1, value=1)

if st.button("🛒 Agregar al presupuesto"):
    item = {
        "Producto": producto_sel,
        "Cantidad": cantidad,
        "Subtotal": cantidad * datos["Precio_Unitario"]
    }
    st.session_state.carrito.append(item)
    st.success("¡Agregado!")

# Mostrar Resumen
if st.session_state.carrito:
    st.divider()
    st.subheader("Resumen del Trabajo")
    resumen_df = pd.DataFrame(st.session_state.carrito)
    st.table(resumen_df)
    total = resumen_df["Subtotal"].sum()
    st.header(f"Total: S/ {total:.2f}")