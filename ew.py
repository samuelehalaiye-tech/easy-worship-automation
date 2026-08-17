import argparse
import re

from version_control import (
    display_scripture,
    select_version,
    set_reference,
    go_live,
)


def parse_reference(text):
    """
    Convert common Scripture reference formats into:
        book, chapter, verse

    Supported examples:

        John 3:16
        John 3 verse 16
        John chapter 3 verse 16
        John chapter 3:16
        1 Corinthians 13:4
        Psalm 23:1
    """

    text = text.strip()

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # --------------------------------------------------
    # 1. John chapter 3 verse 16
    # --------------------------------------------------
    match = re.match(
        r"^(.+?)\s+chapter\s+(\d+)\s+verse\s+(\d+)$",
        text,
        re.IGNORECASE,
    )

    if match:
        book = match.group(1).strip()
        chapter = int(match.group(2))
        verse = int(match.group(3))

        return book, chapter, verse

    # --------------------------------------------------
    # 2. John chapter 3:16
    # --------------------------------------------------
    match = re.match(
        r"^(.+?)\s+chapter\s+(\d+)\s*:\s*(\d+)$",
        text,
        re.IGNORECASE,
    )

    if match:
        book = match.group(1).strip()
        chapter = int(match.group(2))
        verse = int(match.group(3))

        return book, chapter, verse

    # --------------------------------------------------
    # 3. John 3 verse 16
    # --------------------------------------------------
    match = re.match(
        r"^(.+?)\s+(\d+)\s+verse\s+(\d+)$",
        text,
        re.IGNORECASE,
    )

    if match:
        book = match.group(1).strip()
        chapter = int(match.group(2))
        verse = int(match.group(3))

        return book, chapter, verse

    # --------------------------------------------------
    # 4. John 3:16
    # --------------------------------------------------
    match = re.match(
        r"^(.+?)\s+(\d+)\s*:\s*(\d+)$",
        text,
        re.IGNORECASE,
    )

    if match:
        book = match.group(1).strip()
        chapter = int(match.group(2))
        verse = int(match.group(3))

        return book, chapter, verse

    raise ValueError(
        f"Could not understand Scripture reference: {text!r}"
    )


def main():
    parser = argparse.ArgumentParser(
        description="EasyWorship 2009 Controller"
    )

    parser.add_argument(
        "--version",
        help="Bible version, e.g. ASV, HCSB, RVA",
    )

    parser.add_argument(
        "--reference",
        help='Scripture reference, e.g. "John 3:16"',
    )

    parser.add_argument(
        "--live",
        action="store_true",
        help="Send the prepared Scripture Live",
    )

    args = parser.parse_args()

    # Nothing supplied.
    if not any(
        [
            args.version,
            args.reference,
            args.live,
        ]
    ):
        parser.print_help()
        return

    # Version only.
    if args.version and not args.reference:
        select_version(args.version)

        print(
            f"\nVersion {args.version.upper()} selected."
        )

        return

    # Reference only.
    if args.reference and not args.version:
        book, chapter, verse = parse_reference(
            args.reference
        )

        result = set_reference(
            book,
            chapter,
            verse,
        )

        print(
            "\nEasyWorship reports:",
            result,
        )

        return

    # Version + reference.
    if args.version and args.reference:
        book, chapter, verse = parse_reference(
            args.reference
        )

        display_scripture(
            version=args.version,
            book=book,
            chapter=chapter,
            verse=verse,
            live=args.live,
        )

        return

    # Live only.
    if args.live:
        go_live()


if __name__ == "__main__":
    main()