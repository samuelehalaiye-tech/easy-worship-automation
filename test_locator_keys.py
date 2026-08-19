from pywinauto import Desktop, Application
import pyautogui
import time


WINDOW_TITLE = "EasyWorship 2009 - Default Profile"


desktop = Desktop(backend="win32")

windows = desktop.windows(
    title=WINDOW_TITLE
)

if not windows:
    raise RuntimeError(
        "EasyWorship 2009 was not found."
    )

app = Application(
    backend="win32"
).connect(
    handle=windows[0].handle
)

ew = app.window(
    handle=windows[0].handle
)

locator = ew.child_window(
    class_name="TScriptureLocator"
).wrapper_object()


def show(label):
    print(
        f"{label}: {locator.window_text()!r}"
    )


ew.set_focus()

time.sleep(0.5)

rect = locator.rectangle()

pyautogui.click(
    x=rect.left + 10,
    y=rect.top + rect.height() // 2,
)

time.sleep(0.2)

pyautogui.hotkey(
    "ctrl",
    "a",
)

time.sleep(0.1)

pyautogui.write(
    "Genesis",
    interval=0.08,
)

time.sleep(0.3)

show("BOOK")


# Test TAB
pyautogui.press("tab")
time.sleep(0.3)
show("TAB")


# Test ENTER
pyautogui.press("enter")
time.sleep(0.3)
show("ENTER")


# Test DOWN
pyautogui.press("down")
time.sleep(0.3)
show("DOWN")


# Test UP
pyautogui.press("up")
time.sleep(0.3)
show("UP")


# Test SPACE
pyautogui.press("space")
time.sleep(0.3)
show("SPACE")