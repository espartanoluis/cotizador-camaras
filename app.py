import streamlit as st
import pandas as pd
import re

# 1. Configuración de la página - AQUÍ SE CAMBIÓ EL TÍTULO
st.set_page_config(page_title="Innovatec J.A", page_icon="🛡️")

# 2. Funciones de utilidad (Imágenes de Drive y Limpieza de precios)
def convertir_enlace_drive(url):
    if pd.isna(url) or str(url).lower() == "nan": return None
    url_str = str(url)
    if "drive.google.com" in url_str:
        if "file/d/" in url_str: id_foto = url_str.split('/')[-2]
        else:
            try: id_foto = url_str.split('id=')[-1].split('&')[0]
            except: return url_str
        return f"https://drive.google.com/thumbnail?id={id_foto}&sz=600"
    return url_str

def limpiar_precio(precio):
    if pd.isna(precio): return 0.0
    if isinstance(precio, (int, float)): return float(precio)
    # Extraemos solo números y puntos para evitar errores de formato
    solo_numeros = re.sub(r'[^0-9.]', '', str(precio).replace(',', '.'))
    try: return float(solo_numeros)
    except: return 0.0

# 3. Carga de datos
try:
    df = pd.read_csv("productos.csv")
except FileNotFoundError:
    st.error("⚠️ No se encontró el archivo 'productos.csv'. Verifica que el nombre sea correcto en GitHub.")
    st.stop()

# Título visual en la aplicación
st.title("🛡️ Innovatec J.A: Sistema de Presupuestos")

# 4. Inicializar el carrito en la sesión del usuario
if 'carrito' not in st.session_state:
    st.session_state.carrito = []

# 5. Selector de producto y visualización de detalles
producto_sel = st.selectbox("Seleccione un producto:", df["Producto"].unique())
datos = df[df["Producto"] == producto_sel].iloc[0]

col1, col2 = st.columns([1, 1])
with col1:
    url_limpia = convertir_enlace_drive(datos["Foto"])
    if url_limpia: 
        st.image(url_limpia, width=300)

with col2:
    precio_unitario = limpiar_precio(datos['Precio_Unitario'])
    st.write(f"### Precio: S/ {precio_unitario:,.2f}")
    st.write(f"**Descripción:** {datos['Descripción']}")
    cantidad = st.number_input("Cantidad:", min_value=1, value=1)
    
    if st.button("🛒 Agregar al presupuesto"):
        nuevo_item = {
            "Producto": producto_sel,
            "Cantidad": cantidad,
            "Precio_Unitario": precio_unitario,
            "Subtotal": cantidad * precio_unitario
        }
        st.session_state.carrito.append(nuevo_item)
        st.success(f"¡{producto_sel} añadido con éxito!")
        st.rerun()

# 6. Gestión del Resumen (Borrado de ítems por separado)
if st.session_state.carrito:
    st.divider()
    st.header("📋 Detalle del Presupuesto")
    
    # Encabezados de la tabla de resumen
    header_cols = st.columns([3, 1, 2, 1])
    header_cols[0].write("**Producto**")
    header_cols[1].write("**Cant.**")
    header_cols[2].write("**Subtotal**")
    header_cols[3].write("**Acción**")

    # Mostrar cada producto con su botón de eliminar
    for index, item in enumerate(st.session_state.carrito):
        c1, c2, c3, c4 = st.columns([3, 1, 2, 1])
        with c1: st.write(item['Producto'])
        with c2: st.write(f"x{item['Cantidad']}")
        with c3: st.write(f"S/ {item['Subtotal']:,.2f}")
        with c4:
            if st.button("❌", key=f"del_{index}"):
                st.session_state.carrito.pop(index)
                st.rerun()

    # Cálculo del total final
    total_final = sum(item['Subtotal'] for item in st.session_state.carrito)
    st.subheader(f"Total Final: S/ {total_final:,.2f}")
    
    if st.button("🗑️ Vaciar todo"):
        st.session_state.carrito = []
        st.rerun()
