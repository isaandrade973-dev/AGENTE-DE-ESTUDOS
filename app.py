import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração da página Streamlit
st.set_page_config(page_title="Assistente Groq + Streamlit", page_icon="🤖")
st.title("🤖 Assistente de IA com Groq")

# Inicialização do cliente Groq
api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")

if not api_key:
    st.error("Chave da API da Groq não encontrada. Configure no arquivo .env ou nos Secrets do Streamlit.")
    st.stop()

client = Groq(api_key=api_key)

# Histórico de conversas da sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe histórico na interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada do usuário
if prompt := st.chat_input("Como posso ajudar com seus estudos hoje?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Resposta do modelo Groq
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            completion = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )

            for chunk in completion:
                content = chunk.choices[0].delta.content or ""
                full_response += content
                message_placeholder.markdown(full_response + "▌")
                
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Erro ao consultar a API da Groq: {e}")
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})