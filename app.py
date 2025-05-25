import streamlit as st
import google.generativeai as genai

# ¡ESTA LÍNEA DEBE IR PRIMERO!
st.set_page_config(page_title="Asistente Virtual", page_icon="🤖")

# --- CSS para fijar la caja y el botón al fondo ---
st.markdown("""
    <style>
    .fixed-bottom-container {
        position: fixed;
        left: 0;
        right: 0;
        bottom: 0;
        background: #fafafa;
        padding: 1rem 1rem 0.5rem 1rem;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
        z-index: 100;
    }
    .fixed-bottom-container textarea {
        width: 100% !important;
        min-height: 50px;
        max-height: 120px;
        resize: vertical;
    }
    </style>
""", unsafe_allow_html=True)

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

# Contenedor fijo al fondo de la pantalla
st.markdown('<div class="fixed-bottom-container">', unsafe_allow_html=True)
pregunta = st.text_area(
    "Escribe tu pregunta aquí:",
    height=60,
    max_chars=500,
    key="pregunta_usuario"
)
enviar = st.button("Preguntar")
st.markdown('</div>', unsafe_allow_html=True)

# Lógica para procesar la pregunta
if enviar:
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






















