import re


# =========================================================
# CANONICAL BIBLE BOOKS
# =========================================================

BIBLE_BOOKS = {
    "genesis": "Genesis",
    "exodus": "Exodus",
    "leviticus": "Leviticus",
    "numbers": "Numbers",
    "deuteronomy": "Deuteronomy",
    "joshua": "Joshua",
    "judges": "Judges",
    "ruth": "Ruth",
    "1 samuel": "1 Samuel",
    "2 samuel": "2 Samuel",
    "1 kings": "1 Kings",
    "2 kings": "2 Kings",
    "1 chronicles": "1 Chronicles",
    "2 chronicles": "2 Chronicles",
    "ezra": "Ezra",
    "nehemiah": "Nehemiah",
    "esther": "Esther",
    "job": "Job",
    "psalm": "Psalm",
    "psalms": "Psalm",
    "proverbs": "Proverbs",
    "ecclesiastes": "Ecclesiastes",
    "song of solomon": "Song of Solomon",
    "song of songs": "Song of Solomon",
    "isaiah": "Isaiah",
    "jeremiah": "Jeremiah",
    "lamentations": "Lamentations",
    "ezekiel": "Ezekiel",
    "daniel": "Daniel",
    "hosea": "Hosea",
    "joel": "Joel",
    "amos": "Amos",
    "obadiah": "Obadiah",
    "jonah": "Jonah",
    "micah": "Micah",
    "nahum": "Nahum",
    "habakkuk": "Habakkuk",
    "zephaniah": "Zephaniah",
    "haggai": "Haggai",
    "zechariah": "Zechariah",
    "malachi": "Malachi",

    "matthew": "Matthew",
    "mark": "Mark",
    "luke": "Luke",
    "john": "John",
    "acts": "Acts",
    "romans": "Romans",
    "1 corinthians": "1 Corinthians",
    "2 corinthians": "2 Corinthians",
    "galatians": "Galatians",
    "ephesians": "Ephesians",
    "philippians": "Philippians",
    "colossians": "Colossians",
    "1 thessalonians": "1 Thessalonians",
    "2 thessalonians": "2 Thessalonians",
    "1 timothy": "1 Timothy",
    "2 timothy": "2 Timothy",
    "titus": "Titus",
    "philemon": "Philemon",
    "hebrews": "Hebrews",
    "james": "James",
    "1 peter": "1 Peter",
    "2 peter": "2 Peter",
    "1 john": "1 John",
    "2 john": "2 John",
    "3 john": "3 John",
    "jude": "Jude",
    "revelation": "Revelation",
    "revelations": "Revelation",
}
NUMBERED_BOOK_ALIASES = {
    "first samuel": "1 samuel",
    "second samuel": "2 samuel",

    "first kings": "1 kings",
    "second kings": "2 kings",

    "first chronicles": "1 chronicles",
    "second chronicles": "2 chronicles",

    "first corinthians": "1 corinthians",
    "second corinthians": "2 corinthians",

    "first thessalonians": "1 thessalonians",
    "second thessalonians": "2 thessalonians",

    "first timothy": "1 timothy",
    "second timothy": "2 timothy",

    "first peter": "1 peter",
    "second peter": "2 peter",

    "first john": "1 john",
    "second john": "2 john",
    "third john": "3 john",
}
BOOK_CHAPTER_COUNTS = {
    "Genesis": 50,
    "Exodus": 40,
    "Leviticus": 27,
    "Numbers": 36,
    "Deuteronomy": 34,
    "Joshua": 24,
    "Judges": 21,
    "Ruth": 4,
    "1 Samuel": 31,
    "2 Samuel": 24,
    "1 Kings": 22,
    "2 Kings": 25,
    "1 Chronicles": 29,
    "2 Chronicles": 36,
    "Ezra": 10,
    "Nehemiah": 13,
    "Esther": 10,
    "Job": 42,
    "Psalm": 150,
    "Proverbs": 31,
    "Ecclesiastes": 12,
    "Song of Solomon": 8,
    "Isaiah": 66,
    "Jeremiah": 52,
    "Lamentations": 5,
    "Ezekiel": 48,
    "Daniel": 12,
    "Hosea": 14,
    "Joel": 3,
    "Amos": 9,
    "Obadiah": 1,
    "Jonah": 4,
    "Micah": 7,
    "Nahum": 3,
    "Habakkuk": 3,
    "Zephaniah": 3,
    "Haggai": 2,
    "Zechariah": 14,
    "Malachi": 4,

    "Matthew": 28,
    "Mark": 16,
    "Luke": 24,
    "John": 21,
    "Acts": 28,
    "Romans": 16,
    "1 Corinthians": 16,
    "2 Corinthians": 13,
    "Galatians": 6,
    "Ephesians": 6,
    "Philippians": 4,
    "Colossians": 4,
    "1 Thessalonians": 5,
    "2 Thessalonians": 3,
    "1 Timothy": 6,
    "2 Timothy": 4,
    "Titus": 3,
    "Philemon": 1,
    "Hebrews": 13,
    "James": 5,
    "1 Peter": 5,
    "2 Peter": 3,
    "1 John": 5,
    "2 John": 1,
    "3 John": 1,
    "Jude": 1,
    "Revelation": 22,
}


