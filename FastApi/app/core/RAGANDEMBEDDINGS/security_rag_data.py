security_knowledge = [
    {
        "id": "sql_injection",
        "text": "SQL Injection occurs when user input is concatenated into SQL queries. Fix by using parameterized queries, ORM bindings, or prepared statements."
    },
    {
        "id": "xss",
        "text": "Cross Site Scripting (XSS) appears when unescaped user input is rendered in HTML. Fix by sanitizing output, using HTML escaping libraries, and Content Security Policy."
    },
    {
        "id": "hardcoded_secrets",
        "text": "Never hardcode secrets, API keys, tokens, passwords. Use environment variables or secret managers."
    },
    {
        "id": "eval_code_execution",
        "text": "Dangerous functions: eval(), exec(), child_process.exec() in Node, os.system() in Python. Fix by avoiding dynamic execution."
    },
    {
        "id": "weak_crypto",
        "text": "Weak cryptography includes MD5, SHA1, hardcoded salts, insecure random generators. Use bcrypt/argon2 or strong cryptography algorithms."
    },
    {
        "id": "insecure_file_handling",
        "text": "Path traversal (../) and unsafe file writes. Validate paths and use secure file APIs."
    }
]