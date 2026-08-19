import sys
sys.path.insert(0, r'C:\Users\User\Documents\easyworshi')

from speech_parser import parse_spoken_reference
from server import detect_version_only_command
from version_control import set_reference_verified


def assert_ref(raw, expected):
    parsed = parse_spoken_reference(raw)
    for key, value in expected.items():
        if parsed.get(key) != value:
            raise AssertionError(f"{raw!r}: expected {key}={value!r}, got {parsed!r}")
    print('PASS', raw)


def assert_version(raw, expected):
    got = detect_version_only_command(raw)
    if got != expected:
        raise AssertionError(f"{raw!r}: expected version {expected!r}, got {got!r}")
    print('PASS', raw)


assert_version('Actually, use ASV', 'ASV')

assert_ref('John 3:16', {'book': 'John', 'chapter': 3, 'verse': 16})
assert_ref('Job 11.35', {'book': 'Job', 'chapter': 11, 'verse': 35})
assert_ref('Job 1135', {'book': 'Job', 'chapter': 11, 'verse': 35})
assert_ref('Psalm 119:11', {'book': 'Psalm', 'chapter': 119, 'verse': 11})
assert_ref('Psalm 11911', {'book': 'Psalm', 'chapter': 119, 'verse': 11})
assert_ref('John 316', {'book': 'John', 'chapter': 3, 'verse': 16})
assert_ref('James two three', {'book': 'James', 'chapter': 2, 'verse': 3})
assert_ref('What does Joshua chapter 1 verse 2 say?', {'book': 'Joshua', 'chapter': 1, 'verse': 2})
assert_ref('First John 4:8', {'book': '1 John', 'chapter': 4, 'verse': 8})
assert_ref('First Peter 3:15', {'book': '1 Peter', 'chapter': 3, 'verse': 15})
assert_ref('No, Romans 8:28', {'book': 'Romans', 'chapter': 8, 'verse': 28})

parsed = parse_spoken_reference('hello there')
if parsed.get('book') is not None:
    raise AssertionError(f"ordinary speech unexpectedly parsed: {parsed!r}")
print('PASS ordinary speech ignored')

for ref in [
    ('John', 11, 35),
    ('Isaiah', 2, 2),
    ('Mark', 2, 2),
    ('James', 2, 3),
    ('Psalm', 119, 11),
    ('John', 3, 16),
]:
    result = set_reference_verified(ref[0], ref[1], ref[2], attempts=2)
    print(f'LIVE CHECK {ref} -> {result}')

print('ALL SOURCE REGRESSION CHECKS PASSED')
