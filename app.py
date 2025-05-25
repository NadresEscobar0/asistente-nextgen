import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página (esto SIEMPRE debe ir primero)
st.set_page_config(page_title="MentorIA - Asistente Académico", page_icon="🧠")

# 2. CSS para panel inferior moderno (no chat)
st.markdown("""
    <style>
    .bottom-panel {
        position: fixed;
        left: 0;
        right: 0;
        bottom: 0;
        background: #f8f9fa;
        padding: 1.2rem 1rem 1rem 1rem;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.07);
        z-index: 100;
        border-top: 2px solid #e3e3e3;
    }
    .bottom-panel textarea {
        width: 100% !important;
        min-height: 70px;
        max-height: 150px;
        resize: vertical;
        font-size: 1.08rem;
    }
    .stButton button {
        width: 100%;
        background: #2b7de9;
        color: white;
        font-weight: bold;
        border-radius: 6px;
        margin-top: 0.5rem;
        font-size: 1.08rem;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Tu API Key de Google Cloud para Gemini
API_KEY = "AIzaSyDDgVzgub-2Va_5xCVcKBU_kYtpqpttyfk"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# 4. Título y bienvenida (nombre creativo)
st.title("MentorIA: Tu Asistente Académico Next-Gen")
st.markdown("""
<div style="text-align: center; margin-bottom: 2.5rem;">
    <b>¡Bienvenido a MentorIA!<br>
    Tu guía personalizada para aprender, razonar y crear.<br>
    Elige tu estilo de aprendizaje y pregunta lo que quieras.<br>
    <span style='color: #2b7de9;'>MentorIA te ayudará a descubrir, no solo a responder.</span></b>
</div>
""", unsafe_allow_html=True)

# 5. Selección de estilo de aprendizaje
estilo = st.selectbox(
    "¿Cuál es tu estilo de aprendizaje preferido?",
    ("Visual", "Auditivo", "Kinestésico")
)

# 6. Mostrar respuestas arriba, caja y botón siempre abajo
if "historial" not in st.session_state:
    st.session_state.historial = []

def construir_prompt(pregunta, estilo):
    base = (
        "Eres un asistente académico ético y creativo. "
        "Primero, responde de forma clara y concreta con los datos más importantes. "
        "Luego, guía al usuario con explicaciones adaptadas a su estilo de aprendizaje."
    )
    if estilo == "Visual":
        detalle = "Usa analogías visuales y ejemplos gráficos."
    elif estilo == "Auditivo":
        detalle = "Usa ejemplos auditivos y relatos."
    else:
        detalle = "Sugiere actividades prácticas y ejemplos kinestésicos."
    return f"{base} {detalle} Pregunta: {pregunta}"

# 7. Mostrar historial de preguntas y respuestas (no chat, solo registro)
st.markdown("### Historial de Interacciones")
for entrada in st.session_state.historial[::-1]:
    st.markdown(f"**Tú:** {entrada['pregunta']}")
    st.markdown(f"**MentorIA:** {entrada['respuesta']}")

# 8. Panel inferior fijo para preguntar
st.markdown('<div class="bottom-panel">', unsafe_allow_html=True)
with st.form(key="formulario_pregunta", clear_on_submit=True):
    pregunta = st.text_area(
        "Haz tu pregunta académica aquí:",
        height=80,
        max_chars=500,
        key="pregunta_usuario"
    )
    enviar = st.form_submit_button("Preguntar")
st.markdown('</div>', unsafe_allow_html=True)

# 9. Procesar la pregunta
if enviar:
    pregunta_baja = pregunta.lower()
    if "historia falsa" in pregunta_baja or "mentir" in pregunta_baja or "cómo hackear" in pregunta_baja:
        respuesta = "Lo siento, no puedo ayudarte con solicitudes poco éticas o que impliquen desinformación."
    else:
        prompt = construir_prompt(pregunta, estilo)
        try:
            respuesta = model.generate_content(prompt)
            respuesta = respuesta.text
        except Exception as e:
            respuesta = f"Error al generar respuesta: {e}"
    st.session_state.historial.append({"pregunta": pregunta, "respuesta": respuesta})

# ¡Listo! No hace falta `st.experimental_rerun()`, el formulario se limpia solo.


























