"""Conservative metadata filter inference from explicit query scope only."""
import re


def infer_filter(query: str) -> dict[str, str] | None:
    """Infer a `part` filter only when the user explicitly names a section.

    Content keywords such as "deployment", "fairness", or "accuracy" are not
    used because mapping them to a section could encode benchmark gold.
    """
    text = re.sub(r"\s+", " ", query.casefold())
    if re.search(r"\bappendix\b", text):
        return {"part": "appendix"}
    match = re.search(r"\bpart\s*([12])\b", text)
    if match:
        return {"part": f"part{match.group(1)}"}
    return None
