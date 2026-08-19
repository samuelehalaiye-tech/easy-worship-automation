from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import keyboard
import threading
import re

from speech_parser import (
    parse_spoken_reference,
    extract_version,
)

from version_control import (
    display_scripture,
    prepare_reference,
)


app = FastAPI(
    title="EasyWorship Controller",
    version="1.0.0",
)


AUTOMATION_ENABLED = True

CURRENT_VERSION = None
CURRENT_BOOK = None
CURRENT_CHAPTER = None
CURRENT_VERSE = None


# =========================================================
# AUTOMATION SWITCH
# =========================================================

def toggle_automation():
    global AUTOMATION_ENABLED

    AUTOMATION_ENABLED = not AUTOMATION_ENABLED

    print("\n==============================")
    print(
        "AUTOMATION:",
        "ON" if AUTOMATION_ENABLED else "OFF"
    )
    print("==============================")


def hotkey_listener():
    keyboard.add_hotkey(
        "f8",
        toggle_automation,
    )

    print("F8 = Toggle automation ON/OFF")

    keyboard.wait()


# =========================================================
# API MODELS
# =========================================================

class DisplayRequest(BaseModel):
    command: str
    live: bool = True


class ToggleResponse(BaseModel):
    automation_enabled: bool


# =========================================================
# STATE
# =========================================================

def save_reference(parsed):
    global CURRENT_BOOK
    global CURRENT_CHAPTER
    global CURRENT_VERSE

    CURRENT_BOOK = parsed["book"]
    CURRENT_CHAPTER = parsed["chapter"]
    CURRENT_VERSE = parsed["verse"]


def save_version(version):
    global CURRENT_VERSION

    CURRENT_VERSION = version


def current_reference_exists():
    return (
        CURRENT_BOOK is not None
        and CURRENT_CHAPTER is not None
        and CURRENT_VERSE is not None
    )


# =========================================================
# VERSION-ONLY CORRECTION
# =========================================================

def detect_version_only_command(text):
    """
    Recognize commands such as:

        use HCSB
        actually use HCSB
        actually, use HCSB
        switch to ASV
        change to HCSB
        use the HCSB
    """

    cleaned = text.strip().lower()

    # Remove punctuation.
    cleaned = re.sub(r"[,.!?]", " ", cleaned)

    # Normalize spaces.
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    patterns = [
        r"^use\s+(?:the\s+)?(.+)$",
        r"^actually\s+use\s+(?:the\s+)?(.+)$",
        r"^switch\s+to\s+(?:the\s+)?(.+)$",
        r"^change\s+to\s+(?:the\s+)?(.+)$",
        r"^change\s+(?:the\s+)?version\s+to\s+(?:the\s+)?(.+)$",
        r"^actually\s+switch\s+to\s+(?:the\s+)?(.+)$",
    ]

    for pattern in patterns:
        match = re.match(
            pattern,
            cleaned,
            re.IGNORECASE,
        )

        if match:
            candidate = match.group(1).strip()

            # Ask the speech parser's version logic
            # to resolve the candidate.
            version = extract_version(candidate)

            if version:
                return version

    return None


# =========================================================
# STATUS
# =========================================================

@app.get("/status")
def status():

    return {
        "automation_enabled": AUTOMATION_ENABLED,
        "current_version": CURRENT_VERSION,
        "current_reference": (
            f"{CURRENT_BOOK} "
            f"{CURRENT_CHAPTER}:"
            f"{CURRENT_VERSE}"
            if current_reference_exists()
            else None
        ),
    }


# =========================================================
# TOGGLE
# =========================================================

@app.post(
    "/toggle",
    response_model=ToggleResponse,
)
def toggle():

    global AUTOMATION_ENABLED

    AUTOMATION_ENABLED = not AUTOMATION_ENABLED

    print("\n==============================")
    print(
        "AUTOMATION:",
        "ON" if AUTOMATION_ENABLED else "OFF"
    )
    print("==============================")

    return {
        "automation_enabled":
            AUTOMATION_ENABLED
    }


