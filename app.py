import streamlit as st
import pandas as pd
import re

# 1. Configuración de la página
st.set_page_config(page_title="Innovatec J.A", page_icon="🛡️", layout="wide")

# --- CSS PARA FORZAR DISEÑO HORIZONTAL Y BOTÓN X MINÚSCULO ---
st.markdown("""
    <style>
    /* Forzar que las columnas NO se apilen en móviles */
    [data-testid="column"] {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: flex-start !important;
        width: auto !important;
    }

    /* Botón X atómico y centrado */
    div[data-testid="column"] button {
        height: 12px !important;
        width: 12px !important;
        min-height: 12px !important;
        min-width: 12px !important;
        padding: 0px !important;
        font-size: 7px !important;
        line-height: 1 !important;
        border-radius: 2px !important;
        border: 1px solid rgba(255, 75, 75, 0.4) !important;
        color: #ff4b4b !important;
        background-color: transparent !important;
    }

    /* Ajuste de texto para que quepa todo en una línea */
    .table-text { font-size: 13px !important; }
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

st.title("🛡️ Innovatec J.A")

if 'carrito' not in st.session_state:
    st.session_state.carrito = []

# 4. Selección de producto
producto_sel = st.selectbox("Seleccione un producto:", df["Producto"].unique())
datos = df[df["Producto"] == producto_sel].iloc[0]

c1, c2 = st.columns([1, 1])
with c1:
    url_limpia = convertir_enlace_drive(datos["Foto"])
    if url_limpia: st.image(url_limpia, width=280)

with c2:
    precio_unitario = limpiar_precio(datos['Precio_Unitario'])
    st.write(f"### S/ {precio_unitario:,.2f}")
    st.write(f"**Descripción:** {datos['Descripción']}")
    cantidad = st.number_input("Cantidad:", min_value=1, value=1)
    if st.button("🛒 Agregar al presupuesto"):
        st.session_state.carrito.append({
            "Producto": producto_sel,
            "Cantidad": cantidad,
            "Precio": precio_unitario,
            "Subtotal": cantidad * precio_unitario
        })
        st.rerun()

# 5. RESUMEN HORIZONTAL (Corregido para móviles)
if st.session_state.carrito:
    st.divider()
    st.header("📋 Detalle del Presupuesto")
    
    # Encabezados - Usamos proporciones muy precisas
    h1, h2, h3, h4 = st.columns([4, 1, 2, 0.3])
    h1.write("**Producto**")
    h2.write("**Cant.**")
    h3.write("**Total**")
    h4.write("")

    for index, item in enumerate(st.session_state.carrito):
        # Creamos las filas. Eliminamos el error de la Captura 60 aquí:
        col_p, col_c, col_t, col_x = st.columns([4, 1, 2, 0.3])
        
        with col_p: st.markdown(f"<div class='table-text'>{item['Producto']}</div>", unsafe_allow_html=True)
        with col_c: st.markdown(f"<div class='table-text'>{item['Cantidad']}</div>", unsafe_allow_html=True)
        with col_t: st.markdown(f"<div class='table-text'>S/ {item['Subtotal']:,.2f}</div>", unsafe_allow_html=True)
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
