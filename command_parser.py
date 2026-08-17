import re


KNOWN_VERSIONS = {
    "ASV",
    "HCSB",
    "RVA",
    "KJV",
    "NKJV",
    "NIV",
    "NLT",
    "MSG",
    "AMP",
    "ESV",
    "RSV",
    "GNB",
}


COMMAND_PREFIXES = [
    r"let's\s+read\s+",
    r"lets\s+read\s+",
    r"show\s+",
    r"display\s+",
    r"put\s+",
    r"read\s+",
    r"bring\s+up\s+",
    r"go\s+to\s+",
    r"give\s+me\s+",
    r"open\s+",
]


VERSION_ALIASES = {
    "KING JAMES VERSION": "KJV",
    "KING JAMES": "KJV",
    "NEW KING JAMES VERSION": "NKJV",
    "NEW KING JAMES": "NKJV",
    "NEW LIVING TRANSLATION": "NLT",
    "HOLMAN CHRISTIAN STANDARD": "HCSB",
    "HOLMAN": "HCSB",
}


def clean_command(text):
    text = text.strip()

    # Remove common command prefixes.
    for pattern in COMMAND_PREFIXES:
        text = re.sub(
            rf"^\s*{pattern}",
            "",
            text,
            flags=re.IGNORECASE,
        )

    return text.strip()


def extract_version(text):
    upper = text.upper()

    # Long phrases first.
    for phrase, version in sorted(
        VERSION_ALIASES.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    ):
        if phrase in upper:
            return version

    # Exact version codes.
    for version in sorted(
        KNOWN_VERSIONS,
        key=len,
        reverse=True,
    ):
        if re.search(
            rf"\b{re.escape(version)}\b",
            upper,
        ):
            return version

    return None


def remove_version(text):
    result = text

    for phrase in VERSION_ALIASES:
        result = re.sub(
            rf"\b{re.escape(phrase)}\b",
            "",
            result,
            flags=re.IGNORECASE,
        )

    for version in sorted(
        KNOWN_VERSIONS,
        key=len,
        reverse=True,
    ):
        result = re.sub(
            rf"\b{re.escape(version)}\b",
            "",
            result,
            flags=re.IGNORECASE,
        )

    return re.sub(r"\s+", " ", result).strip()


def extract_reference(text):
    text = clean_command(text)

    # Remove Bible version before extracting the book.
    text = remove_version(text)

    # Remove common connecting words left by speech.
    text = re.sub(
        r"\b(in|using|with|from)\s*$",
        "",
        text,
        flags=re.IGNORECASE,
    ).strip()

    # John chapter 3 verse 16
    match = re.search(
        r"^(.+?)\s+chapter\s+(\d+)\s+verse\s+(\d+)$",
        text,
        re.IGNORECASE,
    )

    if match:
        return (
            match.group(1).strip(),
            int(match.group(2)),
            int(match.group(3)),
        )

    # John chapter 3:16
    match = re.search(
        r"^(.+?)\s+chapter\s+(\d+)\s*:\s*(\d+)$",
        text,
        re.IGNORECASE,
    )

    if match:
        return (
            match.group(1).strip(),
            int(match.group(2)),
            int(match.group(3)),
        )

    # John 3 verse 16
    match = re.search(
        r"^(.+?)\s+(\d+)\s+verse\s+(\d+)$",
        text,
        re.IGNORECASE,
    )

    if match:
        return (
            match.group(1).strip(),
            int(match.group(2)),
            int(match.group(3)),
        )

    # John 3:16
    match = re.search(
        r"^(.+?)\s+(\d+)\s*:\s*(\d+)$",
        text,
        re.IGNORECASE,
    )

    if match:
        return (
            match.group(1).strip(),
            int(match.group(2)),
            int(match.group(3)),
        )

    return None


def parse_command(text):
    version = extract_version(text)
    reference = extract_reference(text)

    result = {
        "version": version,
        "book": None,
        "chapter": None,
        "verse": None,
    }

    if reference:
        (
            result["book"],
            result["chapter"],
            result["verse"],
        ) = reference

    return result