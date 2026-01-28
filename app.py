import streamlit as st
import pandas as pd
import re

# 1. Configuración de la página
st.set_page_config(page_title="Innovatec J.A", page_icon="🛡️", layout="wide")

# --- CSS PARA FORZAR DISEÑO HORIZONTAL EN MÓVILES ---
st.markdown("""
    <style>
    /* Forzar que las columnas del presupuesto NO se apilen en móvil */
    [data-testid="column"] {
        flex-direction: row !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        width: auto !important;
        min-width: 0px !important;
    }

    /* Contenedor de la fila de productos */
    .row-container {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #444;
        padding: 5px 0px;
    }

    /* Botón X minúsculo y sin márgenes */
    div[data-testid="column"] button {
        height: 18px !important;
        width: 18px !important;
        min-height: 18px !important;
        min-width: 18px !important;
        padding: 0px !important;
        margin: 0px !important;
        font-size: 9px !important;
        border-radius: 50% !important; /* Circular para que ocupe menos espacio visual */
        border: 1px solid rgba(255, 75, 75, 0.5) !important;
        background-color: transparent !important;
        color: #ff4b4b !important;
    }

    /* Estilo para los textos del presupuesto para que no se corten */
    .product-text { font-size: 14px; font-weight: 500; }
    .price-text { font-size: 14px; color: #00ff00; }
    </style>
    """, unsafe_allow_html=True)

# 2. Funciones de utilidad (Drive y Precios)
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

st.title("🛡️ Innovatec J.A")

if 'carrito' not in st.session_state:
    st.session_state.carrito = []

# 4. Selección de producto
producto_sel = st.selectbox("Seleccione un producto:", df["Producto"].unique())
datos = df[df["Producto"] == producto_sel].iloc[0]

c_img, c_det = st.columns([1, 1])
with c_img:
    url_limpia = convertir_enlace_drive(datos["Foto"])
    if url_limpia: st.image(url_limpia, width=250)

with c_det:
    precio_unitario = limpiar_precio(datos['Precio_Unitario'])
    st.subheader(f"S/ {precio_unitario:,.2f}")
    st.write(f"{datos['Descripción']}")
    cantidad = st.number_input("Cantidad:", min_value=1, value=1)
    if st.button("🛒 Agregar"):
        st.session_state.carrito.append({
            "Producto": producto_sel,
            "Cantidad": cantidad,
            "Precio": precio_unitario,
            "Subtotal": cantidad * precio_unitario
        })
        st.rerun()

# 5. RESUMEN HORIZONTAL (Incluso en móviles)
if st.session_state.carrito:
    st.divider()
    st.markdown("### 📋 Resumen del Presupuesto")
    
    # Encabezado Manual (Fila única)
    # Proporciones: [Producto, Cant, Total, X] -> [5, 1, 2, 0.5]
    h1, h2, h3, h4 = st.columns([5, 1.5, 2.5, 0.8])
    h1.caption("**Producto**")
    h2.caption("**Cant.**")
    h3.caption("**Total**")
    h4.caption("")

    for index, item in enumerate(st.session_state.carrito):
        # Cada producto es una fila de columnas que NO se apilan
        col_p, col_c, col_t, col_x = st.columns([5, 1.5, 2.5, 0.8])
        
        with col_p: st.markdown(f"<span class='product-text'>{item['Producto']}</span>", unsafe_allow_html=True)
        with col_c: st.write(f"x{item['Cantidad']}")
        with c_t := col_t: st.markdown(f"<span class='price-text'>S/ {item['Subtotal']:,.2f}</span>", unsafe_allow_html=True)
        with col_x:
            if st.button("x", key=f"del_{index}"):
                st.session_state.carrito.pop(index)
                st.rerun()

    total_final = sum(i['Subtotal'] for i in st.session_state.carrito)
    st.divider()
    st.subheader(f"Total Final: S/ {total_final:,.2f}")
    
    if st.button("🗑️ Vaciar todo"):
        st.session_state.carrito = []
        st.rerun()
