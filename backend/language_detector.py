import re


def detect_language(code: str) -> str:
    """Detect whether the supplied code is Python or Java."""

    stripped_code = code.strip()

    # Strong Java indicators
    java_patterns = [
        r"\bpublic\s+(static\s+)?[\w<>\[\]]+\s+\w+\s*\(",
        r"\bprivate\s+(static\s+)?[\w<>\[\]]+\s+\w+\s*\(",
        r"\bprotected\s+(static\s+)?[\w<>\[\]]+\s+\w+\s*\(",
        r"\bclass\s+\w+\s*\{",
        r"\bSystem\.out\.println\s*\(",
        r"\bimport\s+java\.",
    ]

    for pattern in java_patterns:
        if re.search(pattern, stripped_code):
            return "java"

    # Strong Python indicators
    python_patterns = [
        r"^\s*def\s+\w+\s*\(",
        r"^\s*async\s+def\s+\w+\s*\(",
        r"^\s*from\s+\w+(\.\w+)*\s+import\s+",
        r"^\s*import\s+\w+",
        r"\bprint\s*\(",
        r":\s*$",
    ]

    for pattern in python_patterns:
        if re.search(pattern, stripped_code, re.MULTILINE):
            return "python"

    # Default to Python for backward compatibility
    return "python"