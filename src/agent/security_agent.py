import re
import time

from src.agent.router import route_question
from src.agent.generator import QwenGenerator
from src.tools.calculator import calculator_tool
from src.tools.nvd import extract_cve_id, nvd_cve_tool
from src.retrieval.citation import format_citations


class SecurityAgent:
    """
    Unified security knowledge agent.

    Routes user requests to:
    - Calculator
    - NIST NVD CVE API
    - RAG retrieval + Qwen generation
    """

    def __init__(
        self,
        retriever,
        tokenizer,
        model,
        top_k=5,
    ):
        if retriever is None:
            raise ValueError(
                "retriever cannot be None."
            )

        self.retriever = retriever

        self.generator = QwenGenerator(
            tokenizer=tokenizer,
            model=model,
        )

        self.top_k = top_k


    def _extract_expression(self, question):
        """Extract arithmetic expression from a calculation request."""

        expression = re.sub(
            r"^\s*(calculate|compute)\s*",
            "",
            question,
            flags=re.IGNORECASE,
        ).strip()

        return expression


    def _build_context(self, results):
        """Build grounded context from retrieved chunks."""

        context_parts = []

        for result in results:

            citation = (
                f"[{result['organization']} | "
                f"{result['version']} | "
                f"p.{result['page']}]"
            )

            context_parts.append(
                f"{citation}\n"
                f"{result['text']}"
            )

        return "\n\n".join(
            context_parts
        )


    def ask(self, question):
        """Route and execute one user request."""

        if not isinstance(question, str):
            raise TypeError(
                "Question must be a string."
            )

        question = question.strip()

        if not question:
            raise ValueError(
                "Question cannot be empty."
            )

        started_at = time.perf_counter()

        route = route_question(
            question
        )


        # ==================================
        # Calculator
        # ==================================

        if route == "calculator":

            expression = self._extract_expression(
                question
            )

            tool_result = calculator_tool(
                expression
            )

            latency = (
                time.perf_counter()
                - started_at
            )

            if not tool_result["success"]:

                return {
                    "success": False,
                    "route": route,
                    "tool": "calculator_tool",
                    "answer": None,
                    "sources": [],
                    "latency_seconds": latency,
                    "error": tool_result.get(
                        "error"
                    ),
                }

            return {
                "success": True,
                "route": route,
                "tool": "calculator_tool",
                "answer": str(
                    tool_result["result"]
                ),
                "sources": [],
                "latency_seconds": latency,
            }


        # ==================================
        # NVD API
        # ==================================

        if route == "nvd_api":

            cve_id = extract_cve_id(
                question
            )

            tool_result = nvd_cve_tool(
                cve_id
            )

            latency = (
                time.perf_counter()
                - started_at
            )

            if not tool_result["success"]:

                return {
                    "success": False,
                    "route": route,
                    "tool": "nvd_cve_tool",
                    "answer": None,
                    "sources": [],
                    "latency_seconds": latency,
                    "error": tool_result.get(
                        "error"
                    ),
                }

            answer = (
                f"{tool_result['cve_id']}: "
                f"{tool_result.get('description', '')}"
            )

            return {
                "success": True,
                "route": route,
                "tool": "nvd_cve_tool",
                "answer": answer,
                "sources": [
                    "NIST National Vulnerability Database"
                ],
                "latency_seconds": latency,
                "metadata": {
                    "published":
                        tool_result.get(
                            "published"
                        ),
                    "last_modified":
                        tool_result.get(
                            "last_modified"
                        ),
                },
            }


        # ==================================
        # Policy RAG
        # ==================================

        results = self.retriever.retrieve(
            question,
            top_k=self.top_k,
        )

        if not results:

            latency = (
                time.perf_counter()
                - started_at
            )

            return {
                "success": False,
                "route": "policy_rag",
                "tool": "retriever",
                "answer": None,
                "sources": [],
                "latency_seconds": latency,
                "error": "No retrieval results.",
            }


        context = self._build_context(
            results
        )

        answer = self.generator.generate(
            question=question,
            context=context,
        )

        sources = format_citations(
            results
        )

        latency = (
            time.perf_counter()
            - started_at
        )

        return {
            "success": True,
            "route": "policy_rag",
            "tool": "retriever + qwen",
            "answer": answer,
            "sources": sources,
            "latency_seconds": latency,
            "retrieval_count": len(
                results
            ),
        }
