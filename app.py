import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Innovatec: Presupuestos", page_icon="🛡️")

# 2. Función para las imágenes de Drive (Versión Thumbnail que funcionó)
def convertir_enlace_drive(url):
    if "drive.google.com" in str(url):
        # Extraer el ID del archivo
        if "file/d/" in url:
            id_foto = url.split('/')[-2]
        else:
            id_foto = url.split('id=')[-1].split('&')[0]
        # Usar el formato de thumbnail que es más rápido y estable
        return f"https://drive.google.com/thumbnail?id={id_foto}&sz=w600"
    return url

# 3. Función segura para leer el precio
def limpiar_precio(precio):
    # Si el precio ya es un número, lo devolvemos tal cual
    if isinstance(precio, (int, float)):
        return float(precio)
    
    # Si es texto, limpiamos S/, comas y espacios
    if isinstance(precio, str):
        precio_limpio = precio.replace('S/', '').replace('s/', '').replace(',', '').strip()
        try:
            return float(precio_limpio)
        except ValueError:
            return 0.0  # Si falla, devolvemos 0
    return 0.0

# 4. Carga de datos
try:
    # Asegúrate de que en GitHub el archivo se llame productos.csv
    df = pd.read_csv("productos.csv")
except FileNotFoundError:
    st.error("⚠️ No se encontró el archivo 'productos.csv'. Verifica el nombre en GitHub.")
    st.stop()

st.title("🛡️ Innovatec: Presupuestos")

# 5. Inicializar carrito
if 'carrito' not in st.session_state:
    st.session_state.carrito = []

# 6. Selección de producto
producto_sel = st.selectbox("Seleccione un producto:", df["Producto"].unique())

# Obtener los datos del producto seleccionado
datos = df[df["Producto"] == producto_sel].iloc[0]

# --- INTERFAZ PRINCIPAL ---
col1, col2 = st.columns([1, 1])

with col1:
    # Mostrar imagen
    url_limpia = convertir_enlace_drive(datos["Foto"])
    st.image(url_limpia, width=300, caption=producto_sel)

with col2:
    # Procesar precio usando la función de limpieza
    precio_unitario = limpiar_precio(datos['Precio_Unitario'])
    
    st.write(f"### Precio: S/ {precio_unitario:,.2f}")
    st.write(f"**Descripción:** {datos['
