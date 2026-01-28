import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Innovatec: Presupuestos", page_icon="🛡️")

# 2. Función para convertir links de Drive en imágenes directas
def convertir_enlace_drive(url):
    if "drive.google.com" in str(url):
        # Extraer el ID del archivo
        if "file/d/" in url:
            id_foto = url.split('/')[-2]
        else:
            id_foto = url.split('id=')[-1].split('&')[0]
        # Usar el formato de thumbnail de Google que es más estable
        return f"https://drive.google.com/thumbnail?id={id_foto}&sz=w600"
    return url

# 3. Carga de datos
# Asegúrate de que el nombre coincida exactamente con tu archivo en GitHub
try:
    df = pd.read_csv("productos.csv")
except FileNotFoundError:
    st.error("No se encontró el archivo productos.csv. Verifica el nombre en GitHub.")
    st.stop()

st.title("🛡️ Innovatec: Presupuestos")

# 4. Inicializar el carrito de compras
if 'carrito' not in st.session_state:
    st.session_state.carrito = []

# 5. Selector de productos
producto_sel = st.selectbox("Seleccione un producto:", df["Producto"].unique())
datos = df[df["Producto"] == producto_sel].iloc[0]

# 6. Mostrar Ficha Técnica
col1, col2 = st.columns([1, 1])

with col1:
    url_limpia = convertir_enlace_drive(datos["Foto"])
    st.image(url_limpia, width=300, caption=producto_sel)

with col2:
    # Corrección del error de formato: convertimos a float por seguridad
    precio_unitario = float(datos['Precio_Unitario'])
    st.write(f"### Precio: S/ {precio_unitario:,.2f}")
    
    st.write(f"**Descripción:** {datos['Descripción']}")
    cantidad = st.number_input("Cantidad:", min_value=1, value=1)

if st.button("🛒 Agregar al presupuesto"):
    item = {
        "Producto": producto_sel,
        "Cantidad": cantidad,
        "Precio_Unitario": precio_unitario,
        "Subtotal": cantidad * precio_unitario
    }
    st.session_state.carrito.append(item)
    st.success(f"Agregado: {producto_sel} x{cantidad}")

# 7. Resumen del Presupuesto (Aquí estaba el error de la línea 69)
if st.session_state.carrito:
    st.divider()
    st.header("📋 Resumen del Presupuesto")
    
    # Convertir el carrito a DataFrame para mostrarlo como tabla
    df_carrito = pd.DataFrame(st.session_state.carrito)
    st.table(df_carrito)
    
    total = df_carrito["Subtotal"].sum()
    st.subheader(f"Total Final: S/ {total:,.2f}")

    if st.button("Limpiar presupuesto"):
        st.session_state.carrito = []
        st.rerun()
