
import os
import uuid
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# =====================================================
# NEXUS AI — ORANGE BLACK EDITION
# =====================================================

st.set_page_config(
    page_title="NEXUS AI | Orange Black",
    page_icon="🟠",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
API_KEY = os.getenv("GROQ_API_KEY", "").strip()

MODELS = {
    "GPT OSS 20B": "openai/gpt-oss-20b",
    "GPT OSS 120B": "openai/gpt-oss-120b",
    "Llama 3.3 70B": "llama-3.3-70b-versatile",
}

PERSONALITIES = {
    "Natural": "Seja natural, claro e útil.",
    "Amigável": "Seja simpático, acolhedor e descontraído.",
    "Profissional": "Seja profissional, educado e objetivo.",
    "Criativo": "Seja criativo, original e interessante.",
    "Professor": "Explique passo a passo com exemplos simples.",
    "Resumido": "Responda de forma direta e concisa.",
    "Detalhado": "Dê explicações completas e bem organizadas.",
}

# =====================================================
# ESTADO
# =====================================================

def nova_conversa():
    cid = str(uuid.uuid4())
    st.session_state.conversations[cid] = {
        "title": "Nova conversa",
        "messages": [],
        "created": datetime.now().strftime("%d/%m/%Y %H:%M"),
    }
    st.session_state.active = cid


if "conversations" not in st.session_state:
    st.session_state.conversations = {}
    st.session_state.active = None
    st.session_state.personality = "Natural"
    st.session_state.temperature = 0.7

if not st.session_state.conversations:
    nova_conversa()

# =====================================================
# VISUAL PRETO E LARANJA
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
    color-scheme: dark;
    --orange: #ff7900;
    --orange-light: #ffad60;
    --black: #080808;
    --panel: #151515;
    --white: #ffffff;
}

.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, #512000 0%, transparent 38%),
        radial-gradient(ellipse at 90% 90%, #301400 0%, transparent 35%),
        #080808;
    color: #ffffff;
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] {
    background: rgba(8, 8, 8, .94);
}

[data-testid="stSidebar"] {
    background: #101010;
    border-right: 1px solid #693000;
}

[data-testid="stSidebar"] * {
    color: #ffffff;
}

.hero {
    text-align: center;
    padding: 30px 10px;
}

