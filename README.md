# AGENTE-DE-ESTUDOS
# 📚 Agente de Estudos — Plataforma Acadêmica com IA

Assistente acadêmico virtual desenvolvido em Python e Streamlit, integrado à API da Groq (`llama-3.1-8b-instant`) com interface em tons de azul.

---

## 📁 1. Organização das Pastas e Arquivos Principais

agente-de-estudos/
├── .env                  # Chave privada da API Groq (GROQ_API_KEY)
├── .gitignore            # Arquivos ignorados pelo controle de versão
├── app.py                # Código-fonte principal (Interface e Integração)
├── prompt.md             # Engenharia de Prompt (System Prompt do Agente)
├── README.md             # Documentação oficial do repositório
└── requirements.txt      # Dependências da aplicação (streamlit, groq, etc.)

---

## 📜 2. Engenharia de Prompt (`prompt.md`)

"Você é um Tutor Acadêmico Especialista de Alta Performance. Sua missão é fornecer explicações claras, objetivas e pedagogicamente estruturadas sobre qualquer disciplina escolar ou universitária.

Diretrizes de Resposta:
1. Tom de Voz: Profissional, claro e estritamente acadêmico.
2. Formatação: Resumos explicativos e tabelas Markdown comparativas.
3. Contexto: Adapte a linguagem conforme a matéria selecionada no painel lateral."

---

## 💻 3. Código Principal (`app.py`)

import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="Agente de Estudos", layout="wide")

# Inicialização da API e Cliente Groq
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Captura de entrada do usuário e requisição em Streaming
if prompt := st.chat_input("Digite sua dúvida acadêmica..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        stream=True,
    )

---

## 🚀 4. Como Executar o Projeto

1. Clonar o repositório:
   git clone https://github.com/usuario/agente-de-estudos.git

2. Instalar as dependências:
   pip install -r requirements.txt

3. Configurar a chave no arquivo .env:
   GROQ_API_KEY=sua_chave_aqui

4. Executar a aplicação:
   python -m streamlit run app.py
