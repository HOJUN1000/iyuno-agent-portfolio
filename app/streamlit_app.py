import sys
from pathlib import Path

import streamlit as st
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
)


# --------------------------------------------------
# Project Path
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT)
    )


from src.agent.security_agent import SecurityAgent
from src.retrieval.retriever import Retriever


MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"


# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Agentic Knowledge Triage",
    page_icon="🛡️",
    layout="wide",
)


# --------------------------------------------------
# Resource Loading
# --------------------------------------------------

@st.cache_resource
def load_agent():

    # Retriever
    retriever = Retriever(
        device="cpu"
    )

    # Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    # GPU 사용 가능 시 GPU 사용
    if torch.cuda.is_available():

        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            torch_dtype=torch.float16,
            device_map="auto",
        )

        model_mode = "GPU"

    else:

        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            torch_dtype=torch.float32,
        )

        model_mode = "CPU"

    model.eval()

    agent = SecurityAgent(
        retriever=retriever,
        tokenizer=tokenizer,
        model=model,
        top_k=5,
    )

    return agent, model_mode


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title(
    "🛡️ Agentic Knowledge Triage"
)

st.caption(
    "Security AI Agent powered by RAG, "
    "tool calling, NIST NVD API, and Qwen."
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header(
        "System"
    )

    st.write(
        "**LLM:** Qwen2.5-1.5B-Instruct"
    )

    st.write(
        "**Retriever:** FAISS + MiniLM"
    )

    st.write(
        "**Knowledge Base:** 20 public security documents"
    )

    st.write(
        "**Tools:** Calculator / NVD API / Policy RAG"
    )

    st.divider()

    st.write(
        "**Evaluation**"
    )

    st.write(
        "Recall@5: 100%"
    )

    st.write(
        "Tool Selection: 100%"
    )

    st.write(
        "Citation Success: 100%"
    )

    st.write(
        "Faithfulness Proxy: 78.1%"
    )


# --------------------------------------------------
# Agent Loading
# --------------------------------------------------

with st.spinner(
    "Loading AI Agent..."
):

    try:

        agent, model_mode = load_agent()

        st.success(
            f"Agent ready ({model_mode})"
        )

    except Exception as e:

        st.error(
            "Failed to load the AI Agent."
        )

        st.exception(e)

        st.stop()


# --------------------------------------------------
# Example Questions
# --------------------------------------------------

st.subheader(
    "Example Questions"
)

st.code(
    """Calculate 125 * 48

What is CVE-2026-15144?

What does NIST recommend for zero trust access control?

How can prompt injection attacks against generative AI systems be mitigated?"""
)


# --------------------------------------------------
# User Input
# --------------------------------------------------

question = st.text_area(
    "Ask the security agent",
    placeholder=(
        "Enter a calculation, CVE question, "
        "or security policy question..."
    ),
    height=100,
)


ask_button = st.button(
    "Ask Agent",
    type="primary",
    use_container_width=True,
)


# --------------------------------------------------
# Agent Execution
# --------------------------------------------------

if ask_button:

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Agent is reasoning..."
        ):

            try:

                result = agent.ask(
                    question
                )

            except Exception as e:

                st.error(
                    "Agent execution failed."
                )

                st.exception(e)

                st.stop()


        # ------------------------------------------
        # Result Status
        # ------------------------------------------

        if result.get(
            "success"
        ):

            st.success(
                "Request completed"
            )

        else:

            st.error(
                "Request failed"
            )


        # ------------------------------------------
        # Execution Information
        # ------------------------------------------

        col1, col2, col3 = st.columns(
            3
        )

        with col1:

            st.metric(
                "Route",
                result.get(
                    "route",
                    "-"
                )
            )

        with col2:

            st.metric(
                "Tool",
                result.get(
                    "tool",
                    "-"
                )
            )

        with col3:

            latency = result.get(
                "latency_seconds",
                0
            )

            st.metric(
                "Latency",
                f"{latency:.2f}s"
            )


        # ------------------------------------------
        # Answer
        # ------------------------------------------

        st.subheader(
            "Answer"
        )

        answer = result.get(
            "answer"
        )

        if answer:

            st.write(
                answer
            )

        else:

            st.warning(
                result.get(
                    "error",
                    "No answer generated."
                )
            )


        # ------------------------------------------
        # Sources
        # ------------------------------------------

        sources = result.get(
            "sources",
            []
        )

        if sources:

            st.subheader(
                "Sources"
            )

            for source in sources:

                st.write(
                    f"- {source}"
                )


        # ------------------------------------------
        # Raw Execution Details
        # ------------------------------------------

        with st.expander(
            "Execution Details"
        ):

            st.json(
                result
            )


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    "Iyuno AI Agent Engineer Portfolio Project | "
    "RAG + Tool Calling + Evaluation"
)
