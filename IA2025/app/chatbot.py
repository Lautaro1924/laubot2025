import streamlit as st
from groq import Groq 

st.set_page_config(page_title="CHATBOT", page_icon="🤖", layout="centered")

st.title("Curso De Programación PYTHON Talento Tech")

nombre = st.text_input("¿Cúal es tu nombre?: ")

if st.button("Saludar"):
    st.write(f"¡Hola {nombre}! Bienvenido/a a mi chatbot.")

modelos = ['llama3-8b-8192', 'llama3-70b-8192', 'gemma2-9b-it']

def configurar_pagina():
    st.title("¿Cuál será tu pregunta?")
    st.sidebar.title("Configurar la IA")
    elegirModelo = st.sidebar.selectbox("Elegi un modelo", options=modelos, index=0)
    return elegirModelo

# Funcion que nos ayuda a conectar con Groq
def crear_usuario_groq():
    claveSecreta = st.secrets["clave_api"]
    return Groq(api_key=claveSecreta)

# Configurar el modelo y el mensaje del usuario. 
def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": mensajeDeEntrada}],
        stream=True
    )

def incializacion_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(role, mensaje, icono):
    st.session_state.mensajes.append({"role": role, "mensaje": mensaje, "icono": icono})

def generar_respuesta(chat_completo):
    respuesta = ""
    for chunk in chat_completo:
        if hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content:
            respuesta += chunk.choices[0].delta.content
            yield chunk.choices[0].delta.content
    return respuesta

modelo = configurar_pagina()
clienteUsuario = crear_usuario_groq()
incializacion_estado()

mensaje = st.chat_input("Escribí tu mensaje")
if mensaje:
    actualizar_historial("user", mensaje, "👦")
    with st.chat_message("user"):
        st.markdown(f" **{mensaje}**")
    chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
    if chat_completo:
        with st.chat_message("assistant"):
            respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
            actualizar_historial("assistant", respuesta_completa, "🤖")