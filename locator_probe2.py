from pywinauto import Desktop, Application
import pyautogui, time, win32gui, win32con

WINDOW_TITLE = 'EasyWorship 2009 - Default Profile'

def main():
    windows = Desktop(backend='win32').windows(title=WINDOW_TITLE)
    if not windows:
        raise RuntimeError('EasyWorship not found')
    handle = windows[0].handle
    app = Application(backend='win32').connect(handle=handle)
    ew = app.window(handle=handle)
    locator = ew.child_window(class_name='TScriptureLocator').wrapper_object()
    print('initial', repr(locator.window_text()))

    ew.set_focus()
    time.sleep(0.5)
    rect = locator.rectangle()
    pyautogui.click(x=rect.left + 15, y=rect.top + rect.height() // 2)
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    win32gui.SendMessage(locator.handle, win32con.WM_SETTEXT, 0, 'John 11:35')
    time.sleep(0.8)
    print('after wm_settext', repr(locator.window_text()))

    ew.set_focus()
    time.sleep(0.5)
    rect = locator.rectangle()
    pyautogui.click(x=rect.left + 15, y=rect.top + rect.height() // 2)
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.write('Genesis 1:1', interval=0.05)
    time.sleep(0.8)
    print('after pyautogui write', repr(locator.window_text()))

    ew.set_focus()
    time.sleep(0.5)
    rect = locator.rectangle()
    pyautogui.click(x=rect.left + 15, y=rect.top + rect.height() // 2)
    time.sleep(0.2)
    pyautogui.write('John', interval=0.05)
    time.sleep(0.4)
    pyautogui.press('right')
    time.sleep(0.3)
    pyautogui.write('11:35', interval=0.05)
    time.sleep(0.8)
    print('after right-sequence', repr(locator.window_text()))

main()
