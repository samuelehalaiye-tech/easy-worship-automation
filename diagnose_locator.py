"""Inspect and exercise the EasyWorship 2009 Scripture locator.

This diagnostic never clicks Go Live.  It records the reference reported by
EasyWorship after entering book -> RIGHT -> chapter:verse, the sequence
specified by the EasyWorship 2009 manual.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import time

import pyautogui
import win32clipboard
import win32gui
import win32con
from pywinauto import Desktop


WINDOW_TITLE = "EasyWorship 2009 - Default Profile"
LOCATOR_CLASS = "TScriptureLocator"


@contextmanager
def temporary_clipboard(text):
    """Paste text without leaving the user's clipboard changed."""
    win32clipboard.OpenClipboard()
    try:
        try:
            previous = win32clipboard.GetClipboardData(
                win32clipboard.CF_UNICODETEXT
            )
        except TypeError:
            previous = None
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text)
    finally:
        win32clipboard.CloseClipboard()

    try:
        yield
    finally:
        win32clipboard.OpenClipboard()
        try:
            win32clipboard.EmptyClipboard()
            if previous is not None:
                win32clipboard.SetClipboardText(previous)
        finally:
            win32clipboard.CloseClipboard()


def get_easyworship():
    windows = Desktop(backend="win32").windows(title=WINDOW_TITLE)
    if not windows:
        raise RuntimeError("EasyWorship 2009 was not found.")

    window = windows[0]
    if not window.is_visible():
        window.restore()
        time.sleep(0.5)

    window.set_focus()
    time.sleep(0.3)
    return window


def get_locator(window):
    locators = [
        control
        for control in window.descendants()
        if control.class_name() == LOCATOR_CLASS
    ]
    if not locators:
        raise RuntimeError("EasyWorship Scripture locator was not found.")
    return locators[0]


def enter_reference(locator, book, chapter, verse):
    """Enter a reference with EasyWorship 2009's documented sequence."""
    locator.click_input(coords=(15, locator.rectangle().height() // 2))
    time.sleep(0.15)
    print("  foreground after click:", hex(win32gui.GetForegroundWindow()))

    # Ctrl+A only selects the book portion in this custom control.  It is
    # needed because clicking the book area alone leaves the previous book
    # selected inconsistently when focus moves back from another control.
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.10)
    pyautogui.write(book, interval=0.03)
    time.sleep(0.25)
    print("  after book:", repr(locator.window_text()))

    pyautogui.press("right")
    time.sleep(0.10)

    # The control switches from book completion to the whole verse address.
    pyautogui.write(f"{chapter}:{verse}", interval=0.03)
    time.sleep(0.35)

    return locator.window_text()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--one", action="store_true")
    parser.add_argument("--book-only", action="store_true")
    parser.add_argument("--paste", action="store_true")
    parser.add_argument("--navigation", action="store_true")
    parser.add_argument("--wm-settext", action="store_true")
    parser.add_argument("--wm-reference", action="store_true")
    args = parser.parse_args()

    window = get_easyworship()
    locator = get_locator(window)

    print("Locator class:", locator.class_name())
    print("Locator rect :", locator.rectangle())
    print("Visible      :", locator.is_visible())
    print("Initial text :", repr(locator.window_text()))

    if args.book_only:
        locator.click_input(
            coords=(15, locator.rectangle().height() // 2)
        )
        time.sleep(0.15)
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.10)
        if args.paste:
            with temporary_clipboard("John"):
                pyautogui.hotkey("ctrl", "v")
        else:
            pyautogui.write("John", interval=0.10)
        time.sleep(0.50)
        window.capture_as_image().save("locator_diagnostic_result.png")
        print("Book-only result:", repr(locator.window_text()))
        return

    if args.navigation:
        locator.click_input(
            coords=(15, locator.rectangle().height() // 2)
        )
        pyautogui.hotkey("ctrl", "a")
        pyautogui.write("j")
        time.sleep(0.30)
        print("J:", repr(locator.window_text()))
        for index in range(1, 8):
            pyautogui.press("down")
            time.sleep(0.20)
            print(f"down {index}:", repr(locator.window_text()))
        window.capture_as_image().save("locator_diagnostic_result.png")
        return

    if args.wm_settext:
        result = win32gui.SendMessage(
            locator.handle,
            win32con.WM_SETTEXT,
            0,
            "John",
        )
        time.sleep(0.50)
        window.capture_as_image().save("locator_diagnostic_result.png")
        print("WM_SETTEXT result:", result)
        print("WM_SETTEXT text  :", repr(locator.window_text()))
        return

    if args.wm_reference:
        win32gui.SendMessage(
            locator.handle,
            win32con.WM_SETTEXT,
            0,
            "John",
        )
        locator.set_focus()
        pyautogui.press("right")
        time.sleep(0.20)
        pyautogui.write("11:35", interval=0.08)
        time.sleep(0.75)
        window.capture_as_image().save("locator_diagnostic_result.png")
        print("WM reference text:", repr(locator.window_text()))
        return

    references = [
        ("Genesis", 1, 1),
        ("John", 11, 35),
        ("Isaiah", 2, 2),
        ("Mark", 2, 2),
        ("James", 2, 3),
        ("Psalm", 119, 11),
    ]
    if args.one:
        references = [("John", 11, 35)]
    else:
        references.extend([("John", 11, 35)] * args.repeat)

    failures = []
    for index, (book, chapter, verse) in enumerate(references, start=1):
        expected = f"{book} {chapter}:{verse}"
        actual = enter_reference(locator, book, chapter, verse)
        window.capture_as_image().save("locator_diagnostic_result.png")
        passed = actual.casefold() == expected.casefold()
        print(
            f"{index:02d}. expected={expected!r} actual={actual!r} "
            f"result={'PASS' if passed else 'FAIL'}"
        )
        if not passed:
            failures.append((expected, actual))

    if failures:
        raise SystemExit(f"{len(failures)} locator test(s) failed")


if __name__ == "__main__":
    main()
