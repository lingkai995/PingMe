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

# Surge's JSCore rejects top-level `return;` statements.
up = up.replace("      done();\n      return;", "      done();")

# Only notify on first capture or when stable capture content actually changes.
up = up.replace("const ckKey = 'pingme_capture_v3';", "const ckKey = 'pingme_capture_v3';\nconst ckHashKey = 'pingme_capture_hash_v1';")
up = up.replace(
    "  store.write(JSON.stringify(capture), ckKey);\n  const keys = Object.keys(capture.paramsRaw).filter(k => k !== 'sign').join(', ');\n  notifyDone('✅ 参数抓取成功', `已保存请求头+参数`);",
    "  const stableCapture = {\n    paramsRaw: Object.fromEntries(Object.entries(capture.paramsRaw || {}).filter(([k]) => !['sign', 'signDate'].includes(k))),\n    headers: {\n      'User-Agent': capture.headers?.['User-Agent'] || capture.headers?.['user-agent'] || '',\n      'Authorization': capture.headers?.['Authorization'] || capture.headers?.['authorization'] || '',\n      'Cookie': capture.headers?.['Cookie'] || capture.headers?.['cookie'] || ''\n    }\n  };\n  const captureJson = JSON.stringify(capture);\n  const captureHash = MD5(stableStringify(stableCapture));\n  const prevHash = store.read(ckHashKey);\n  store.write(captureJson, ckKey);\n  store.write(captureHash, ckHashKey);\n  if (prevHash !== captureHash) notifyDone('✅ 参数抓取成功', prevHash ? '检测到参数变化，已更新保存' : '已保存请求头+参数');"
)

out.write_text(pre + '\n' + up, encoding='utf-8')
print(f'Wrote {out}')
