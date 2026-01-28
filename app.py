import streamlit as st
import pandas as pd
import re

# 1. Configuración de la página
st.set_page_config(page_title="Innovatec J.A", page_icon="🛡️", layout="wide")

# --- CSS PARA MAXIMIZAR EL ESPACIO EN MÓVIL ---
st.markdown("""
    <style>
    .reportview-container .main .block-container { padding-top: 1rem; }
    .product-row {
        display: flex;
        justify-content: space-between;
        padding: 5px 0px;
        border-bottom: 1px solid #333;
        font-size: 14px;
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
    solo_numbers = re.sub(r'[^0-9.]', '', str(precio).replace(',', '.'))
    try: return float(solo_numbers)
    except: return 0.0

# 3. Carga de datos
try:
    df = pd.read_csv("productos.csv")
except FileNotFoundError:
    st.error("⚠️ No se encontró productos.csv")
    st.stop()

st.title("🛡️ Innovatec J.A")

if 'carrito' not in st.session_state:
    st.session_state.carrito = []

# 4. Interfaz de Selección
producto_sel = st.selectbox("Seleccione producto:", df["Producto"].unique())
datos = df[df["Producto"] == producto_sel].iloc[0]

c1, c2 = st.columns([1, 1])
with c1:
    url = convertir_enlace_drive(datos["Foto"])
    if url: st.image(url, use_container_width=True)
with c2:
    p_unit = limpiar_precio(datos['Precio_Unitario'])
    st.write(f"### S/ {p_unit:,.2f}")
    cant = st.number_input("Cantidad:", min_value=1, value=1)
    if st.button("🛒 Agregar al presupuesto"):
        st.session_state.carrito.append({
            "Producto": producto_sel,
            "Cantidad": cant,
            "Subtotal": cant * p_unit
        })
        st.rerun()

# 5. RESUMEN DEL PRESUPUESTO (Sin botones para evitar desorden)
if st.session_state.carrito:
    st.divider()
    st.header("📋 Detalle del Presupuesto")
    
    # Encabezado simple
    st.markdown("**Producto — Cant. — Total**")
    
    for item in st.session_state.carrito:
        # Formato de línea simple que no se rompe en móvil
        st.markdown(f"✅ {item['Producto']} (x{item['Cantidad']}) — **S/ {item['Subtotal']:,.2f}**")

    total_f = sum(i['Subtotal'] for i in st.session_state.carrito)
    st.subheader(f"Total Final: S/ {total_f:,.2f}")

    # --- NUEVA SECCIÓN: BORRAR PRODUCTOS ---
    st.divider()
    with st.expander("🗑️ Gestionar / Borrar productos"):
        # Creamos una lista de nombres para el multiselect
        opciones_borrar = [f"{i}: {item['Producto']}" for i, item in enumerate(st.session_state.carrito)]
        seleccionados = st.multiselect("Seleccione los productos que desea quitar:", opciones_borrar)
        
        if st.button("Eliminar seleccionados", type="primary"):
            if seleccionados:
                # Extraemos los índices a borrar
                indices_a_borrar = [int(s.split(':')[0]) for s in seleccionados]
                # Creamos nuevo carrito excluyendo esos índices
                st.session_state.carrito = [item for i, item in enumerate(st.session_state.carrito) if i not in indices_a_borrar]
                st.rerun()
            else:
                st.warning("Seleccione al menos un producto para borrar.")
    
    if st.button("Vaciar todo el presupuesto"):
        st.session_state.carrito = []
        st.rerun()