.hero-logo {
    font-size: clamp(38px, 6vw, 66px);
    font-weight: 900;
    letter-spacing: 5px;
    background: linear-gradient(90deg, #ff4500, #ff7900, #ffc078);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
    filter: drop-shadow(0 0 18px #ff790044);
}

.hero-subtitle {
    color: #bbbbbb;
    font-size: 11px;
    letter-spacing: 3px;
}

.hero-line {
    width: 100px;
    height: 2px;
    margin: 18px auto;
    background: #ff7900;
}

/* MENSAGENS */
[data-testid="stChatMessage"] {
    background: #151515;
    border: 1px solid #392012;
    border-radius: 17px;
    padding: 16px;
    margin-bottom: 14px;
}

[data-testid="stChatMessage"] p {
    color: #ffffff;
    line-height: 1.7;
}

/* CAIXA DE DIGITAÇÃO: FUNDO CLARO, LETRAS PRETAS */
[data-testid="stChatInput"],
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] [data-baseweb="textarea"],
[data-testid="stChatInput"] [data-baseweb="base-input"] {
    background: #fff4e8 !important;
    border: 2px solid #ff7900 !important;
    border-radius: 16px !important;
}

[data-testid="stChatInput"] textarea,
.stChatInput textarea {
    background: #fff4e8 !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    caret-color: #ff7900 !important;
    font-size: 16px !important;
    opacity: 1 !important;
}

[data-testid="stChatInput"] textarea::placeholder,
.stChatInput textarea::placeholder {
    color: #555555 !important;
    -webkit-text-fill-color: #555555 !important;
    opacity: 1 !important;
}

[data-testid="stChatInput"]:focus-within {
    border-color: #ffad60 !important;
    box-shadow: 0 0 20px #ff790055 !important;
}

/* BOTÕES: LETRAS PRETAS */
.stButton > button {
    background: linear-gradient(110deg, #ff7900, #ffad60) !important;
    color: #000000 !important;
    border: 1px solid #ffad60 !important;
    border-radius: 12px !important;
    font-weight: 800 !important;
    min-height: 42px;
    transition: .2s ease;
}

.stButton > button *,
.stButton > button p,
.stButton > button span {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

.stButton > button:hover {
    box-shadow: 0 0 20px #ff790066 !important;
    transform: translateY(-2px);
}

/* CAMPOS DE CONFIGURAÇÃO */
[data-baseweb="select"] > div {
    background: #fff4e8 !important;
    border-color: #ff7900 !important;
    color: #000000 !important;
}

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: #fff4e8 !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    caret-color: #ff7900 !important;
    border: 1px solid #ff7900 !important;
    border-radius: 10px !important;
}

[data-testid="stTextInput"] input::placeholder,
[data-testid="stTextArea"] textarea::placeholder {
    color: #555555 !important;
    -webkit-text-fill-color: #555555 !important;
    opacity: 1 !important;
}

hr {
    border-color: #392012;
}

footer {
    visibility: hidden;
}

@media (max-width: 640px) {
    .hero {
        padding: 18px 5px;
    }
    .hero-subtitle {
        letter-spacing: 1px;
    }
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# CLIENTE DA GROQ
# =====================================================

@st.cache_resource
def cliente_groq(chave):
    return Groq(api_key=chave, timeout=60, max_retries=1)


# =====================================================
# BARRA LATERAL
# =====================================================

with st.sidebar:
    st.markdown(
        "<h2 style='color:#ff7900'>🟠 NEXUS AI</h2>",
        unsafe_allow_html=True,
    )
    st.caption("ORANGE BLACK EDITION")
    st.divider()

    if st.button("＋ Nova conversa", use_container_width=True):
        nova_conversa()
        st.rerun()

    st.markdown("### 🗂 Conversas")

    ids = list(st.session_state.conversations.keys())

    active_id = st.session_state.active
    if active_id not in ids:
        active_id = ids[0]
        st.session_state.active = active_id

    escolhido = st.selectbox(
        "Abrir conversa",
        options=ids,
        index=ids.index(active_id),
        format_func=lambda cid: st.session_state.conversations[cid]["title"],
        label_visibility="collapsed",
    )

    if escolhido != st.session_state.active:
        st.session_state.active = escolhido
        st.rerun()

    if st.button("🗑 Excluir conversa", use_container_width=True):
        del st.session_state.conversations[st.session_state.active]
        if not st.session_state.conversations:
            nova_conversa()
        else:
            st.session_state.active = next(
                iter(st.session_state.conversations)
            )
        st.rerun()

    st.divider()
    st.markdown("### 🧠 Modelo")

    modelo_nome = st.selectbox(
        "Escolha o modelo",
        list(MODELS.keys()),
    )

    st.markdown("### 🎭 Personalidade")

    personalidade = st.selectbox(
        "Estilo de resposta",
        list(PERSONALITIES.keys()),
        index=list(PERSONALITIES.keys()).index(
            st.session_state.personality
        ),
    )
    st.session_state.personality = personalidade

    st.markdown("### 🎨 Criatividade")

    st.session_state.temperature = st.slider(
        "Nível criativo",
        min_value=0.0,
        max_value=1.5,
        value=float(st.session_state.temperature),
        step=0.1,
    )

    st.divider()

    if API_KEY:
        st.success("Chave da API configurada")
    else:
        st.error("Chave da API não encontrada")
        st.caption("Confira o arquivo .env.")

    st.caption("NEXUS AI • ORANGE BLACK")

# =====================================================
# CABEÇALHO
# =====================================================

st.markdown("""
<div class="hero">
    <div class="hero-logo">NEXUS AI</div>
    <div class="hero-subtitle">INTELIGÊNCIA · CRIATIVIDADE · POSSIBILIDADES</div>
    <div class="hero-line"></div>
</div>
""", unsafe_allow_html=True)

conversa = st.session_state.conversations[st.session_state.active]

# =====================================================
# SUGESTÕES
# =====================================================

if not conversa["messages"]:
    st.markdown(
        "<h3 style='text-align:center'>O que vamos descobrir hoje?</h3>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p style='text-align:center;color:#bbbbbb'>"
        "Escolha uma sugestão ou escreva sua própria pergunta."
        "</p>",
        unsafe_allow_html=True,
    )

    a, b, c = st.columns(3)

    with a:
        if st.button("🌎 Curiosidades", use_container_width=True):
            st.session_state.sugestao = (
                "Conte cinco curiosidades surpreendentes sobre o mundo."
            )
            st.rerun()

    with b:
        if st.button("🎬 Filmes e séries", use_container_width=True):
            st.session_state.sugestao = (
                "Recomende filmes e séries interessantes para assistir."
            )
            st.rerun()

    with c:
        if st.button("💡 Ideias criativas", use_container_width=True):
            st.session_state.sugestao = (
                "Me dê ideias criativas e diferentes para fazer hoje."
            )
            st.rerun()

    d, e, f = st.columns(3)

    with d:
        if st.button("📚 Aprender algo", use_container_width=True):
            st.session_state.sugestao = (
                "Ensine-me algo interessante com exemplos simples."
            )
            st.rerun()

    with e:
        if st.button("✍️ Criar história", use_container_width=True):
            st.session_state.sugestao = (
                "Crie uma história original, envolvente e surpreendente."
            )
            st.rerun()

    with f:
        if st.button("🎮 Entretenimento", use_container_width=True):
            st.session_state.sugestao = (
                "Sugira jogos e atividades divertidas para meu tempo livre."
            )
            st.rerun()

# =====================================================
# EXIBIR HISTÓRICO
# =====================================================

for mensagem in conversa["messages"]:
    avatar = "👤" if mensagem["role"] == "user" else "🟠"

    with st.chat_message(mensagem["role"], avatar=avatar):
        st.markdown(mensagem["content"])

# =====================================================
# ENTRADA DE MENSAGENS
# =====================================================

pergunta = st.chat_input(
    "Escreva sua mensagem aqui...",
    key="nexus_orange_input",
)

if "sugestao" in st.session_state:
    pergunta = st.session_state.pop("sugestao")

# =====================================================
# RESPOSTA DA INTELIGÊNCIA ARTIFICIAL
# =====================================================

if pergunta and pergunta.strip():
    pergunta = pergunta.strip()

    conversa = st.session_state.conversations[st.session_state.active]

    conversa["messages"].append({
        "role": "user",
        "content": pergunta,
    })

    if conversa["title"] == "Nova conversa":
        conversa["title"] = (
            pergunta[:32] + "..." if len(pergunta) > 32 else pergunta
        )

    with st.chat_message("user", avatar="👤"):
        st.markdown(pergunta)

    if not API_KEY:
        st.error(
            "Não encontrei a chave da Groq. Confira o arquivo .env "
            "na mesma pasta do app.py."
        )
        conversa["messages"].pop()

    else:
        try:
            cliente = cliente_groq(API_KEY)

            mensagens_api = [{
                "role": "system",
                "content": (
                    "Seu nome é NEXUS AI. Responda em português brasileiro "
                    "por padrão. Seja útil, respeitoso e claro. "
                    + PERSONALITIES[personalidade]
                ),
            }]

            mensagens_api.extend(conversa["messages"][-20:])

            with st.chat_message("assistant", avatar="🟠"):
                with st.spinner("🟠 NEXUS está pensando..."):
                    fluxo = cliente.chat.completions.create(
                        model=MODELS[modelo_nome],
                        messages=mensagens_api,
                        temperature=st.session_state.temperature,
                        max_completion_tokens=2048,
                        stream=True,
                    )

                    def gerar_partes():
                        for parte in fluxo:
                            if not parte.choices:
                                continue

                            texto = parte.choices[0].delta.content
                            if texto:
                                yield texto

                    resposta = st.write_stream(gerar_partes())

                if resposta and str(resposta).strip():
                    conversa["messages"].append({
                        "role": "assistant",
                        "content": str(resposta),
                    })
                else:
                    st.warning(
                        "A IA retornou uma resposta vazia. Tente novamente."
                    )

        except Exception as erro:
            st.error("Não foi possível gerar sua resposta.")
            st.markdown("**Detalhes técnicos do erro:**")
            st.code(f"{type(erro).__name__}: {str(erro)[:2000]}")

            detalhes = str(erro)

            if "401" in detalhes:
                st.warning("Confira se sua chave da API está correta.")
            elif "429" in detalhes:
                st.warning("Limite da API atingido. Tente novamente mais tarde.")
            elif "model" in detalhes.lower():
                st.warning("Tente selecionar outro modelo na barra lateral.")

            if (
                conversa["messages"]
                and conversa["messages"][-1]["role"] == "user"
                and conversa["messages"][-1]["content"] == pergunta
            ):
                conversa["messages"].pop()

# =====================================================
# RODAPÉ
# =====================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        color:#999999;
        font-size:11px;
        padding:8px 0 20px;
    ">
        NEXUS AI · ORANGE BLACK EDITION
        <br>
        Conversas, ideias e descobertas.
    </div>
    """,
    unsafe_allow_html=True,
)
