from pywinauto import Desktop, Application

WINDOW_TITLE = 'EasyWorship 2009 - Default Profile'

windows = Desktop(backend='win32').windows(title=WINDOW_TITLE)
if not windows:
    raise RuntimeError('No EasyWorship window')

win = windows[0]
app = Application(backend='win32').connect(handle=win.handle)
ew = app.window(handle=win.handle)

for i, c in enumerate(ew.children()):
    try:
        print('CHILD', i, c.class_name(), repr(c.window_text()), c.rectangle())
    except Exception as e:
        print('CHILD', i, c.class_name(), 'ERR', repr(e))

locators = [c for c in ew.descendants() if c.class_name() == 'TScriptureLocator']
print('locator count', len(locators))
for c in locators:
    try:
        print('LOCATOR', c.handle, c.rectangle(), repr(c.window_text()))
        print('CONTROL_IDS', c.control_identifiers())
    except Exception as e:
        print('LOCATOR ERR', e)

print('TREE START')
print(ew.dump_tree())
