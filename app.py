import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Innovatec: Presupuestos", page_icon="🛡️")

# 2. Función para las imágenes de Drive (Versión Thumbnail)
def convertir_enlace_drive(url):
    # Si no hay URL o está vacía, devuelve una imagen genérica o vacío
    if pd.isna(url) or str(url) == "nan":
        return None
        
    url_str = str(url)
    if "drive.google.com" in url_str:
        if "file/d/" in url_str:
            id_foto = url_str.split('/')[-2]
        else:
            try:
                id_foto = url_str.split('id=')[-1].split('&')[0]
            except IndexError:
                return url_str # Si falla el split, devuelve la original
        
        # Usar el formato thumbnail que funciona mejor
        return f"https://drive.google.com/thumbnail?id={id_foto}&sz=w600"
    return url_str

# 3. Función para limpiar y leer el precio correctamente
def limpiar_precio(precio):
    # Si ya es número, todo bien
    if isinstance(precio, (int, float)):
        return float(precio)
    
    # Si es texto, limpiamos símbolos
    if isinstance(precio, str):
        # Quitamos S/, espacios y comas
        precio_limpio = precio.replace('S/', '').replace('s/', '').replace(',', '').strip()
        try:
            return float(precio_limpio)
        except ValueError:
            return 0.0
    return 0.0

# 4. Carga de datos
try:
    df = pd.read_csv("productos.csv")
except FileNotFoundError:
    st.error("⚠️ No se encontró el archivo 'productos.csv'.")
    st.stop()

st.title("🛡️ Innovatec: Presupuestos")

# 5. Inicializar carrito
if 'carrito' not in st.session_state:
    st.session_state.carrito = []

# 6. Selector de productos
producto_sel = st.selectbox("Seleccione un producto:", df["Producto"].unique())

# Obtener datos del producto seleccionado
datos = df[df["Producto"] == producto_sel].iloc[0]

# --- MOSTRAR DETALLES ---
col1, col2 = st.columns([1, 1])

with col1:
    # Imagen
    url_limpia = convertir_enlace_drive(datos["Foto"])
    if url_limpia:
        st.image(url_limpia, width=300, caption=producto_sel)
    else:
        st.write("Sin imagen disponible")

with col2:
    # Precio (usando la función de limpieza para evitar errores)
    precio_unitario = limpiar_precio(datos['Precio_Unitario'])
    
    # Mostrar Precio
    st.write(f"### Precio: S/ {precio_unitario:,.2f}")
    
    # Mostrar Descripción (Aquí estaba el error de sintaxis, ya corregido)
    st.write(f"**Descripción:** {datos['Descripción']}")
    
    # Selector de cantidad
    cantidad = st.number_input("Cantidad:", min_value=1, value=1)
    
    # Botón agregar
    if st.button("🛒 Agregar al presupuesto"):
        item = {
            "Producto": producto_sel,
            "Cantidad": cantidad,
            "Precio Unitario": precio_unitario,
            "Subtotal": cantidad * precio_unitario
        }
        st.session_state.carrito.append(item)
        st.success(f"¡{producto_sel} agregado!")

# 7. Tabla de Resumen
if st.session_state.carrito:
    st.divider()
    st.header("📋 Resumen del Presupuesto")
    
    df_carrito = pd.DataFrame(st.session_state.carrito)
    st.table(df_carrito)
    
    total = df_carrito["Subtotal"].sum()
    st.subheader(f"Total Final: S/ {total:,.2f}")
    
    if st.button("🗑️ Vaciar Carrito"):
        st.session_state.carrito = []
        st.rerun()
