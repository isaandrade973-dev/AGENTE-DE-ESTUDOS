import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração da página Streamlit
st.set_page_config(
    page_title="Agente de Estudos",
    layout="wide"
)

# Estilização CSS Profissional (Tons Pastéis, Tipografia e Balões Arredondados)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Quicksand:wght@500;600;700&display=swap');

    /* Estilo do Fundo e Tipografia */
    .stApp {
        background-color: #FFFFFF;
        font-family: 'Poppins', sans-serif;
    }

    /* Barra Lateral (Sidebar) */
    section[data-testid="stSidebar"] {
        background-color: #EBF0FF;
        border-right: 2px solid #D8E2FF;
    }
    
    .sidebar-title {
        font-family: 'Quicksand', sans-serif;
        color: #4A5568;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #CBD5E0;
    }

    /* Cabeçalho Principal */
    .main-header {
        background: linear-gradient(135deg, #E2E8F0 0%, #EDF2F7 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        margin-bottom: 1.5rem;
        border: 1px solid #CBD5E0;
    }
    .main-header h1 {
        font-family: 'Quicksand', sans-serif;
        color: #2D3748;
        font-weight: 700;
        font-size: 2rem;
        margin: 0 0 0.5rem 0;
    }
    .main-header p {
        color: #000000;
        font-size: 0.95rem;
        margin: 0;
    }

    /* Estilização das Mensagens de Chat (Balões Arredondados) */
    .stChatMessage[data-testid="stChatMessage"] {
        border-radius: 20px !important;
        padding: 1.2rem 1.5rem !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02) !important;
        font-size: 0.95rem;
    }

    /* Balão da IA (Esquerda / Azul Pastel) */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) {
        background-color: #E8EEFF !important;
        border: 1px solid #D0DDFB !important;
        border-top-left-radius: 4px !important;
    }

    /* Balão do Usuário (Direita / Rosa/Lilás Pastel) */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #000000 !important;
             
        border: 1px solid #FCD6E3 !important;
        border-top-right-radius: 4px !important;
    }

    /* Caixa de Entrada de Texto Arredondada */
    .stChatInputContainer {
        border-radius: 25px !important;
        border: 2px solid #CBD5E0 !important;
        background-color: #000000 !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03) !important;
    }

    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Menu Lateral com Seleção de Matérias
with st.sidebar:
    st.markdown('<div class="sidebar-title">Painel de Estudos</div>', unsafe_allow_html=True)
    materia_selecionada = st.selectbox(
        "Selecione a matéria:",
        [
            "Geral / Todas as Matérias",
            "Matemática",
            "Português e Literatura",
            "História",
            "Geografia",
            "Física",
            "Química",
            "Biologia",
            "Filosofia e Sociologia",
            "Inglês"
        ]
    )
    st.markdown("---")
    st.info(f"Foco selecionado: {materia_selecionada}")

# Cabeçalho Principal
st.markdown(f"""
<div class="main-header">
    <h1>Agente de Estudos</h1>
    <p>Plataforma de Suporte Acadêmico • Foco Atual: <b>{materia_selecionada}</b></p>
</div>
""", unsafe_allow_html=True)

# Captura da API Key de forma segura sem crashar st.secrets
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    st.warning("Aviso: Chave GROQ_API_KEY não encontrada no arquivo .env. Configure para realizar perguntas.")

# Histórico de conversas da sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe histórico de mensagens na interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Caixa de Entrada de Pergunta no Rodapé
if prompt := st.chat_input("Digite sua dúvida acadêmica aqui..."):
    if not api_key:
        st.error("Erro: Adicione sua chave GROQ_API_KEY no arquivo .env para obter respostas.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        client = Groq(api_key=api_key)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                # String do modelo limpa de caracteres especiais ocultos
                MODEL_NAME = "openai/gpt-oss-120b"
                
                completion = client.chat.completions.create(
                    model=MODEL_NAME,
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



# import os
# import streamlit as st
# from groq import Groq
# from dotenv import load_dotenv

# # Carrega variáveis de ambiente
# load_dotenv()

# # Configuração da página Streamlit
# st.set_page_config(page_title="Assistente Groq + Streamlit", page_icon="🤖")
# st.title("🤖 Assistente de IA com Groq")

# # Inicialização do cliente Groq
# api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")

# if not api_key:
#     st.error("Chave da API da Groq não encontrada. Configure no arquivo .env ou nos Secrets do Streamlit.")
#     st.stop()

# client = Groq(api_key=api_key)

# # Histórico de conversas da sessão
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Exibe histórico na interface
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Entrada do usuário
# if prompt := st.chat_input("Como posso ajudar com seus estudos hoje?"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # Resposta do modelo Groq
#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
#         full_response = ""
        
#         try:
#             completion = client.chat.completions.create(
#                 model="openai/gpt-oss-120b",
#                 messages=[
#                     {"role": m["role"], "content": m["content"]}
#                     for m in st.session_state.messages
#                 ],
#                 stream=True,
#             )

#             for chunk in completion:
#                 content = chunk.choices[0].delta.content or ""
#                 full_response += content
#                 message_placeholder.markdown(full_response + "▌")
                
#             message_placeholder.markdown(full_response)
#         except Exception as e:
#             st.error(f"Erro ao consultar a API da Groq: {e}")
            
#     st.session_state.messages.append({"role": "assistant", "content": full_response})
