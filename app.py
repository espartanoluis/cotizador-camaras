import streamlit as st
import pandas as pd
import re

# 1. Configuración de la página
st.set_page_config(page_title="Innovatec: Presupuestos", page_icon="🛡️")

# 2. Función para las imágenes de Drive (Mantenemos la que ya funciona)
def convertir_enlace_drive(url):
    if pd.isna(url) or str(url).lower() == "nan":
        return None
    url_str = str(url)
    if "drive.google.com" in url_str:
        if "file/d/" in url_str:
            id_foto = url_str.split('/')[-2]
        else:
            try:
                id_foto = url_str.split('id=')[-1].split('&')[0]
            except:
                return url_str
        return f"https://drive.google.com/thumbnail?id={id_foto}&sz=600"
    return url_str

# 3. FUNCIÓN DE LIMPIEZA MEJORADA PARA PRECIOS
def limpiar_precio(precio):
    if pd.isna(precio):
        return 0.0
    # Si ya es un número (flotante o entero), lo devolvemos
    if isinstance(precio, (int, float)):
        return float(precio)
    
    # Si es texto, extraemos solo los números y el punto decimal
    precio_texto = str(precio)
    # Usamos una expresión regular para quedarnos solo con dígitos y el punto
    solo_numeros = re.sub(r'[^0-9.]', '', precio_texto.replace(',', '.'))
    
    try:
        return float(solo_numeros)
    except ValueError:
        return 0.0

# 4. Carga de datos
try:
    # Nota: Si usas Google Sheets directo, asegúrate de que el CSV se actualice
    df = pd.read_csv("productos.csv")
except FileNotFoundError:
    st.error("⚠️ No se encontró el archivo 'productos.csv'.")
    st.stop()

st.title("🛡️ Innovatec: Presupuestos")

if 'carrito' not in st.session_state:
    st.session_state.carrito = []

# 5. Selector de productos
producto_sel = st.selectbox("Seleccione un producto:", df["Producto"].unique())
datos = df[df["Producto"] == producto_sel].iloc[0]

# --- INTERFAZ ---
col1, col2 = st.columns([1, 1])

with col1:
    url_limpia = convertir_enlace_drive(datos["Foto"])
    if url_limpia:
        st.image(url_limpia, width=300)
    else:
        st.warning("Imagen no disponible")

with col2:
    # Aplicamos la nueva limpieza de precio
    precio_unitario = limpiar_precio(datos['Precio_Unitario'])
    
    # Mostramos el precio real
    st.write(f"### Precio: S/ {precio_unitario:,.2f}")
    st.write(f"**Descripción:** {datos['Descripción']}")
    
    cantidad = st.number_input("Cantidad:", min_value=1, value=1)
    
    if st.button("🛒 Agregar al presupuesto"):
        st.session_state.carrito.append({
            "Producto": producto_sel,
            "Cantidad": cantidad,
            "Precio Unitario": precio_unitario,
            "Subtotal": cantidad * precio_unitario
        })
        st.success("¡Agregado!")

# 6. Resumen
if st.session_state.carrito:
    st.divider()
    st.header("📋 Resumen")
    df_resumen = pd.DataFrame(st.session_state.carrito)
    st.table(df_resumen)
    st.subheader(f"Total: S/ {df_resumen['Subtotal'].sum():,.2f}")
    
    if st.button("🗑️ Limpiar Todo"):
        st.session_state.carrito = []
        st.rerun()
