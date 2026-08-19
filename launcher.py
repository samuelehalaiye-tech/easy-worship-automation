import subprocess
import time
from pathlib import Path
import sys


if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent


EASYWORSHIP_WORKER = (
    BASE_DIR
    / "EasyWorshipWorker"
    / "EasyWorshipWorker.exe"
)

MOONSHINE_WORKER = (
    BASE_DIR
    / "MoonshineWorker"
    / "MoonshineWorker.exe"
)


def start_worker(executable, name):
    if not executable.exists():
        raise FileNotFoundError(
            f"{name} not found:\n{executable}"
        )

    print(f"Starting {name}...")

    return subprocess.Popen(
        [str(executable)],
        cwd=str(executable.parent),
    )


def main():
    print("=" * 60)
    print("EASYWORSHIP VOICE CONTROLLER")
    print("=" * 60)

    server_process = None
    moonshine_process = None

    try:
        server_process = start_worker(
            EASYWORSHIP_WORKER,
            "EasyWorship Worker",
        )

        print("Waiting for FastAPI...")
        time.sleep(4)

        moonshine_process = start_worker(
            MOONSHINE_WORKER,
            "Moonshine Worker",
        )

        print()
        print("=" * 60)
        print("SYSTEM STARTED")
        print("=" * 60)
        print(
            "EasyWorship PID:",
            server_process.pid,
        )
        print(
            "Moonshine PID:",
            moonshine_process.pid,
        )
        print()
        print("Press Ctrl+C to stop everything.")

        while True:
            time.sleep(1)

            if server_process.poll() is not None:
                print("EasyWorship Worker stopped.")
                break

            if moonshine_process.poll() is not None:
                print("Moonshine Worker stopped.")
                break

    except KeyboardInterrupt:
        print("\nStopping...")

    except Exception as exc:
        print("\nSTARTUP ERROR:")
        print(exc)

    finally:
        for process in (
            moonshine_process,
            server_process,
        ):
            if process is not None and process.poll() is None:
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except Exception:
                    try:
                        process.kill()
                    except Exception:
                        pass

        print("System stopped.")


if __name__ == "__main__":
    main()