#!/usr/bin/env python3
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
upstream = repo / 'upstream' / 'PingMe.js'
prefix = repo / 'scripts' / 'wrapper_prefix.js'
out = repo / 'PingMe.surge.js'

up = upstream.read_text(encoding='utf-8')
pre = prefix.read_text(encoding='utf-8')

replacements = {
    '$prefs.setValueForKey': 'store.write',
    '$prefs.valueForKey': 'store.read',
    '$notify': 'notify',
    '$done': 'done',
    '$task.fetch': 'requestGet',
}

for old, new in replacements.items():
    up = up.replace(old, new)

out.write_text(pre + '\n' + up, encoding='utf-8')
print(f'Wrote {out}')
