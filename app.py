import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página
st.set_page_config(page_title="VictorIA Nexus - Asistente Académico Adaptativo", page_icon="🧠")

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

# 4. Título y bienvenida profesional
st.title("VictorIA Nexus: Asistente Académico Adaptativo")

st.markdown("""
<div style="text-align: center; margin-bottom: 2.5rem;">
    <b>
    <span style='font-size:1.3em; color:#2b7de9;'>¡Bienvenido a VictorIA Nexus!</span><br><br>
    Mucho más que un asistente: VictorIA Nexus es el puente entre tu curiosidad y el conocimiento.<br><br>
    Esta plataforma de inteligencia artificial adaptativa no solo responde preguntas, sino que te guía en la exploración creativa de soluciones, personalizando cada interacción según tu estilo de aprendizaje.<br><br>
    Inspirada en el poder de la tecnología y la pedagogía, VictorIA Nexus fomenta el razonamiento crítico, la autonomía y la innovación académica. Aquí, cada consulta es una oportunidad para descubrir, reflexionar y crecer.<br><br>
    <span style='color: #2b7de9;'>Elige tu estilo de aprendizaje, plantea tu reto académico y deja que VictorIA Nexus te acompañe en el viaje de transformar dudas en descubrimientos.</span>
    </b>
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

# 7. Prompt profesional y adaptativo
def construir_prompt(pregunta, estilo):
    base = (
        "Eres VictorIA Nexus, una asistente académica ética, creativa y adaptativa. "
        "Prioriza siempre responder de forma clara y concreta a la pregunta planteada. "
        "Después de la respuesta, añade una explicación creativa adaptada únicamente al estilo de aprendizaje indicado."
    )
    if estilo == "Visual":
        detalle = "Después de la respuesta, utiliza analogías visuales, descripciones gráficas, esquemas mentales o ejemplos visuales. No expliques otros estilos."
    elif estilo == "Auditivo":
        detalle = "Después de la respuesta, utiliza ejemplos auditivos, relatos, metáforas sonoras o explicaciones habladas. No expliques otros estilos."
    else:
        detalle = "Después de la respuesta, sugiere actividades prácticas, ejemplos kinestésicos y pasos que impliquen acción física. No expliques otros estilos."
    return f"{base} Estilo de aprendizaje: {estilo}. {detalle} Pregunta: {pregunta}"

# 8. Historial visual profesional y contrastante
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
            <b><span style="color:#87CEEB;">VictorIA Nexus:</span></b> {entrada['respuesta']}
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
        <b><span style="color:#87CEEB;">VictorIA Nexus:</span></b> {respuesta}
    </div>
    """, unsafe_allow_html=True)
elif enviar:
    st.warning("Por favor, escribe una pregunta antes de continuar.")

# ¡Listo! Nombre original, bienvenida profesional, historial visual, respuesta inmediata y adaptación real al estilo de aprendizaje.





























