import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Innovatec: Presupuestos", layout="centered")

# 2. Función para que las fotos de Drive se vean (Limpieza de URL)
def convertir_enlace_drive(url):
    try:
        if "drive.google.com" in str(url):
            # Extrae el ID sin importar si el link termina en /view o ?usp=sharing
            if "/d/" in url:
                id_foto = url.split('/d/')[1].split('/')[0]
            else:
                id_foto = url.split('id=')[1].split('&')[0]
            return f"https://drive.google.com/uc?export=view&id={id_foto}"
        return url
    except:
        return "https://via.placeholder.com/300?text=Error+en+Enlace"

# 3. Cargar los datos desde tu archivo CSV
@st.cache_data
def cargar_datos():
    # El archivo debe llamarse exactamente productos.csv en GitHub
    return pd.read_csv("productos.csv")

try:
    df = cargar_datos()

    st.title("🛡️ Innovatec: Presupuestos")

    # 4. Carrito de compras (Sesión)
    if 'carrito' not in st.session_state:
        st.session_state.carrito = []

    # 5. Interfaz de selección
    producto_sel = st.selectbox("Buscar producto:", df["Producto"].unique())
    datos = df[df["Producto"] == producto_sel].iloc[0]

    col1, col2 = st.columns([1, 1])

    with col1:
        # Aquí aplicamos la conversión de la imagen
        url_limpia = convertir_enlace_drive(datos["Foto"])
        st.image(url_limpia, width=300, use_container_width=True)

    with col2:
        st.write(f"### Precio: S/ {datos['Precio_Unitario']:.2f}")
        st.write(f"**Descripción:** {datos['Descripción']}")
        cantidad = st.number_input("Cantidad:", min_value=1, value=1)
        
        if st.button("🛒 Agregar al presupuesto"):
            item = {
                "Producto": producto_sel,
                "Cantidad": cantidad,
                "Subtotal": cantidad * datos["Precio_Unitario"]
            }
            st.session_state.carrito.append(item)
            st.success("¡Añadido!")

    # 6. Resumen del Presupuesto
    if st.session_state.carrito:
        st.divider()
        st.subheader("Resumen de Cotización")
        resumen_df = pd.DataFrame(st.session_state.carrito)
        st.table(resumen_df)
        
        total = resumen_df["Subtotal"].sum()
        st.header(f"
