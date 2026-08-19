from pywinauto import Desktop, Application


WINDOW_TITLE = "EasyWorship 2009 - Default Profile"


desktop = Desktop(backend="win32")

windows = desktop.windows(
    title=WINDOW_TITLE
)

if not windows:
    raise RuntimeError(
        "EasyWorship 2009 was not found."
    )

window = windows[0]

app = Application(
    backend="win32"
).connect(
    handle=window.handle
)

ew = app.window(
    handle=window.handle
)

locator = ew.child_window(
    class_name="TScriptureLocator"
).wrapper_object()


print("=" * 70)
print("SCRIPTURE LOCATOR")
print("=" * 70)

print("Class:", locator.class_name())
print("Text :", repr(locator.window_text()))
print("Handle:", locator.handle)

print()
print("=" * 70)
print("LOCATOR CHILDREN")
print("=" * 70)

children = locator.children()

print("Child count:", len(children))

for index, child in enumerate(children):

    try:
        rect = child.rectangle()
    except Exception:
        rect = None

    try:
        text = child.window_text()
    except Exception:
        text = "<error>"

    try:
        cls = child.class_name()
    except Exception:
        cls = "<error>"

    try:
        control_type = child.control_type()
    except Exception:
        control_type = "<error>"

    print()
    print(f"[{index}]")
    print("  Handle :", getattr(child, "handle", None))
    print("  Class  :", cls)
    print("  Type   :", control_type)
    print("  Text   :", repr(text))
    print("  Rect   :", rect)