import streamlit as st
import pandas as pd
import re

# 1. Configuración de la página
st.set_page_config(page_title="Innovatec j.a : Presupuestos", page_icon="🛡️")

# 2. Funciones de utilidad (Imágenes y Limpieza de precios)
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
    solo_numeros = re.sub(r'[^0-9.]', '', str(precio).replace(',', '.'))
    try: return float(solo_numeros)
    except: return 0.0

# 3. Carga de datos
try:
    df = pd.read_csv("productos.csv")
except FileNotFoundError:
    st.error("⚠️ No se encontró el archivo 'productos.csv'.")
    st.stop()

st.title("🛡️ Innovatec: Presupuestos")

# 4. Inicializar carrito con un ID único para poder borrar
if 'carrito' not in st.session_state:
    st.session_state.carrito = []

# 5. Selección de producto
producto_sel = st.selectbox("Seleccione un producto:", df["Producto"].unique())
datos = df[df["Producto"] == producto_sel].iloc[0]

col1, col2 = st.columns([1, 1])
with col1:
    url_limpia = convertir_enlace_drive(datos["Foto"])
    if url_limpia: st.image(url_limpia, width=300)

with col2:
    precio_unitario = limpiar_precio(datos['Precio_Unitario'])
    st.write(f"### Precio: S/ {precio_unitario:,.2f}")
    st.write(f"**Descripción:** {datos['Descripción']}")
    cantidad = st.number_input("Cantidad:", min_value=1, value=1)
    
    if st.button("🛒 Agregar al presupuesto"):
        # Guardamos un diccionario con un 'id' basado en el momento actual para borrarlo luego
        nuevo_item = {
            "Producto": producto_sel,
            "Cantidad": cantidad,
            "Precio_Unitario": precio_unitario,
            "Subtotal": cantidad * precio_unitario
        }
        st.session_state.carrito.append(nuevo_item)
        st.success(f"¡{producto_sel} agregado!")
        st.rerun()

# 6. RESUMEN Y GESTIÓN DE BORRADO
if st.session_state.carrito:
    st.divider()
    st.header("📋 Detalle del Presupuesto")
    
    # Creamos una lista para saber qué índices borrar
    for index, item in enumerate(st.session_state.carrito):
        col_prod, col_cant, col_sub, col_borrar = st.columns([3, 1, 2, 1])
        
        with col_prod:
            st.write(f"**{item['Producto']}**")
        with col_cant:
            st.write(f"x{item['Cantidad']}")
        with col_sub:
            st.write(f"S/ {item['Subtotal']:,.2f}")
        with col_borrar:
            # El botón de borrar usa el índice de la lista
            if st.button("❌", key=f"btn_{index}"):
                st.session_state.carrito.pop(index)
                st.rerun()

    # Total Final
    total_final = sum(item['Subtotal'] for item in st.session_state.carrito)
    st.subheader(f"Total Final: S/ {total_final:,.2f}")
    
    if st.button("🗑️ Vaciar todo el presupuesto"):
        st.session_state.carrito = []
        st.rerun()

