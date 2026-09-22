import pytest

from src.agent.router import (
    route_question,
    validate_tool,
)


def test_route_calculator():

    assert (
        route_question("Calculate 125 * 48")
        == "calculator"
    )


def test_route_nvd():

    assert (
        route_question("What is CVE-2026-15144?")
        == "nvd_api"
    )


def test_route_policy_rag():

    assert (
        route_question(
            "What does NIST recommend for zero trust?"
        )
        == "policy_rag"
    )


def test_route_case_insensitive_cve():

    assert (
        route_question("Explain cve-2026-15144")
        == "nvd_api"
    )


def test_empty_question_rejected():

    with pytest.raises(ValueError):
        route_question("   ")


def test_non_string_rejected():

    with pytest.raises(TypeError):
        route_question(None)


def test_valid_tool():

    assert validate_tool("calculator") is True
    assert validate_tool("nvd_api") is True
    assert validate_tool("policy_rag") is True


def test_invalid_tool():

    assert validate_tool("unknown_tool") is False
