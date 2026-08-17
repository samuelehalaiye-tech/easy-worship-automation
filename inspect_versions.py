from pywinauto import Desktop, Application
import pyautogui
import time


WINDOW_TITLE = "EasyWorship 2009 - Default Profile"


def main():
    desktop = Desktop(backend="win32")

    windows = desktop.windows(
        title=WINDOW_TITLE
    )

    if not windows:
        raise RuntimeError(
            "EasyWorship 2009 was not found."
        )

    wrapper = windows[0]

    app = Application(
        backend="win32"
    ).connect(handle=wrapper.handle)

    ew = app.window(handle=wrapper.handle)

    ew.set_focus()
    time.sleep(0.5)

    tabset = ew.child_window(
        class_name="TezTabset"
    ).wrapper_object()

    rect = tabset.rectangle()

    print("TezTabset:")
    print(rect)

    # Actual visible tab centers based on your screenshot.
    tabs = [
        ("TAB 1 / ASV", 20),
        ("TAB 2 / HCSB", 64),
        ("TAB 3 / KJV", 108),
        ("TAB 4 / RVA", 145),
    ]

    y = rect.height() // 2

    print("\nVersion test")
    print("============")

    for name, relative_x in tabs:

        screen_x = rect.left + relative_x
        screen_y = rect.top + y

        print("\n" + "=" * 40)
        print(name)
        print("Screen position:", screen_x, screen_y)

        pyautogui.moveTo(
            screen_x,
            screen_y,
            duration=0.2
        )

        pyautogui.click()

        time.sleep(1)

        input(
            "Look at EasyWorship. "
            "Is this tab highlighted? Press ENTER..."
        )


if __name__ == "__main__":
    main()