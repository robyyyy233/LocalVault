# LocalVault

A local-only, offline password manager built with Python and CustomTkinter.
Your passwords never leave your machine — everything is stored and encrypted in a single vault file you control.

---

## Features

- **Master password protection** — vault is encrypted with a key derived from your master password using PBKDF2-HMAC-SHA256 (600,000 iterations) and Fernet symmetric encryption
- **Tabs** — organize passwords into custom tabs for easy browsing and filtering
- **Password storage** — save site, email, username, and password entries per tab
- **Password generator** — generate cryptographically secure passwords with configurable length, character sets (lowercase, uppercase, numbers, symbols)
- **Email alias generator** — generate random email aliases with a configurable domain and number suffix length
- **Generator settings** — configure and persist generator preferences directly inside the vault file
- **Show/hide passwords** — toggle password visibility in the login screen and entry forms
- **Vault selection** — choose where your vault file lives; the app remembers it across sessions
- **First-time setup** — automatically detects a new vault and prompts you to create a master password
- **Vault portability** — your vault is a single `.json` file you can move, back up, or copy anywhere

---

## Tech Stack

| Library | Purpose |
|---|---|
| `customtkinter` | Modern dark-themed UI |
| `cryptography` | PBKDF2 key derivation + Fernet encryption |
| `Pillow` | Image assets (logo, icons) |
| `darkdetect` | System dark/light mode detection |
| `secrets` | Cryptographically secure password generation |

---

## Getting Started

### Prerequisites

- Python 3.10+

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run

```bash
python main.py
```

---

## How It Works

1. On first launch, you select (or create) a vault file anywhere on your system.
2. If the vault is new, you set a master password (minimum 8 characters). This password is **permanent** — it cannot be changed and there is no recovery option.
3. The master password is never stored. Instead, it is used to derive an encryption key via PBKDF2-HMAC-SHA256 with a random 16-byte salt and 600,000 iterations.
4. The vault payload (tabs + passwords) is encrypted with Fernet and written back to the vault file.
5. On subsequent launches, entering the correct master password decrypts the vault and opens the main window.

> **Warning:** If you forget your master password, your vault data is unrecoverable. Keep your master password safe.

---

## Vault File Structure

```json
{
    "Metadata": {
        "Magic": "...",
        "Version": "...",
        "kdf": "pbkdf2_hmac_sha256",
        "iterations": 600000,
        "salt": "<hex>",
        "vault_id": "<hex>"
    },
    "Generator Settings": {
        "Password": 
        {   "length": 12, 
            "lower": true, 
            "upper": true, 
            "numbers": true, 
            "symbols": true },
        "Email":   
         { 
            "domain": "", 
            "numbers_length": 6 
            }
    },
    "Payload": "<fernet encrypted blob>"
}
```

---

## Version

**v1.0** — Initial release
