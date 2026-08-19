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


print("Before:", repr(locator.window_text()))

ew.set_focus()
time.sleep(0.5)

rect = locator.rectangle()

pyautogui.click(
    x=rect.left + 25,
    y=rect.top + rect.height() // 2,
)

time.sleep(0.3)

# Use actual Windows keyboard input.
pyautogui.hotkey("ctrl", "a")
time.sleep(0.2)

pyautogui.write(
    "Isaiah 2:2",
    interval=0.05,
)

time.sleep(1)

print("After:", repr(locator.window_text()))