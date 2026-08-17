from pywinauto import Desktop
import time


def main():
    windows = Desktop(backend="win32").windows(
        title_re=r".*EasyWorship.*"
    )

    if not windows:
        raise RuntimeError("EasyWorship was not found.")

    ew = windows[0]
    ew.set_focus()

    # Find the actual Scripture reference control
    scripture_box = ew.child_window(
        class_name="TScriptureLocator"
    )

    print("Found:", scripture_box.window_text())

    # Focus it
    scripture_box.set_focus()

    # Replace current reference
    scripture_box.type_keys(
        "^a",
        set_foreground=True
    )

    scripture_box.type_keys(
        "John 3:16",
        set_foreground=True
    )

    print("New value:", scripture_box.window_text())


if __name__ == "__main__":
    main()