from speech_parser import parse_spoken_reference


def handle_transcript(text):
    print("\nMOONSHINE TRANSCRIPT:")
    print(text)

    result = parse_spoken_reference(text)

    if result is None:
        print("Not recognized as a Scripture reference.")
        return

    print("PARSED REFERENCE:")
    print(result)


def main():
    print("Moonshine parser test")
    print("=====================")
    print("This stage does NOT control EasyWorship.")
    print()

    # Temporary manual test.
    # We will replace this with Moonshine microphone
    # callbacks in the next step.
    while True:
        text = input("\nTranscript: ").strip()

        if text.lower() in {
            "quit",
            "exit",
        }:
            break

        handle_transcript(text)


if __name__ == "__main__":
    main()