import re


VALID_TOOLS = {
    "calculator",
    "nvd_api",
    "policy_rag",
}


def route_question(question):
    """
    Lightweight deterministic routing layer.

    The production agent may use an LLM selector,
    while this function provides predictable routing
    and fallback behavior for common request types.
    """

    if not isinstance(question, str):
        raise TypeError("Question must be a string.")

    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty.")

    lower_question = question.lower()


    # CVE identifier → NVD API
    if re.search(
        r"\bCVE-\d{4}-\d{4,}\b",
        question,
        flags=re.IGNORECASE,
    ):
        return "nvd_api"


    # Explicit calculation request → Calculator
    if (
        lower_question.startswith("calculate ")
        or lower_question.startswith("compute ")
    ):
        return "calculator"


    # General security / policy questions → RAG
    return "policy_rag"


def validate_tool(tool_name):
    """Check whether a selected tool is supported."""

    return tool_name in VALID_TOOLS
