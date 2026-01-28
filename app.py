import streamlit as st
import pandas as pd
import re

# 1. Configuración de la página
st.set_page_config(page_title="Innovatec J.A", page_icon="🛡️")

# --- ESTILO CSS PARA HACER EL BOTÓN X MÁS PEQUEÑO ---
st.markdown("""
    <style>
    div[data-testid="column"] button {
        height: 1.5rem !important;
        width: 1.5rem !important;
        padding: 0px !important;
        font-size: 10px !important;
        line-height: 1 !important;
        border-radius: 5px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Funciones de utilidad
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

st.title("🛡️ Innovatec J.A: Sistema de Presupuestos")

if 'carrito' not in st.session_state:
    st.session_state.carrito = []

# 5. Selector de producto
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
        st.session_state.carrito.append({
            "Producto": producto_sel,
            "Cantidad": cantidad,
            "Precio_Unitario": precio_unitario,
            "Subtotal": cantidad * precio_unitario
        })
        st.success("¡Agregado!")
        st.rerun()

# 6. Resumen con botones X pequeños
if st.session_state.carrito:
    st.divider()
    st.header("📋 Detalle del Presupuesto")
    
    for index, item in enumerate(st.session_state.carrito):
        # Ajustamos el ancho de las columnas para que la X tenga poco espacio
        c1, c2, c3, c4 = st.columns([4, 1, 2, 0.5])
        with c1: st.write(item['Producto'])
        with c2: st.write(f"x{item['Cantidad']}")
        with c3: st.write(f"S/ {item['Subtotal']:,.2f}")
        with c4:
            # El CSS de arriba hará que este botón sea pequeño
            if st.button("❌", key=f"del_{index}"):
                st.session_state.carrito.pop(index)
                st.rerun()

    total_final = sum(item['Subtotal'] for item in st.session_state.carrito)
    st.subheader(f"Total Final: S/ {total_final:,.2f}")
    
    if st.button("🗑️ Vaciar todo"):
        st.session_state.carrito = []
        st.rerun()
