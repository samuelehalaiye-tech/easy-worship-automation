from pywinauto import Desktop, Application
import pyautogui, time, win32gui, win32con

WINDOW_TITLE = 'EasyWorship 2009 - Default Profile'

def get_window():
    windows = Desktop(backend='win32').windows(title=WINDOW_TITLE)
    if not windows:
        raise RuntimeError('EasyWorship not found')
    w = windows[0]
    app = Application(backend='win32').connect(handle=w.handle)
    return app.window(handle=w.handle)


def probe(label, action):
    ew = get_window()
    locator = ew.child_window(class_name='TScriptureLocator').wrapper_object()
    ew.set_focus()
    time.sleep(0.4)
    rect = locator.rectangle()
    pyautogui.click(x=rect.left + 15, y=rect.top + rect.height() // 2)
    time.sleep(0.2)
    try:
        action(locator, ew)
    except Exception as exc:
        print(label, 'EXC', repr(exc))
        return
    time.sleep(0.7)
    print(label, '=>', repr(locator.window_text()))


def action_type(locator, ew):
    locator.type_keys('^a', set_foreground=True)
    time.sleep(0.1)
    locator.type_keys('John 11:35', set_foreground=True)


def action_write(locator, ew):
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pyautogui.write('John 11:35', interval=0.04)


def action_wm(locator, ew):
    win32gui.SendMessage(locator.handle, win32con.WM_SETTEXT, 0, 'John 11:35')


probe('type_keys', action_type)
probe('pyautogui_write', action_write)
probe('wm_settext', action_wm)
