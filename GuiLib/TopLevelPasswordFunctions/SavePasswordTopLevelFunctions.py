import secrets
from datetime import datetime
from tkinter import messagebox

from GuiLib.VaultFunctions import VaultUnlock


def show_add_password_window(master):
    """Show the add password window. If already open, bring it to focus."""
    from GuiLib.SavePasswordTopLevel import AddPasswordTopLevel
    if hasattr(master, "_add_password_window") and master._add_password_window.winfo_exists():
        master._add_password_window.lift()
        master._add_password_window.focus_force()
        return
    master._add_password_window = AddPasswordTopLevel(master)


def save_password(window, master):
    """Validate, write the new entry to the vault, re-render the list, close."""
    email    = window.EmailEntry.get().strip()
    password = window.PasswordEntry.get().strip()
    site     = window.SiteEntry.get().strip()
    tab      = window.TabOptionMenu.get()
    notes    = window.OptionalTextBox.get("1.0", "end").strip()

    if not site:
        messagebox.showerror("Error", "Site cannot be empty.", parent=window)
        return
    if not password:
        messagebox.showerror("Error", "Password cannot be empty.", parent=window)
        return

    entry = {
        "id":         secrets.token_hex(6),
        "site":       site,
        "email":      email,
        "password":   password,
        "tab":        tab,
        "notes":      notes,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    master.vault_data.setdefault("Passwords", []).append(entry)

    encrypted = VaultUnlock.encrypt(master.vault_key, str(master.vault_data).encode("utf-8"))
    VaultUnlock.write_enc_data(encrypted)
    master.vault_data = VaultUnlock.decrypt(master.vault_key)

    from GuiLib.MainWindowFunctions import PasswordListFunctions
    PasswordListFunctions.render_passwords(master)

    window.destroy()


def close_window(window):
    window.destroy()


if __name__ == "__main__":
    pass
