import streamlit as st
import google.generativeai as genai
import re
import requests
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="VictorIA Nexus - Asistente Académico Adaptativo", page_icon="🧠")

# API Key y modelo
API_KEY = "AIzaSyDDgVzgub-2Va_5xCVcKBU_kYtpqpttyfk"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Título con emojis
st.title("VictorIA Nexus 🧠💪✝️")
st.markdown("""
<div style="text-align: center; margin-bottom: 2.5rem;">
    <b>
    <span style='font-size:1.3em; color:#2b7de9;'>¡Bienvenido a VictorIA Nexus!</span><br><br>
    Mucho más que un asistente: VictorIA Nexus es el puente entre tu curiosidad y el conocimiento.<br><br>
    Esta plataforma de inteligencia artificial adaptativa no solo responde preguntas, sino que guía, inspira y personaliza cada interacción según tu estilo de aprendizaje.<br><br>
    Inspirada en la pedagogía y la tecnología, VictorIA Nexus fomenta el pensamiento crítico, la creatividad y la autonomía. Aquí, cada consulta es una oportunidad para descubrir, reflexionar y crecer.<br><br>
    <span style='color: #2b7de9;'>Elige tu estilo de aprendizaje, plantea tu reto académico y deja que VictorIA Nexus te acompañe en el viaje de transformar dudas en descubrimientos. No solo obtendrás respuestas, sino caminos para aprender y crear.</span>
    </b>
</div>
""", unsafe_allow_html=True)

# --- Generador de imágenes IA ---
st.header("Generador de Imágenes por IA (Gratis)")
prompt_img = st.text_input("Describe la imagen educativa que quieres generar:")

if st.button("Generar imagen IA"):
    if prompt_img.strip():
        with st.spinner("Generando imagen..."):
            url = "https://api.kieai.tech/v1/generate"
            payload = {"prompt": prompt_img}
            try:
                response = requests.post(url, json=payload, timeout=60)
                response.raise_for_status()
                img_url = response.json().get("image_url")
                if img_url:
                    img_data = requests.get(img_url).content
                    image = Image.open(BytesIO(img_data))
                    st.image(image, caption="Imagen generada por IA", use_column_width=True)
                else:
                    st.warning("No se pudo generar la imagen. Intenta con otra descripción.")
            except Exception as e:
                st.error(f"Error al generar imagen: {e}")
    else:
        st.warning("Por favor, escribe una descripción para la imagen.")

# --- Selección de estilo de aprendizaje ---
estilo = st.selectbox(
    "¿Cuál es tu estilo de aprendizaje preferido?",
    ("Visual", "Auditivo", "Kinestésico")
)

if "historial" not in st.session_state:
    st.session_state.historial = []

def construir_prompt(pregunta, estilo):
    pregunta_baja = pregunta.lower()
    if (
        "quién te desarrolló" in pregunta_baja
        or "quien te desarrolló" in pregunta_baja
        or "quién es tu creador" in pregunta_baja
        or "quien es tu creador" in pregunta_baja
        or "autor" in pregunta_baja
        or "quién lo hizo" in pregunta_baja
        or "quien lo hizo" in pregunta_baja
        or "desarrollador" in pregunta_baja
        or "creador" in pregunta_baja
    ):
        return "Por favor, responde únicamente: 'Fui desarrollado por Pedro Tovar.'"
    base = (
        "Eres VictorIA Nexus, una asistente académica ética, creativa y adaptativa. "
        "Prioriza siempre responder de forma clara, extensa y concreta a la pregunta planteada, "
        "proporcionando una explicación detallada, profunda y bien desarrollada, con ejemplos y contexto para que cualquier estudiante pueda comprender a fondo el tema. "
        "No seas breve ni superficial. "
        "Después de la respuesta, añade una explicación creativa, extensa y adaptada únicamente al estilo de aprendizaje indicado, "
        "con el objetivo de fomentar el aprendizaje real, la creatividad y el pensamiento crítico. "
        "Desarrolla la explicación y utiliza recursos propios del estilo elegido. "
        "Nunca menciones que eres de Google, Gemini, Streamlit, ni ningún proveedor externo. "
        "Si te preguntan por tu creador, responde únicamente: 'Fui desarrollado por Pedro Tovar.'"
    )
    if estilo == "Visual":
        detalle = "Después de la respuesta, utiliza analogías visuales, descripciones gráficas, esquemas mentales, mapas conceptuales o ejemplos visuales. No expliques otros estilos."
    elif estilo == "Auditivo":
        detalle = "Después de la respuesta, utiliza ejemplos auditivos, relatos, metáforas sonoras, explicaciones habladas o historias narradas. No expliques otros estilos."
    else:
        detalle = "Después de la respuesta, sugiere actividades prácticas, ejemplos kinestésicos, ejercicios paso a paso y propuestas que impliquen acción física. No expliques otros estilos."
    return f"{base} Estilo de aprendizaje: {estilo}. {detalle} Pregunta: {pregunta}"