# =========================================================
# VERSION ALIASES
# =========================================================

VERSION_ALIASES = {
    "king james version": "KJV",
    "king james": "KJV",
    "new king james version": "NKJV",
    "new king james": "NKJV",
    "new living translation": "NLT",
    "holman christian standard": "HCSB",
    "holman": "HCSB",
}


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


# =========================================================
# SPOKEN NUMBERS
# =========================================================

NUMBER_WORDS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
}


def normalize_text(text):
    text = text.lower()

    # Remove punctuation used as sentence endings.
    text = re.sub(
        r"[?!,;]+$",
        "",
        text,
    )

    # A final period is sentence punctuation.
    # Remove it ONLY when it is not between digits.
    text = re.sub(
        r"(?<!\d)\.(?=\s*$)",
        "",
        text,
    )

    # Normalize commas, question marks, exclamation marks
    # and semicolons inside the sentence.
    text = text.replace(",", " ")
    text = text.replace("?", " ")
    text = text.replace("!", " ")
    text = text.replace(";", " ")

    # Preserve chapter/verse separators:
    #
    #   11.35 -> 11:35
    #   11:35 -> 11:35
    #
    text = re.sub(
        r"(?<=\d)\s*[.:]\s*(?=\d)",
        ":",
        text,
    )

    return re.sub(
        r"\s+",
        " ",
        text,
    ).strip()


def normalize_book(book):
    book = re.sub(
        r"\s+",
        " ",
        book.strip().lower(),
    )

    return BIBLE_BOOKS.get(book)


def spoken_number_to_int(text):
    text = text.lower().strip()

    if not text:
        return None

    if text.isdigit():
        return int(text)

    parts = text.split()

    total = 0

    for part in parts:
        value = NUMBER_WORDS.get(part)

        if value is None:
            return None

        total += value

    return total if total else None


def extract_version(text):
    lower = text.lower()

    for phrase, version in sorted(
        VERSION_ALIASES.items(),
        key=lambda x: len(x[0]),
        reverse=True,
    ):
        if re.search(
            rf"\b{re.escape(phrase)}\b",
            lower,
        ):
            return version

    upper = text.upper()

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


