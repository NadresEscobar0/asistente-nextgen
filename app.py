import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página
st.set_page_config(page_title="VictorIA Next - Asistente Académico", page_icon="🧠")

# 2. CSS para panel inferior moderno
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

# 3. API Key de Google Cloud para Gemini
API_KEY = "AIzaSyDDgVzgub-2Va_5xCVcKBU_kYtpqpttyfk"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# 4. Título y bienvenida
st.title("VictoRIA Next: Tu Asistente Académico Next-Gen")
st.markdown("""
<div style="text-align: center; margin-bottom: 2.5rem;">
    <b>¡Bienvenido a <span style='color: #2b7de9;'>VictoRIA Next</span>!<br>
    Tu guía personalizada para aprender, razonar y crear.<br>
    Elige tu estilo de aprendizaje y pregunta lo que quieras.<br>
    <span style='color: #2b7de9;'>VictoRIA Next te ayudará a descubrir, no solo a responder.</span></b>
</div>
""", unsafe_allow_html=True)

# 5. Selección de estilo de aprendizaje
estilo = st.selectbox(
    "¿Cuál es tu estilo de aprendizaje preferido?",
    ("Visual", "Auditivo", "Kinestésico")
)

# 6. Inicializar historial en sesión
if "historial" not in st.session_state:
    st.session_state.historial = []

# 7. Función para construir el prompt adaptado
def construir_prompt(pregunta, estilo):
    base = (
        "Eres VictoRIA Next, una asistente académica ética, creativa y adaptativa. "
        "Responde la siguiente pregunta de forma clara, concreta y adaptada exclusivamente al estilo de aprendizaje indicado."
    )
    if estilo == "Visual":
        detalle = "Utiliza analogías visuales, descripciones gráficas, diagramas mentales o ejemplos visuales. No expliques otros estilos."
    elif estilo == "Auditivo":
        detalle = "Utiliza ejemplos auditivos, relatos, metáforas sonoras o explicaciones habladas. No expliques otros estilos."
    else:
        detalle = "Sugiere actividades prácticas, ejemplos kinestésicos y pasos que impliquen acción física. No expliques otros estilos."
    return f"{base} Estilo de aprendizaje: {estilo}. {detalle} Pregunta: {pregunta}"

# 8. Mostrar historial organizado y visualmente limpio, con alto contraste
if st.session_state.historial:
    st.markdown("### Historial de Interacciones")
    for i, entrada in enumerate(st.session_state.historial[::-1], 1):
        st.markdown(f"""
        <div style="
            background-color:#1b4a7a;
            border-radius:10px;
            padding:1em;
            margin-bottom:0.5em;
            color:#ffffff;
            ">
            <b><span style="color:#FFD700;">{i}. Tú:</span></b> {entrada['pregunta']}<br>
            <b><span style="color:#87CEEB;">VictoRIA Next:</span></b> {entrada['respuesta']}
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("¡Haz tu primera pregunta académica abajo para comenzar!")

# 9. Panel inferior fijo para preguntar
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

# 10. Procesar la pregunta y mostrar la respuesta inmediatamente
if enviar and pregunta.strip():
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
    # Mostrar la respuesta inmediatamente arriba del formulario
    st.markdown(f"""
    <div style="
        background-color:#1b4a7a;
        border-radius:10px;
        padding:1em;
        margin-bottom:0.5em;
        color:#ffffff;">
        <b><span style="color:#FFD700;">Tú:</span></b> {pregunta}<br>
        <b><span style="color:#87CEEB;">VictoRIA Next:</span></b> {respuesta}
    </div>
    """, unsafe_allow_html=True)
elif enviar:
    st.warning("Por favor, escribe una pregunta antes de continuar.")

# ¡Listo! Nombre original, historial visual, respuesta inmediata y adaptación real al estilo de aprendizaje.




























