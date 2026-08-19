import sys
import time
import subprocess
from pathlib import Path

import requests

from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
)


API_URL = "http://127.0.0.1:8000"


# =========================================================
# PATHS
# =========================================================

if getattr(sys, "frozen", False):
    APP_DIR = Path(sys.executable).resolve().parent
else:
    APP_DIR = Path(__file__).resolve().parent


EASYWORSHIP_EXE = (
    APP_DIR
    / "EasyWorshipWorker"
    / "EasyWorshipWorker.exe"
)

MOONSHINE_EXE = (
    APP_DIR
    / "MoonshineWorker"
    / "MoonshineWorker.exe"
)


EASYWORSHIP_PYTHON = Path(
    r"C:\Users\User\AppData\Local\Programs\Python\Python313-32\python.exe"
)

MOONSHINE_PYTHON = Path(
    r"C:\Users\User\AppData\Local\Programs\Python\Python312\python.exe"
)

SERVER_PY = APP_DIR / "server.py"
MOONSHINE_PY = APP_DIR / "moonshine_bridge.py"


# =========================================================
# HELPERS
# =========================================================

def fastapi_is_running():
    try:
        response = requests.get(
            f"{API_URL}/status",
            timeout=0.8,
        )

        return response.status_code == 200

    except requests.RequestException:
        return False


def start_easyworship_worker():

    # Packaged application
    if EASYWORSHIP_EXE.exists():

        return subprocess.Popen(
            [str(EASYWORSHIP_EXE)],
            cwd=str(EASYWORSHIP_EXE.parent),
            creationflags=subprocess.CREATE_NO_WINDOW,
        )

    # Development mode
    if SERVER_PY.exists() and EASYWORSHIP_PYTHON.exists():

        return subprocess.Popen(
            [
                str(EASYWORSHIP_PYTHON),
                str(SERVER_PY),
            ],
            cwd=str(APP_DIR),
            creationflags=subprocess.CREATE_NO_WINDOW,
        )

    return None


def start_moonshine_worker():

    # Packaged application
    if MOONSHINE_EXE.exists():

        return subprocess.Popen(
            [str(MOONSHINE_EXE)],
            cwd=str(MOONSHINE_EXE.parent),
            creationflags=subprocess.CREATE_NO_WINDOW,
        )

    # Development mode
    if MOONSHINE_PY.exists() and MOONSHINE_PYTHON.exists():

        return subprocess.Popen(
            [
                str(MOONSHINE_PYTHON),
                str(MOONSHINE_PY),
            ],
            cwd=str(APP_DIR),
            creationflags=subprocess.CREATE_NO_WINDOW,
        )

    return None


def stop_process(process):

    if process is None:
        return

    if process.poll() is not None:
        return

    try:
        process.terminate()
        process.wait(timeout=5)

    except Exception:

        try:
            process.kill()
        except Exception:
            pass


# =========================================================
# GUI
# =========================================================

