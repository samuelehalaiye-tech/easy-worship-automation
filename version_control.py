from pywinauto import Desktop, Application
from PIL import ImageGrab, ImageOps, ImageEnhance
from pytesseract import Output
import pytesseract
import pyautogui
import os
import re
import time


WINDOW_TITLE = "EasyWorship 2009 - Default Profile"

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TESSDATA_DIR = r"C:\Program Files\Tesseract-OCR\tessdata"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
os.environ["TESSDATA_PREFIX"] = TESSDATA_DIR


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


def get_tabset(ew):
    return ew.child_window(
        class_name="TezTabset"
    ).wrapper_object()


def get_locator(ew):
    return ew.child_window(
        class_name="TScriptureLocator"
    ).wrapper_object()


def normalize(text):
    return re.sub(
        r"[^A-Z0-9]",
        "",
        text.upper().strip()
    )


def recognize_version(text):
    text = normalize(text)

    if text == "ASV":
        return "ASV"

    if text == "HCSB":
        return "HCSB"

    if text == "RVA":
        return "RVA"

    # KJV is sometimes read as K, [K..., etc.
    if text == "KJV" or text == "K":
        return "KJV"

    if text.startswith("K"):
        return "KJV"

    return None


def read_version_tabs(tabset):
    rect = tabset.rectangle()

    image = ImageGrab.grab(
        bbox=(
            rect.left,
            rect.top,
            rect.right,
            rect.bottom
        )
    )

    # Enlarge tiny tab text.
    image = image.resize(
        (
            image.width * 5,
            image.height * 5
        )
    )

    image = ImageOps.grayscale(image)

    image = ImageEnhance.Contrast(image).enhance(2.5)

    data = pytesseract.image_to_data(
        image,
        lang="eng",
        config="--psm 7",
        output_type=Output.DICT
    )

    versions = {}

    for i in range(len(data["text"])):
        raw = data["text"][i].strip()

        if not raw:
            continue

        try:
            confidence = float(data["conf"][i])
        except Exception:
            continue

        if confidence < 20:
            continue

        version = recognize_version(raw)

        if not version:
            continue

        x = data["left"][i]
        y = data["top"][i]
        w = data["width"][i]
        h = data["height"][i]

        scale = 5

        relative_x = (x + w / 2) / scale
        relative_y = (y + h / 2) / scale

        versions[version] = {
            "x": relative_x,
            "y": relative_y,
            "confidence": confidence,
            "ocr": raw
        }

    return rect, versions


def select_version(version):
    version = version.upper().strip()

    if not version:
        raise ValueError(
            "Bible version cannot be empty."
        )

    ew = get_easyworship()
    ew.set_focus()

    time.sleep(0.3)

    tabset = get_tabset(ew)

    rect, versions = read_version_tabs(tabset)

    print("\nDetected versions:")

    for name, info in versions.items():
        print(
            f"  {name}: "
            f"relative=({info['x']:.1f}, "
            f"{info['y']:.1f}) "
            f"confidence={info['confidence']:.1f}"
        )

    # OCR found requested version.
    if version in versions:
        info = versions[version]

        screen_x = rect.left + info["x"]
        screen_y = rect.top + info["y"]

        print(
            f"\nSelecting {version}"
        )
        print(
            f"Screen position: "
            f"{screen_x:.1f}, {screen_y:.1f}"
        )

        pyautogui.moveTo(
            screen_x,
            screen_y,
            duration=0.2
        )

        pyautogui.click()

        time.sleep(1)

        return True

    # RVA fallback if OCR misses it.
    if version == "RVA":
        print(
            "\nRVA was not detected by OCR."
        )

        print(
            "Using rightmost-tab fallback."
        )

        screen_x = rect.left + 185
        screen_y = rect.top + rect.height() / 2

        pyautogui.moveTo(
            screen_x,
            screen_y,
            duration=0.2
        )

        pyautogui.click()

        time.sleep(1)

        return True

    raise RuntimeError(
        f"Version {version} was not found "
        f"on the current EasyWorship screen."
    )


def set_reference(book, chapter, verse):
    ew = get_easyworship()

    ew.set_focus()
    time.sleep(0.3)

    # BOOK
    box = get_locator(ew)

    rect = box.rectangle()

    box.click_input(
        coords=(25, rect.height() // 2)
    )

    time.sleep(0.2)

    box.type_keys(str(book))

    time.sleep(0.8)

    # CHAPTER
    box = get_locator(ew)

    box.type_keys("{RIGHT}")

    time.sleep(0.2)

    box.type_keys(str(chapter))

    time.sleep(0.8)

    # VERSE
    box = get_locator(ew)

    box.type_keys("{RIGHT}")

    time.sleep(0.2)

    box.type_keys(str(verse))

    time.sleep(0.8)

    return get_locator(ew).window_text()


def go_live():
    ew = get_easyworship()

    ew.set_focus()

    time.sleep(0.3)

    button = ew.child_window(
        title="Go Live",
        class_name="TsdSpeedButton"
    ).wrapper_object()

    button.click()

    time.sleep(1)

    print("Go Live complete.")


def display_scripture(
    version,
    book,
    chapter,
    verse,
    live=False
):
    print("=" * 50)
    print("EASYWORSHIP CONTROLLER")
    print("=" * 50)

    print(f"Version   : {version}")
    print(
        f"Reference : "
        f"{book} {chapter}:{verse}"
    )
    print(f"Go Live   : {live}")

    # 1. VERSION
    print("\n[1/3] Selecting Bible version...")
    select_version(version)

    # 2. REFERENCE
    print("\n[2/3] Entering Scripture...")

    reference = set_reference(
        book,
        chapter,
        verse
    )

    expected = f"{book} {chapter}:{verse}"

    print(
        "EasyWorship reports:",
        reference
    )

    # EasyWorship normalizes the reference to:
    # Book Chapter:Verse
    #
    # Compare against the parsed/normalized reference,
    # not the original spoken wording.
    if reference.strip().lower() != expected.strip().lower():
        raise RuntimeError(
            "Reference verification failed.\n"
            f"Expected: {expected}\n"
            f"Actual: {reference}"
        )

    # 3. LIVE
    if live:
        print(
            "\n[3/3] Sending Go Live..."
        )
        go_live()
    else:
        print(
            "\n[3/3] Preview prepared."
        )

    print("\nSUCCESS")


if __name__ == "__main__":
    print(
        "This module provides functions for "
        "the EasyWorship controller."
    )