def limpiar_html(texto):
    texto_limpio = re.sub(r'</?div[^>]*>', '', texto)
    return texto_limpio.strip()

# Historial y flujo de chat
if st.session_state.historial:
    st.markdown("### Historial de Interacciones")
    for i, entrada in enumerate(st.session_state.historial[::-1], 1):
        respuesta_limpia = limpiar_html(entrada['respuesta'])
        st.markdown(f"""
        <div style="
            background-color:#1b4a7a;
            border-radius:10px;
            padding:1em;
            margin-bottom:0.5em;
            color:#ffffff;">
            <b><span style="color:#FFD700;">{i}. Tú:</span></b> {entrada['pregunta']}<br>
            <b><span style="color:#87CEEB;">VictorIA Nexus:</span></b> {respuesta_limpia}
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("¡Haz tu primera pregunta académica abajo para comenzar!")

# Chat input estándar y seguro
pregunta = st.text_input("Haz tu pregunta académica aquí...", max_chars=500)
if st.button("Preguntar"):
    if pregunta.strip():
        pregunta_baja = pregunta.lower()
        # Respuesta de autoría directa
        if (
            "quién te desarrolló" in pregunta_baja
            or "quien te desarrolló" in pregunta_baja
            or "quién es tu creador" in pregunta_baja
            or "quien es tu creador" in pregunta_baja
            or "autor" in pregunta_baja
            or "quién lo hizo" in pregunta_baja
            or "quien lo hizo" in pregunta_baja
            or "desarrollador" in pregunta_baja
            or "creador" in pregunta_baja
        ):
            respuesta = "Fui desarrollado por Pedro Tovar."
            respuesta_limpia = respuesta
        else:
            prompt = construir_prompt(pregunta, estilo)
            try:
                respuesta = model.generate_content(prompt)
                respuesta = respuesta.text
            except Exception as e:
                respuesta = f"Error al generar respuesta: {e}"
            respuesta_limpia = limpiar_html(respuesta)
        st.session_state.historial.append({"pregunta": pregunta, "respuesta": respuesta_limpia})
        st.markdown(f"""
        <div style="
            background-color:#1b4a7a;
            border-radius:10px;
            padding:1em;
            margin-bottom:0.5em;
            color:#ffffff;">
            <b><span style="color:#FFD700;">Tú:</span></b> {pregunta}<br>
            <b><span style="color:#87CEEB;">VictorIA Nexus:</span></b> {respuesta_limpia}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Por favor, escribe una pregunta antes de continuar.")

# --- FIRMA LEGAL ---
st.markdown("""
---
**© 2025 Pedro Tovar. Todos los derechos reservados.**  
Esta aplicación fue desarrollada por Pedro Tovar para fines académicos. Prohibida su reproducción total o parcial sin autorización.
""")