class EasyWorshipGUI(QWidget):

    def __init__(self):
        super().__init__()

        self.server_process = None
        self.moonshine_process = None
        self.startup_complete = False

        self.setWindowTitle(
            "EasyWorship Voice Controller"
        )

        self.setMinimumSize(
            650,
            500,
        )

        self.build_ui()

        # Start workers after GUI appears.
        QTimer.singleShot(
            300,
            self.start_system,
        )

        # Refresh status.
        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.refresh_status
        )

        self.timer.start(1000)

    # =====================================================
    # UI
    # =====================================================

    def build_ui(self):

        main_layout = QVBoxLayout()

        title = QLabel(
            "EasyWorship Voice Controller"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setStyleSheet(
            "font-size: 24px;"
            "font-weight: bold;"
            "padding: 12px;"
        )

        main_layout.addWidget(title)

        # -------------------------------------------------
        # STATUS
        # -------------------------------------------------

        status_group = QGroupBox(
            "System Status"
        )

        status_layout = QVBoxLayout()

        self.ew_status = QLabel(
            "EasyWorship: Starting..."
        )

        self.moonshine_status = QLabel(
            "Moonshine: Starting..."
        )

        self.automation_status = QLabel(
            "Automation: Starting..."
        )

        status_layout.addWidget(
            self.ew_status
        )

        status_layout.addWidget(
            self.moonshine_status
        )

        status_layout.addWidget(
            self.automation_status
        )

        status_group.setLayout(
            status_layout
        )

        main_layout.addWidget(
            status_group
        )

        # -------------------------------------------------
        # CURRENT SCRIPTURE
        # -------------------------------------------------

        scripture_group = QGroupBox(
            "Current Scripture"
        )

        scripture_layout = QVBoxLayout()

        self.current_label = QLabel(
            "No Scripture loaded"
        )

        self.current_label.setAlignment(
            Qt.AlignCenter
        )

        self.current_label.setStyleSheet(
            "font-size: 20px;"
            "font-weight: bold;"
            "padding: 15px;"
        )

        scripture_layout.addWidget(
            self.current_label
        )

        scripture_group.setLayout(
            scripture_layout
        )

        main_layout.addWidget(
            scripture_group
        )

        # -------------------------------------------------
        # MANUAL COMMAND
        # -------------------------------------------------

        command_group = QGroupBox(
            "Manual Command"
        )

        command_layout = QVBoxLayout()

        self.command_input = QLineEdit()

        self.command_input.setPlaceholderText(
            "Show John 3:16 in HCSB"
        )

        command_layout.addWidget(
            self.command_input
        )

        button_layout = QHBoxLayout()

        self.preview_button = QPushButton(
            "Preview"
        )

        self.live_button = QPushButton(
            "Display + Go Live"
        )

        self.preview_button.clicked.connect(
            self.send_preview
        )

        self.live_button.clicked.connect(
            self.send_live
        )

        button_layout.addWidget(
            self.preview_button
        )

        button_layout.addWidget(
            self.live_button
        )

        command_layout.addLayout(
            button_layout
        )

        command_group.setLayout(
            command_layout
        )

        main_layout.addWidget(
            command_group
        )

        # -------------------------------------------------
        # AUTOMATION
        # -------------------------------------------------

        self.toggle_button = QPushButton(
            "Toggle Automation"
        )

        self.toggle_button.clicked.connect(
            self.toggle_automation
        )

        main_layout.addWidget(
            self.toggle_button
        )

        # -------------------------------------------------
        # LAST COMMAND
        # -------------------------------------------------

        self.last_label = QLabel(
            "Last command: —"
        )

        self.last_label.setWordWrap(
            True
        )

        main_layout.addWidget(
            self.last_label
        )

        # -------------------------------------------------
        # MESSAGE
        # -------------------------------------------------

        self.message_label = QLabel(
            "Starting..."
        )

        self.message_label.setAlignment(
            Qt.AlignCenter
        )

        main_layout.addWidget(
            self.message_label
        )

        self.setLayout(
            main_layout
        )

    # =====================================================
    # START SYSTEM
    # =====================================================

    def start_system(self):

        self.message_label.setText(
            "Starting EasyWorship..."
        )

        # ---------------------------------------------
        # Start EasyWorship/FastAPI only if necessary
        # ---------------------------------------------

        if not fastapi_is_running():

            self.server_process = (
                start_easyworship_worker()
            )

            if self.server_process is None:

                self.message_label.setText(
                    "Could not start EasyWorship worker."
                )

                return

            # Give Uvicorn a moment.
            self.wait_for_fastapi()

        else:

            self.message_label.setText(
                "FastAPI already running."
            )

            self.start_moonshine()

    def wait_for_fastapi(self):

        attempts = 0

        while attempts < 20:

            QApplication.processEvents()

            if fastapi_is_running():

                self.message_label.setText(
                    "EasyWorship connected."
                )

                self.start_moonshine()

                return

            time.sleep(0.25)

            attempts += 1

        self.message_label.setText(
            "FastAPI did not start."
        )

    # =====================================================
    # START MOONSHINE
    # =====================================================

    def start_moonshine(self):

        self.message_label.setText(
            "Starting Moonshine..."
        )

        self.moonshine_process = (
            start_moonshine_worker()
        )

        if self.moonshine_process is None:

            self.message_label.setText(
                "Could not start Moonshine worker."
            )

            return

        self.message_label.setText(
            "Moonshine starting..."
        )

        self.startup_complete = True

    # =====================================================
    # STATUS
    # =====================================================

    def refresh_status(self):

        try:

            response = requests.get(
                f"{API_URL}/status",
                timeout=0.8,
            )

            if response.status_code != 200:

                self.ew_status.setText(
                    "EasyWorship / FastAPI: OFFLINE"
                )

                return

            status = response.json()

            self.ew_status.setText(
                "EasyWorship / FastAPI: CONNECTED"
            )

            # Actual process status.
            if (
                self.moonshine_process is not None
                and self.moonshine_process.poll()
                is None
            ):

                self.moonshine_status.setText(
                    "Moonshine: LISTENING"
                )

            else:

                self.moonshine_status.setText(
                    "Moonshine: STOPPED"
                )

            automation = status.get(
                "automation_enabled",
                False,
            )

            self.automation_status.setText(
                "Automation: "
                + (
                    "ON"
                    if automation
                    else "OFF"
                )
            )

            current_version = status.get(
                "current_version"
            )

            current_reference = status.get(
                "current_reference"
            )

            if current_reference:

                if current_version:

                    self.current_label.setText(
                        f"{current_version} — "
                        f"{current_reference}"
                    )

                else:

                    self.current_label.setText(
                        current_reference
                    )

        except requests.RequestException:

            self.ew_status.setText(
                "EasyWorship / FastAPI: OFFLINE"
            )

            self.moonshine_status.setText(
                "Moonshine: UNKNOWN"
            )

            self.automation_status.setText(
                "Automation: UNKNOWN"
            )

    # =====================================================
    # SEND COMMAND
    # =====================================================

    def send_command(self, live):

        command = (
            self.command_input.text()
            .strip()
        )

        if not command:

            self.message_label.setText(
                "Enter a command first."
            )

            return

        try:

            response = requests.post(
                f"{API_URL}/display",
                json={
                    "command": command,
                    "live": live,
                },
                timeout=120,
            )

            if response.status_code != 200:

                self.message_label.setText(
                    "ERROR: "
                    + response.text
                )

                return

            self.last_label.setText(
                f"Last command: {command}"
            )

            if live:

                self.message_label.setText(
                    "Displayed and sent Live."
                )

            else:

                self.message_label.setText(
                    "Preview prepared."
                )

            self.command_input.clear()

            self.refresh_status()

        except Exception as exc:

            self.message_label.setText(
                f"ERROR: {exc}"
            )

    def send_preview(self):
        self.send_command(
            live=False
        )

    def send_live(self):
        self.send_command(
            live=True
        )

    # =====================================================
    # AUTOMATION
    # =====================================================

    def toggle_automation(self):

        try:

            response = requests.post(
                f"{API_URL}/toggle",
                timeout=5,
            )

            response.raise_for_status()

            self.refresh_status()

        except Exception as exc:

            self.message_label.setText(
                f"ERROR: {exc}"
            )

    # =====================================================
    # CLOSE
    # =====================================================

    def closeEvent(self, event):

        self.message_label.setText(
            "Stopping workers..."
        )

        stop_process(
            self.moonshine_process
        )

        stop_process(
            self.server_process
        )

        event.accept()


# =========================================================
# MAIN
# =========================================================

def main():

    app = QApplication(
        sys.argv
    )

    window = EasyWorshipGUI()

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()