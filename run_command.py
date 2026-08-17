from command_parser import parse_command
from version_control import display_scripture


def execute_command(text, live=False):
    print("=" * 50)
    print("COMMAND")
    print("=" * 50)

    print("Input:", text)

    command = parse_command(text)

    print("\nParsed:")
    print(command)

    if not command["version"]:
        raise ValueError(
            "No Bible version was detected."
        )

    if not command["book"]:
        raise ValueError(
            "No Scripture reference was detected."
        )

    return display_scripture(
        version=command["version"],
        book=command["book"],
        chapter=command["chapter"],
        verse=command["verse"],
        live=live,
    )


if __name__ == "__main__":

    command = input(
        "\nEnter an EasyWorship command: "
    )

    live_answer = input(
        "Go Live? (y/n): "
    ).strip().lower()

    live = live_answer == "y"

    execute_command(
        command,
        live=live,
    )