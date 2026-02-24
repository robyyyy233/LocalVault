import secrets
import string
from tkinter import messagebox as mbox


def _generate_password(settings: dict) -> str:
    chars = ""
    if settings.get("lower"):
        chars += string.ascii_lowercase
    if settings.get("upper"):
        chars += string.ascii_uppercase
    if settings.get("numbers"):
        chars += string.digits
    if settings.get("symbols"):
        chars += string.punctuation

    if not chars:
        return ""

    length = settings.get("length", 12)
    return "".join(secrets.choice(chars) for _ in range(length))


def _generate_email(settings: dict) -> str:
    domain = settings.get("domain", "")
    numbers_length = settings.get("numbers_length", 4)

    if not domain:
        mbox.showwarning("No Domain Set", "Go to Settings to configure the email domain.")
        return ""

    if not domain.startswith("@"):
        domain = "@" + domain

    name = "".join(secrets.choice(string.ascii_lowercase) for _ in range(6))
    numbers = "".join(secrets.choice(string.digits) for _ in range(numbers_length))

    return f"{name}{numbers}{domain}"


def generate_and_display_password(window) -> None:
    from GuiLib.GenerateSettingsFunctions import GenerateSettingsFunctions as GSettingsFuncs
    password_settings, _ = GSettingsFuncs.get_generator_settings()

    if password_settings is None:
        return

    password = _generate_password(password_settings)
    window.PasswordEntry.delete(0, "end")
    window.PasswordEntry.insert(0, password)


def generate_and_display_email(window) -> None:
    from GuiLib.GenerateSettingsFunctions import GenerateSettingsFunctions as GSettingsFuncs
    _, email_settings = GSettingsFuncs.get_generator_settings()

    if email_settings is None:
        return

    email = _generate_email(email_settings)
    if not email:
        return

    window.EmailEntry.delete(0, "end")
    window.EmailEntry.insert(0, email)


def copy_to_clipboard(window, text: str) -> None:
    if not text:
        mbox.showwarning("Nothing to Copy", "Generate something first.")
        return
    window.clipboard_clear()
    window.clipboard_append(text)
    window.update()
