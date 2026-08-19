from speech_parser import parse_spoken_reference


tests = [
    "Show me John 3:16.",
    "Revelations 2:5",
    "Habakkuk 7 verse 8",
    "Nahum two verse two",
    "john eleven thirty five jesus wept",
    "Psalms 5 verse 1 to 2",
]


for text in tests:
    print()
    print("INPUT:")
    print(text)

    result = parse_spoken_reference(text)

    print("OUTPUT:")
    print(result)