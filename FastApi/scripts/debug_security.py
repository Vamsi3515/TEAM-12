import asyncio, json, pprint
from pathlib import Path
from app.core.security_agent import analyze_code_security
p = Path('tests/fixtures/security_test_cases.json')
cases = json.loads(p.read_text())
idx = 11
code = cases[idx]['code']
print('--- CODE ---')
print(code)
print('\n--- ANALYSIS ---')
res = asyncio.run(analyze_code_security(code, language='python'))
pprint.pprint(res)
