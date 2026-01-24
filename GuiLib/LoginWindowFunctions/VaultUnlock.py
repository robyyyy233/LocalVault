import base64
import json

import customtkinter as ctk
from tkinter import messagebox as mbox
from GuiLib.LoginWindowFunctions import VaultSetup

# for encrypting
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet


PASSWORD_MINIMUM_LENGTH = 8


# get payload
def get_payload() -> bytes:

    vault_path = VaultSetup.get_current_vault_path()

    try:
        with open(vault_path, "r") as fr:
            data = json.load(fr)
            payload = data["Payload"]
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print("Error while getting payload")
        return

    return payload


def derive_key(password: str) -> bytes:
    # get current vault
    vault_path = VaultSetup.get_current_vault_path()
    try:
        with open(vault_path, "r") as fr:
            data = json.load(fr)
            metadata = data["Metadata"]

            # everything important for the kdf
            salt = metadata["salt"]
            iter = metadata["iterations"]
            kdf = metadata["kdf"]

            salt_bytes = bytes.fromhex(salt)

    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print("Error reading vault file")
        return

    if not salt or not iter or not kdf:
        print("Cannot get information about kdf from vault")
        return

    if kdf == "pbkdf2_hmac_sha256":
        KDF = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt_bytes,
            iterations=iter,
        )

        key = base64.urlsafe_b64encode(KDF.derive(password.encode()))
        del password

        return key

    return



def encrypt(key: bytes) -> bytes:
    payload = get_payload()
    encoded_payload = base64.urlsafe_b64encode(
        json.dumps(payload, separators=(",", ":")).encode("utf-8")
    )


    #add a check here if there is already encrypted payload
    #so for fernet it starting with 'gAAAAAB'

    check_prefix = payload[:7]
    if check_prefix == "gAAAAAB":
        raise RuntimeError("ERROR! Payload is already encrypted cannot encrypt twice")


    fernet = Fernet(key)
    payload_encr = fernet.encrypt(encoded_payload)


    del payload
    del check_prefix

    # write it to the vault
    vault_path = VaultSetup.get_current_vault_path()

    try:
        with open(vault_path, "r") as fr:
            data = json.load(fr)

        data["Payload"] = payload_encr.decode()
        print(data)

        with open(vault_path, "w") as fw:
            json.dump(data, fw, indent=4)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print("Error while writing encrypted payload back to vault")


def decrypt(key: bytes) -> bytes:
    pass


def ask_sure_password() -> bool:
    answer = mbox.askyesno(
        "Confirm Password",
        "This password encrypts your vault and cannot be changed.\nLosing it means losing access forever.",
    )
    return answer


def set_master_password(Entry: ctk.CTkEntry) -> None:
    # Get password
    password = Entry.get()

    if password == "" or len(password) < PASSWORD_MINIMUM_LENGTH:
        mbox.showerror(
            "Error", f"Password must be at least {PASSWORD_MINIMUM_LENGTH} characters"
        )
        return

    # Ask with messagebox if user is sure this is the password
    answer = ask_sure_password()
    if not answer:
        return

    # create payload
    VaultSetup.create_payload()

    # encryp the tabs and passwords
    # todo: do it later don t forget!!!

    # decrypt right after login
    # show main window
    pass


if __name__ == "__main__":
    key = derive_key("1323")
    encrypt(key)
