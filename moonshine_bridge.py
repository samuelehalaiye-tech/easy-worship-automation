import time
import requests

from moonshine_voice import MicTranscriber
from speech_parser import parse_spoken_reference


FASTAPI_URL = "http://127.0.0.1:8000/display"


def send_to_fastapi(text):
    text = text.strip()

    if not text:
        return

    print("\n" + "=" * 60)
    print("MOONSHINE")
    print("=" * 60)
    print(text)

    parsed = parse_spoken_reference(text)

    print("\nLOCAL PARSE")
    print(parsed)

    # Ignore ordinary speech.
    if not parsed.get("book"):
        print(
            "\nIGNORED: no valid Bible book was detected."
        )
        return

    # Verse ranges are recognized but not yet automated.
    if parsed.get("verse_end") is not None:
        print(
            f"\nVerse range detected. "
            f"Using first verse only: "
            f"{parsed['verse']}"
        )

    print(
        "\nSending Scripture to EasyWorship..."
    )

    try:
        response = requests.post(
            FASTAPI_URL,
            json={
                "command": text,
                "live": True,
            },
            timeout=120,
        )

        print("\nFASTAPI")
        print("HTTP:", response.status_code)
        print(response.text)

    except requests.RequestException as exc:
        print(
            "\nFASTAPI ERROR:",
            exc,
        )


def on_line(line):
    text = getattr(line, "text", "")

    if text:
        send_to_fastapi(text)


def main():

    print("=" * 60)
    print("MOONSHINE → EASYWORSHIP")
    print("=" * 60)
    print()
    print("Recognized Scripture → AUTOMATIC GO LIVE")
    print("F8 = Emergency automation ON/OFF")
    print()
    print("Starting Moonshine...")
    print("Press Ctrl+C to stop.")
    print()

    mic = (
        MicTranscriber()
        .on_line(on_line)
        .language("en")
    )

    print("Loading Moonshine...")
    mic.load()

    print("Moonshine loaded.")
    print("Listening...")
    print()

    mic.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping Moonshine...")

    finally:
        mic.stop()
        print("Moonshine stopped.")


if __name__ == "__main__":
    main()