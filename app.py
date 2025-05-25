import streamlit as st
import google.generativeai as genai

# Configuración de la página
st.set_page_config(page_title="Asistente Virtual", page_icon="🤖")

# Tu API Key de Google Cloud para Gemini
API_KEY = "AIzaSyDDgVzgub-2Va_5xCVcKBU_kYtpqpttyfk"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Título y bienvenida (esto lo cambiaremos por el nombre original en el siguiente paso)
st.title("Asistente Virtual Inteligente")  # Cambiaremos el nombre después

st.markdown("""
<div style="text-align: center;">
    <b>¡Hola! Soy tu asistente virtual académico.<br>
    Pregúntame lo que quieras y te guiaré paso a paso.</b>
</div>
""", unsafe_allow_html=True)

# Selección de estilo de aprendizaje
estilo = st.selectbox(
    "¿Cuál es tu estilo de aprendizaje preferido?",
    ("Visual", "Auditivo", "Kinestésico")
)

# Caja de texto expandible (como WhatsApp)
pregunta = st.text_area(
    "Escribe tu pregunta aquí:",
    height=80,
    max_chars=500,
    key="pregunta_usuario"
)

def construir_prompt(pregunta, estilo):
    base = (
        "Primero, responde de forma clara y concreta con los datos más importantes. "
        "Luego, añade una explicación creativa y adaptada al estilo de aprendizaje."
    )
    if estilo == "Visual":
        detalle = "Usa analogías visuales y ejemplos gráficos."
    elif estilo == "Auditivo":
        detalle = "Usa ejemplos auditivos y relatos."
    else:
        detalle = "Sugiere actividades prácticas y ejemplos kinestésicos."
    return f"{base} {detalle} Pregunta: {pregunta}"

# Botón único de preguntar
if st.button("Preguntar"):
    if not pregunta.strip():
        st.warning("Por favor, escribe una pregunta.")
    else:
        prompt = construir_prompt(pregunta, estilo)
        try:
            respuesta = model.generate_content(prompt)
            st.write("**Respuesta del Asistente:**")
            st.write(respuesta.text)
        except Exception as e:
            st.error(f"Error al generar respuesta: {e}")




















