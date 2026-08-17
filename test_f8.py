import keyboard
import time


print("F8 TEST")
print("=======")
print("Press F8.")
print("Press Ctrl+C to quit.")


def on_f8():
    print("\n*** F8 DETECTED ***")


keyboard.add_hotkey(
    "f8",
    on_f8
)

keyboard.wait()