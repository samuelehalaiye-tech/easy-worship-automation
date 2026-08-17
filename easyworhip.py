from pywinauto import Desktop, Application
import time


WINDOW_TITLE = "EasyWorship 2009 - Default Profile"


def get_easyworship():
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

    return app.window(handle=wrapper.handle)


def get_locator(ew):
    return ew.child_window(
        class_name="TScriptureLocator"
    ).wrapper_object()


def set_reference(book, chapter, verse):
    ew = get_easyworship()

    ew.set_focus()
    time.sleep(0.3)

    # -------------------------
    # BOOK
    # -------------------------

    box = get_locator(ew)

    rect = box.rectangle()

    box.click_input(
        coords=(25, rect.height() // 2)
    )

    time.sleep(0.2)

    box.type_keys(book)

    time.sleep(0.8)

    # -------------------------
    # CHAPTER
    # -------------------------

    box = get_locator(ew)

    box.type_keys("{RIGHT}")

    time.sleep(0.2)

    box.type_keys(str(chapter))

    time.sleep(0.8)

    # -------------------------
    # VERSE
    # -------------------------

    box = get_locator(ew)

    box.type_keys("{RIGHT}")

    time.sleep(0.2)

    box.type_keys(str(verse))

    time.sleep(0.8)

    return get_locator(ew).window_text()