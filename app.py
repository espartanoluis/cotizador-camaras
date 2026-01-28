import streamlit as st
import pandas as pd
import re

# 1. Configuración de la página
st.set_page_config(page_title="Innovatec J.A", page_icon="🛡️")

# --- CSS PARA REDUCIR EL BOTÓN Y SU RECUADRO ---
st.markdown("""
    <style>
    /* Reduce el tamaño del botón */
    div[data-testid="column"] button {
        height: 20px !important;
        width: 20px !important;
        min-height: 20px !important;
        min-width: 20px !important;
        padding: 0px !important;
        font-size: 10px !important;
        line-height: 1 !important;
        border-radius: 4px !important;
        margin-top: 5px !important;
    }
    
    /* Reduce el espacio vertical entre filas del presupuesto */
    [data-testid="column"] {
        display: flex;
        align-items: center;
        justify-content: center;
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

# 6. Resumen con recuadro de X reducido
if st.session_state.carrito:
    st.divider()
    st.header("📋 Detalle del Presupuesto")
    
    # Encabezados
    h1, h2, h3, h4 = st.columns([4, 1, 2, 0.5])
    h1.write("**Producto**")
    h2.write("**Cant.**")
    h3.write("**Total**")
    h4.write("") # Espacio para la X

    for index, item in enumerate(st.session_state.carrito):
        # El 0.5 final hace que la columna de la X sea muy estrecha
        c1, c2, c3, c4 = st.columns([4, 1, 2, 0.5])
        with c1: st.write(item['Producto'])
        with c2: st.write(f"{item['Cantidad']}")
        with c3: st.write(f"S/ {item['Subtotal']:,.2f}")
        with c4:
            if st.button("❌", key=f"del_{index}"):
                st.session_state.carrito.pop(index)
                st.rerun()

    total_final = sum(item['Subtotal'] for item in st.session_state.carrito)
    st.divider()
    st.subheader(f"Total Final: S/ {total_final:,.2f}")
    
    if st.button("🗑️ Vaciar todo"):
        st.session_state.carrito = []
        st.rerun()
