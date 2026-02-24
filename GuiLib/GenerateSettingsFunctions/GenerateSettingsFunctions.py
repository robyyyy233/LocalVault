from tkinter import messagebox as mbox
import json

from GuiLib.VaultFunctions import VaultSetup


def show_generate_settings(master):
    """Show the generator settings window. If already open, bring it to focus."""
    from GuiLib.GenerateSettingsTopLevel import GenerateSettingsTopLevel
    if hasattr(master, "_gen_settings_window") and master._gen_settings_window.winfo_exists():
        master._gen_settings_window.lift()
        master._gen_settings_window.focus_force()
        return
    master._gen_settings_window = GenerateSettingsTopLevel(master)



def enforce_at_least_one(lowercase_var, uppercase_var, numbers_var, symbols_var, toggled_var):
    """Prevent turning off the last enabled toggle. Re-enables the toggled switch if all are off."""
    active = sum([lowercase_var.get(), uppercase_var.get(), numbers_var.get(), symbols_var.get()])
    if active == 0:
        mbox.showinfo("Notice", "At least one character type must be enabled for password generation.")
        toggled_var.set(True)
        

def get_generator_settings() -> tuple[dict, dict] | None:
    VaultSetup.check_generator_settings()
    vault_path = VaultSetup.get_current_vault_path()

    try:
        with open(vault_path, "r") as vr:
            data = json.load(vr)
            password_settings = data["Generator Settings"]["Password"]
            email_settings = data["Generator Settings"]["Email"]
        return password_settings, email_settings

    except FileNotFoundError:
        mbox.showerror("Error", "Vault file not found.")
    except (json.JSONDecodeError, KeyError):
        mbox.showerror("Error", "Failed to read generator settings.")

    return None, None
    
    
    
    
        


def save_settings(generator_window) -> None:
    vault_path = VaultSetup.get_current_vault_path()

    try:
        with open(vault_path, "r") as vr:
            data = json.load(vr)

        data["Generator Settings"]["Password"]["length"] = generator_window.length_var.get()
        data["Generator Settings"]["Password"]["lower"] = generator_window.lowercase_var.get()
        data["Generator Settings"]["Password"]["upper"] = generator_window.uppercase_var.get()
        data["Generator Settings"]["Password"]["numbers"] = generator_window.numbers_var.get()
        data["Generator Settings"]["Password"]["symbols"] = generator_window.symbols_var.get()

        data["Generator Settings"]["Email"]["domain"] = generator_window.DomainEntry.get()
        data["Generator Settings"]["Email"]["numbers_length"] = generator_window.email_numbers_var.get()

        with open(vault_path, "w") as vw:
            json.dump(data, vw, indent=4)
            
        mbox.showinfo("Saved!", "Setting were saved")

        generator_window.destroy()

    except (json.JSONDecodeError, FileNotFoundError):
        mbox.showerror("Error", "Something went wrong saving generator settings.")


def close_window(window):
    """Close the generator settings window."""
    window.destroy()