# =========================================================
# DISPLAY
# =========================================================

@app.post("/display")
def display(request: DisplayRequest):

    if not AUTOMATION_ENABLED:
        raise HTTPException(
            status_code=403,
            detail="EasyWorship automation is OFF",
        )

    text = request.command.strip()

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Command is empty",
        )

    try:

        print("\n" + "=" * 50)
        print("INCOMING COMMAND")
        print("=" * 50)
        print(text)

        # =================================================
        # 1. CHECK VERSION-ONLY COMMAND FIRST
        # =================================================

        version_correction = detect_version_only_command(
            text
        )

        if version_correction:

            print(
                f"\nVERSION-ONLY CORRECTION: "
                f"{version_correction}"
            )

            if not current_reference_exists():

                raise ValueError(
                    "There is no current Scripture "
                    "reference to change version for."
                )

            result = display_scripture(
                version=version_correction,
                book=CURRENT_BOOK,
                chapter=CURRENT_CHAPTER,
                verse=CURRENT_VERSE,
                live=request.live,
            )

            save_version(
                version_correction
            )

            return {
                "success": True,
                "action": "version_correction",
                "version":
                    version_correction,
                "reference":
                    f"{CURRENT_BOOK} "
                    f"{CURRENT_CHAPTER}:"
                    f"{CURRENT_VERSE}",
                "live":
                    request.live,
                "result":
                    result,
            }

        # =================================================
        # 2. NORMAL SCRIPTURE PARSE
        # =================================================

        parsed = parse_spoken_reference(
            text
        )

        print("\nPARSED")
        print(parsed)

        if not parsed["book"]:

            raise ValueError(
                "Scripture reference was not detected."
            )

        # =================================================
        # 3. RANGE NOT YET SUPPORTED
        # =================================================

        if parsed.get("verse_end") is not None:

            raise ValueError(
                "Verse ranges are recognized, "
                "but range automation is not implemented yet."
            )

        # =================================================
        # 4. EXPLICIT VERSION
        # =================================================

        if parsed["version"]:

            print(
                f"\nVersion requested: "
                f"{parsed['version']}"
            )

            result = display_scripture(
                version=parsed["version"],
                book=parsed["book"],
                chapter=parsed["chapter"],
                verse=parsed["verse"],
                live=request.live,
            )

            save_version(
                parsed["version"]
            )

        # =================================================
        # 5. NO VERSION
        # =================================================

        else:

            print(
                "\nNo version specified."
                "\nKeeping current EasyWorship version."
            )

            result = prepare_reference(
                book=parsed["book"],
                chapter=parsed["chapter"],
                verse=parsed["verse"],
                live=request.live,
            )

        # Save the reference after successful execution.
        save_reference(parsed)

        return {
            "success": True,
            "action": "scripture",
            "parsed": parsed,
            "current_version":
                CURRENT_VERSION,
            "live":
                request.live,
            "result":
                result,
        }

    except Exception as exc:

        print(
            "\nERROR:",
            exc,
        )

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# =========================================================
# START SERVER
# =========================================================
if __name__ == "__main__":
    import logging
    import sys
    from pathlib import Path

    BASE_DIR = Path(__file__).resolve().parent
    LOG_DIR = BASE_DIR / "logs"
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    LOG_FILE = LOG_DIR / "server.log"

    logging.basicConfig(
        filename=str(LOG_FILE),
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    logger = logging.getLogger("easyworship")

    logger.info("Starting EasyWorship FastAPI Controller")
    logger.info("Automation: ON")
    logger.info("Address: http://127.0.0.1:8000")

    threading.Thread(
        target=hotkey_listener,
        daemon=True,
    ).start()

    # IMPORTANT:
    # When packaged with --windowed, stdout/stderr may be None.
    # Disable Uvicorn's default logging configuration.
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_config=None,
        access_log=False,
    )