def find_book(text):
    """
    Find the longest canonical Bible book or spoken
    numbered-book form in the text.
    """

    lower = text.lower()

    # -------------------------------------------------
    # First handle spoken numbered books.
    # -------------------------------------------------

    aliases = sorted(
        NUMBERED_BOOK_ALIASES.items(),
        key=lambda x: len(x[0]),
        reverse=True,
    )

    for spoken_name, canonical_key in aliases:

        pattern = (
            rf"(?<!\w)"
            rf"{re.escape(spoken_name)}"
            rf"(?!\w)"
        )

        match = re.search(
            pattern,
            lower,
        )

        if match:

            return {
                "canonical":
                    BIBLE_BOOKS[canonical_key],
                "start":
                    match.start(),
                "end":
                    match.end(),
                "key":
                    canonical_key,
            }

    # -------------------------------------------------
    # Then handle normal canonical book names.
    # -------------------------------------------------

    candidates = sorted(
        BIBLE_BOOKS.items(),
        key=lambda x: len(x[0]),
        reverse=True,
    )

    for book_key, canonical in candidates:

        pattern = (
            rf"(?<!\w)"
            rf"{re.escape(book_key)}"
            rf"(?!\w)"
        )

        match = re.search(
            pattern,
            lower,
        )

        if match:

            return {
                "canonical": canonical,
                "start": match.start(),
                "end": match.end(),
                "key": book_key,
            }

    return None

def parse_numeric_after_book(text, book_end):
    """
    Handles:
        John 3:16
        John 3 verse 16
        John chapter 3 verse 16
        John chapter 3:16
    """

    tail = text[book_end:].strip()

    # chapter 3 verse 16
    match = re.match(
        r"chapter\s+(\d+)\s+verse\s+(\d+)",
        tail,
        re.IGNORECASE,
    )

    if match:
        return (
            int(match.group(1)),
            int(match.group(2)),
            None,
        )

    # chapter 3:16
    match = re.match(
        r"chapter\s+(\d+)\s*:\s*(\d+)",
        tail,
        re.IGNORECASE,
    )

    if match:
        return (
            int(match.group(1)),
            int(match.group(2)),
            None,
        )

    # 3 verse 16
    match = re.match(
        r"(\d+)\s+verse\s+(\d+)",
        tail,
        re.IGNORECASE,
    )

    if match:
        return (
            int(match.group(1)),
            int(match.group(2)),
            None,
        )

    # 3 verse 1 to 2
    match = re.match(
        r"(\d+)\s+verse\s+(\d+)\s+to\s+(\d+)",
        tail,
        re.IGNORECASE,
    )

    if match:
        return (
            int(match.group(1)),
            int(match.group(2)),
            int(match.group(3)),
        )

    # 3:16
    match = re.match(
        r"(\d+)\s*:\s*(\d+)",
        tail,
        re.IGNORECASE,
    )

    if match:
        return (
            int(match.group(1)),
            int(match.group(2)),
            None,
        )

    return None


def parse_spoken_after_book(text, book_end):
    """
    Handles spoken forms such as:

        John eleven thirty five
        John two verse two
        John chapter three verse sixteen
    """

    tail = text[book_end:].strip()

    # Remove conversational words between book and numbers.
    tail = re.sub(
        r"\b(chapter|verse)\b",
        " ",
        tail,
        flags=re.IGNORECASE,
    )

    tail = re.sub(
        r"\s+",
        " ",
        tail,
    ).strip()

    words = tail.split()

    # -----------------------------------------------------
    # chapter + verse spoken separately
    #
    # "three verse sixteen"
    # -----------------------------------------------------

    match = re.match(
        r"^(.+?)\s+to\s+(.+)$",
        tail,
        re.IGNORECASE,
    )

    # "two verse two"
    original_tail = text[book_end:].strip()

    match = re.match(
        r"^(.+?)\s+verse\s+(.+)$",
        original_tail,
        re.IGNORECASE,
    )

    if match:

        chapter = spoken_number_to_int(
            match.group(1)
        )

        verse_text = match.group(2).strip()

        range_match = re.match(
            r"^(.+?)\s+to\s+(.+)$",
            verse_text,
            re.IGNORECASE,
        )

        if range_match:

            verse = spoken_number_to_int(
                range_match.group(1)
            )

            verse_end = spoken_number_to_int(
                range_match.group(2)
            )

            if (
                chapter is not None
                and verse is not None
                and verse_end is not None
            ):
                return (
                    chapter,
                    verse,
                    verse_end,
                )

        verse = spoken_number_to_int(
            verse_text
        )

        if (
            chapter is not None
            and verse is not None
        ):
            return (
                chapter,
                verse,
                None,
            )

    # -----------------------------------------------------
    # "John eleven thirty five"
    # -----------------------------------------------------

    words = original_tail.split()

    if len(words) >= 2:

        chapter_text = words[0]
        verse_text = " ".join(words[1:])

        chapter = spoken_number_to_int(
            chapter_text
        )

        verse = spoken_number_to_int(
            verse_text
        )

        if (
            chapter is not None
            and verse is not None
        ):
            return (
                chapter,
                verse,
                None,
            )

    return None


