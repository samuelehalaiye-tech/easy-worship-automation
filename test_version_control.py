import types
import unittest
from unittest.mock import Mock, patch

import version_control


class SetReferenceTests(unittest.TestCase):
    def test_set_reference_uses_wm_settext_for_single_field_locator(self):
        fake_box = Mock()
        fake_box.rectangle.return_value = types.SimpleNamespace(height=lambda: 24)
        fake_box.handle = 12345
        fake_box.window_text.return_value = "John 11:35"

        fake_window = Mock()

        with patch.object(version_control, "get_easyworship", return_value=fake_window), \
             patch.object(version_control, "get_locator", return_value=fake_box), \
             patch.object(version_control, "_read_locator_text", return_value="John 11:35"), \
             patch.object(version_control.time, "sleep"), \
             patch.object(version_control.pyautogui, "hotkey"), \
             patch.object(version_control.pyautogui, "write"), \
             patch.object(version_control.pyautogui, "press"), \
             patch.object(version_control.win32gui, "SendMessage", return_value=1) as send_message, \
             patch.object(version_control.win32con, "WM_SETTEXT", 0):
            result = version_control.set_reference("John", 11, 35)

        self.assertEqual(result, "John 11:35")
        send_message.assert_called_once_with(12345, 0, 0, "John 11:35")


if __name__ == "__main__":
    unittest.main()
