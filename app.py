import streamlit as st
import google.generativeai as genai

# Tu API Key de Google Cloud para Gemini
API_KEY = "AIzaSyDDgVzgub-2Va_5xCVcKBU_kYtpqpttyfk"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("Asistente Inteligente Next-Gen")

estilo = st.selectbox(
    "¿Cuál es tu estilo de aprendizaje preferido?",
    ("Visual", "Auditivo", "Kinestésico")
)

pregunta = st.text_input("Escribe tu pregunta:")

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

if st.button("Preguntar"):
    if not pregunta.strip():
        st.warning("Por favor, escribe una pregunta.")
    else:
        prompt = construir_prompt(pregunta, estilo)
        try:
            respuesta = model.generate_content(prompt)
            st.write("Respuesta IA:", respuesta.text)
        except Exception as e:
            st.error(f"Error al generar respuesta: {e}")



















