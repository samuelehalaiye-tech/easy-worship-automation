from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import keyboard
import threading

from command_parser import parse_command
from version_control import display_scripture


app = FastAPI(
    title="EasyWorship Controller",
    version="1.0.0",
)


# Global automation state
AUTOMATION_ENABLED = True


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
        toggle_automation
    )

    print("F8 = toggle automation ON/OFF")

    keyboard.wait()


class DisplayRequest(BaseModel):
    command: str
    live: bool = False


class ToggleResponse(BaseModel):
    automation_enabled: bool


@app.get("/status")
def status():
    return {
        "automation_enabled": AUTOMATION_ENABLED
    }


@app.post("/toggle", response_model=ToggleResponse)
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
        "automation_enabled": AUTOMATION_ENABLED
    }


@app.post("/display")
def display(request: DisplayRequest):

    if not AUTOMATION_ENABLED:
        raise HTTPException(
            status_code=403,
            detail="EasyWorship automation is OFF"
        )

    if not request.command.strip():
        raise HTTPException(
            status_code=400,
            detail="Command is empty"
        )

    try:
        parsed = parse_command(request.command)

        print("\n" + "=" * 50)
        print("INCOMING COMMAND")
        print("=" * 50)
        print(request.command)

        print("\nPARSED")
        print(parsed)

        if not parsed["version"]:
            raise ValueError(
                "Bible version was not detected."
            )

        if not parsed["book"]:
            raise ValueError(
                "Scripture reference was not detected."
            )

        result = display_scripture(
            version=parsed["version"],
            book=parsed["book"],
            chapter=parsed["chapter"],
            verse=parsed["verse"],
            live=request.live,
        )

        return {
            "success": True,
            "command": request.command,
            "parsed": parsed,
            "live": request.live,
            "result": result,
        }

    except Exception as exc:
        print("\nERROR:", exc)

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


if __name__ == "__main__":

    print("=" * 50)
    print("EASYWORSHIP FASTAPI CONTROLLER")
    print("=" * 50)
    print("Automation:", "ON")
    print("Address: http://127.0.0.1:8000")
    print("Docs:    http://127.0.0.1:8000/docs")
    print()
    print("F8 = Toggle automation ON/OFF")
    print("Press Ctrl+C to stop.")
    print()

    threading.Thread(
        target=hotkey_listener,
        daemon=True
    ).start()

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
    )