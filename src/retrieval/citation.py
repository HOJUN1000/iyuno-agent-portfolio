def format_citation(chunk):
    """Create a standardized citation from a retrieved chunk."""

    required_fields = [
        "organization",
        "version",
        "page",
    ]

    for field in required_fields:
        if field not in chunk:
            raise ValueError(
                f"Missing citation field: {field}"
            )

    return (
        f"[{chunk['organization']} | "
        f"{chunk['version']} | "
        f"p.{chunk['page']}]"
    )


def format_citations(chunks):
    """Create citations and remove duplicates while preserving order."""

    citations = []

    for chunk in chunks:

        citation = format_citation(chunk)

        if citation not in citations:
            citations.append(citation)

    return citations