def parse_compact_reference_number(
    text,
    book,
):
    """
    Interpret compact chapter/verse numbers using
    the actual chapter count of the Bible book.

    Examples:

        Job 1135       -> 11:35
        John 316       -> 3:16
        Psalm 11911    -> 119:11
        Romans 828     -> 8:28
    """

    text = text.strip()

    if not text.isdigit():
        return None

    if len(text) < 3 or len(text) > 5:
        return None

    max_chapter = BOOK_CHAPTER_COUNTS.get(
        book
    )

    if max_chapter is None:
        return None

    candidates = []

    for split in range(1, len(text)):

        chapter_text = text[:split]
        verse_text = text[split:]

        chapter = int(chapter_text)
        verse = int(verse_text)

        # Chapter must actually exist in this book.
        if chapter > max_chapter:
            continue

        # Bible verses won't exceed 176.
        if verse < 1 or verse > 176:
            continue

        candidates.append(
            (chapter, verse)
        )

    if not candidates:
        return None

    # Prefer the split with the largest chapter number
    # among VALID chapters.
    return max(
        candidates,
        key=lambda pair: pair[0],
    )


def parse_spoken_reference(text):
    """
    Extract a Bible reference from natural language.

    The surrounding language is intentionally ignored.

    Examples:

        What does Joshua chapter 1 verse 2 say?
        Can you show John 3:16?
        I want Romans 8:28 in HCSB.
        Let's look at Exodus 2:1.
        John eleven thirty five.
    """

    original = text

    normalized = normalize_text(
        text
    )

    version = extract_version(
        original
    )

    book = find_book(
        normalized
    )

    if not book:
        return {
            "version": version,
            "book": None,
            "chapter": None,
            "verse": None,
        }

    # First try explicit numeric syntax.
    numeric = parse_numeric_after_book(
        normalized,
        book["end"],
    )

    if numeric:

        chapter, verse, verse_end = numeric

        result = {
            "version": version,
            "book": book["canonical"],
            "chapter": chapter,
            "verse": verse,
        }

        if verse_end is not None:
            result["verse_end"] = verse_end

        return result
    
        # =====================================================
    # COMPACT NUMERIC REFERENCE
    #
    # Examples:
    #   Job 1135       -> Job 11:35
    #   Psalm 11911    -> Psalm 119:11
    #   John 316       -> John 3:16
    # =====================================================

    tail = normalized[book["end"]:].strip()

    # Remove trailing conversational wording.
    tail = re.sub(
        r"\b(say|says|see|read|mean|means)\b.*$",
        "",
        tail,
        flags=re.IGNORECASE,
    ).strip()

    compact = parse_compact_reference_number(
    tail,
    book["canonical"],
)

    if compact:

        chapter, verse = compact

        return {
            "version": version,
            "book": book["canonical"],
            "chapter": chapter,
            "verse": verse,
        }

    # Then spoken-number syntax.
    spoken = parse_spoken_after_book(
        normalized,
        book["end"],
    )

    if spoken:

        chapter, verse, verse_end = spoken

        result = {
            "version": version,
            "book": book["canonical"],
            "chapter": chapter,
            "verse": verse,
        }

        if verse_end is not None:
            result["verse_end"] = verse_end

        return result

    return {
        "version": version,
        "book": None,
        "chapter": None,
        "verse": None,
    }