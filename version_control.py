from pywinauto import Desktop, Application
from PIL import ImageGrab, ImageOps, ImageEnhance
from pytesseract import Output
import pytesseract
import pyautogui
import os
import re
import time
import win32gui
import win32con


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

        pyautogui.click(
                x=screen_x,
                y=screen_y
            )


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


def _normalize_reference_text(text):
    if text is None:
        return ""

    text = str(text).strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s*:\s*", ":", text)
    return text


def _read_locator_text(box):
    """The TScriptureLocator is a custom single-field control and its
    internal state is not always faithfully exposed by window_text().
    Prefer the actual control text when available, then fall back to a
    screen OCR read of the locator itself.
    """

    try:
        text = box.window_text()
        if text:
            return _normalize_reference_text(text)
    except Exception:
        pass

    rect = box.rectangle()
    image = ImageGrab.grab(
        bbox=(
            rect.left,
            rect.top,
            rect.right,
            rect.bottom,
        )
    )

    image = image.resize((image.width * 3, image.height * 3))
    image = ImageOps.grayscale(image)
    image = ImageEnhance.Contrast(image).enhance(2.2)

    data = pytesseract.image_to_data(
        image,
        lang="eng",
        config="--psm 7",
        output_type=Output.DICT,
    )

    lines = []
    for raw in data["text"]:
        value = raw.strip()
        if value:
            lines.append(value)

    if not lines:
        return ""

    return _normalize_reference_text(" ".join(lines))


def set_reference(book, chapter, verse):
    """Enter a Scripture reference into the custom TScriptureLocator.

    This control behaves as a single-field edit box, not a segmented
    book/chapter/verse widget. Directly writing the canonical reference text
    via WM_SETTEXT is the only reliable operation we have verified against the
    live EasyWorship control.
    """

    ew = get_easyworship()
    ew.set_focus()
    time.sleep(0.10)

    box = get_locator(ew)
    box.set_focus()

    reference_text = f"{book} {chapter}:{verse}"

    try:
        win32gui.SendMessage(
            box.handle,
            win32con.WM_SETTEXT,
            0,
            reference_text,
        )
    except Exception:
        # Fallback: if direct control text update is unavailable in a given
        # session, fall back to a single-field keyboard path.
        rect = box.rectangle()
        box.click_input(coords=(25, rect.height() // 2))
        time.sleep(0.10)
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.08)
        pyautogui.write(reference_text, interval=0.02)
        time.sleep(0.15)
        pyautogui.press("enter")
        time.sleep(0.30)

    return _read_locator_text(box)


def set_reference_verified(
    book,
    chapter,
    verse,
    attempts=2,
):
    expected = (
        f"{book} {chapter}:{verse}"
    )

    last_actual = None

    for attempt in range(1, attempts + 1):

        print(
            f"\nReference attempt "
            f"{attempt}/{attempts}"
        )

        reference = set_reference(
            book,
            chapter,
            verse,
        )

        last_actual = reference

        print(
            "EasyWorship reports:",
            reference,
        )

        if (
            _normalize_reference_text(reference).lower()
            == _normalize_reference_text(expected).lower()
        ):
            return reference

        print(
            "Reference mismatch."
        )

        print(
            f"Expected: {expected}"
        )

        print(
            f"Actual:   {reference}"
        )

        if attempt < attempts:
            print(
                "Retrying EasyWorship reference..."
            )

            time.sleep(0.30)

    raise RuntimeError(
        "Reference verification failed "
        f"after {attempts} attempts.\n"
        f"Expected: {expected}\n"
        f"Actual: {last_actual}"
    )
def go_live():
    ew = get_easyworship()

    ew.set_focus()

    button = ew.child_window(
        title="Go Live",
        class_name="TsdSpeedButton"
    ).wrapper_object()

    button.click_input()

    time.sleep(0.25)

    print("Go Live complete.")


def display_scripture(
    version,
    book,
    chapter,
    verse,
    live=False,
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

    # ---------------------------------------------
    # 1. VERSION
    # ---------------------------------------------

    print(
        "\n[1/3] Selecting Bible version..."
    )

    select_version(version)

    # ---------------------------------------------
    # 2. REFERENCE
    # ---------------------------------------------

    print(
        "\n[2/3] Entering Scripture..."
    )

    reference = set_reference_verified(
        book,
        chapter,
        verse,
        attempts=2,
    )

    # ---------------------------------------------
    # 3. LIVE
    # ---------------------------------------------

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

    return reference

def prepare_reference(
    book,
    chapter,
    verse,
    live=False,
):
    """
    Enter a Scripture reference without changing
    the currently selected Bible version.
    """

    print("=" * 50)
    print("EASYWORSHIP CONTROLLER")
    print("=" * 50)

    print(
        f"Reference : {book} {chapter}:{verse}"
    )

    print(
        f"Go Live   : {live}"
    )

    print(
        "\n[1/2] Entering Scripture..."
    )

    reference = set_reference_verified(
        book,
        chapter,
        verse,
        attempts=2,
    )

    if live:

        print(
            "\n[2/2] Sending Go Live..."
        )

        go_live()

    else:

        print(
            "\n[2/2] Preview prepared."
        )

    print("\nSUCCESS")

    return reference