from version_control import select_version
from easyworhip import set_reference, get_easyworship
import time


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


def display_scripture(version, book, chapter, verse):

    print("=" * 50)
    print("EASYWORSHIP CONTROLLER")
    print("=" * 50)

    print(f"Version : {version}")
    print(f"Reference: {book} {chapter}:{verse}")

    print("\n[1/3] Selecting Bible version...")
    select_version(version)

    print("\n[2/3] Entering Scripture...")
    reference = set_reference(
        book,
        chapter,
        verse
    )

    expected = f"{book} {chapter}:{verse}"

    print("EasyWorship reports:", reference)

    if reference != expected:
        raise RuntimeError(
            f"Reference verification failed.\n"
            f"Expected: {expected}\n"
            f"Actual:   {reference}"
        )

    print("\n[3/3] Sending Go Live...")
    go_live()

    print("\nSUCCESS")
    print(
        f"{version} {reference} is now Live."
    )