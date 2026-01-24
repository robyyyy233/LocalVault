import os
import json
from datetime import datetime
import secrets
from mailbox import mbox
from pathlib import Path
import customtkinter as ctk
from customtkinter import CTkButton
from tkinter import messagebox as mbox
import base64

from GuiLib.LoginWindowFunctions import VaultUnlock as VaultUnlock


def print_with_time(message: str) -> None:
    time = datetime.now().strftime("%H:%M:%S")
    print(f"[{time}]  {message}")


def get_config_file_path() -> Path:
    # get config path
    appdata_path = os.getenv("APPDATA")
    folder_path = os.path.join(appdata_path, "LocalVault")
    config_path = os.path.join(folder_path, "config.json")
    return config_path


def get_current_vault_path() -> Path:
    config_path = get_config_file_path()
    with open(config_path, "r") as config_read:
        config = json.load(config_read)

    return config["Vault"]["current_vault"]


def check_first_time_use(Entry: ctk.CTkEntry, Button: CTkButton) -> None:
    # check if the vault has a payload
    vault_path = get_current_vault_path()
    if os.path.exists(vault_path):
        try:
            with open(vault_path, "r") as vault_read:
                data = json.load(vault_read)

            if not "Payload" in data:
                print_with_time("First time use")

                Entry.configure(placeholder_text="Create a master password")
                Button.configure(text="Set")
                Button.configure(command=lambda: VaultUnlock.set_master_password())
            else:
                print_with_time("Vault already has master password")
        except (FileNotFoundError, json.JSONDecodeError):
            print_with_time("Failed to load Vault data")
    else:
        return False


def create_vault(vault_path: Path):

    config_path = get_config_file_path()

    # open config
    with open(config_path, "r") as config_read:
        config = json.load(config_read)
        vault_list = config["Vault"]
        vault_version: str = vault_list["vault_version"]
        vault_magic_string: str = vault_list["vault_magic_string"]

    # generate salt and vault id
    salt_bytes = secrets.token_bytes(16)
    vault_id = secrets.token_hex(16)

    salt_hex = salt_bytes.hex()

    data = {
        "Metadata": {
            "Magic": vault_magic_string,
            "Version": vault_version,
            "kdf": "pbkdf2_hmac_sha256",
            "iterations": 600_000,
            "salt": salt_hex,
            "vault_id": vault_id,
        }
    }

    with open(vault_path, "w") as file:
        file.write(json.dumps(data, indent=4))
        print(f"Created Vault : {vault_path.name}")
        print(f"Vault path: {vault_path} ")

    with open(config_path, "w") as config_write:
        config["Vault"]["current_vault"] = str(vault_path)
        json.dump(config, config_write, indent=4)


def create_payload() -> None:
    current_vault_path = get_current_vault_path()

    try:
        with open(current_vault_path, "r") as current_vault_file:
            data = json.load(current_vault_file)
    except (FileNotFoundError, json.JSONDecodeError):
        mbox.showerror(
            "Error",
            "An error occurred while setting the master password.\nPlease try again.",
        )
        return

    payload = {"Tabs": ["All"], "Passwords": []}

    if "Payload" not in data:
        encoded_payload = base64.urlsafe_b64encode(
            json.dumps(payload, separators=(",", ":")).encode("utf-8")
        )
        print(encoded_payload)
        decoded_back = json.loads(
            base64.urlsafe_b64decode(encoded_payload).decode("utf-8")
        )
        print(decoded_back)

        data["Payload"] = encoded_payload.decode("utf-8")

    try:
        with open(current_vault_path, "w") as current_vault_file:
            json.dump(data, current_vault_file, indent=4)
    except (FileNotFoundError, json.JSONDecodeError):
        mbox.showerror(
            "Error",
            "An error occurred while setting the master password.\nPlease try again.",
        )
        return


if __name__ == "__main__":
    create_payload()
    
