import pytest

from src.retrieval.citation import (
    format_citation,
    format_citations,
)


def test_format_citation():

    chunk = {
        "organization": "NIST",
        "version": "SP 800-207",
        "page": 13,
    }

    result = format_citation(chunk)

    assert result == "[NIST | SP 800-207 | p.13]"


def test_multiple_citations():

    chunks = [
        {
            "organization": "NIST",
            "version": "SP 800-207",
            "page": 13,
        },
        {
            "organization": "NIST",
            "version": "SP 800-228 Update 1",
            "page": 40,
        },
    ]

    result = format_citations(chunks)

    assert len(result) == 2

    assert result[0] == (
        "[NIST | SP 800-207 | p.13]"
    )


def test_duplicate_citations_removed():

    chunk = {
        "organization": "NIST",
        "version": "SP 800-207",
        "page": 13,
    }

    result = format_citations([
        chunk,
        chunk,
    ])

    assert result == [
        "[NIST | SP 800-207 | p.13]"
    ]


def test_missing_organization():

    chunk = {
        "version": "SP 800-207",
        "page": 13,
    }

    with pytest.raises(
        ValueError,
        match="organization"
    ):
        format_citation(chunk)


def test_missing_page():

    chunk = {
        "organization": "NIST",
        "version": "SP 800-207",
    }

    with pytest.raises(
        ValueError,
        match="page"
    ):
        format_citation(chunk)
