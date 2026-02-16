import base64
import json, ast

import customtkinter as ctk
from tkinter import messagebox as mbox
from GuiLib.VaultFunctions import VaultSetup

# for encrypting
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet, InvalidToken

import GuiLib.LoginWindowFunctions.LoginWindowSetupFunctions as SetupFuncs


PASSWORD_MINIMUM_LENGTH = 8



def get_payload() -> bytes:

    vault_path = VaultSetup.get_current_vault_path()

    try:
        with open(vault_path, "r") as fr:
            data = json.load(fr)
            payload = data["Payload"]
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print("Error while getting payload")
        return
    
    del data

    return payload


def convert_payload_to_dict(payload: str) -> dict:
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError:
            try:
                payload = ast.literal_eval(payload)
            except (ValueError, SyntaxError):
                print("Error while loading vault data")
                payload = {}
    
    return payload



def write_enc_data(enc_data:  bytes):

    vault_path = VaultSetup.get_current_vault_path()

    try:
        with open(vault_path, "r") as vr:
            data = json.load(vr)
        
        data["Payload"] = enc_data.decode()

        with open(vault_path, "w") as vw:
            json.dump(data, vw, indent=4)
        

    except (json.JSONDecodeError, FileNotFoundError):
        mbox.showerror("Error!", "Cannot write encrypted data back to the vault!")

    del data
    del enc_data
    print("Encryption writed to vault!")

        


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


def encrypt(key: bytes, data: bytes) -> bytes:
    fernet = Fernet(key)
    
    #add a check if the data is already encrypted "gAAAAAB"
    if data[:7] == b"gAAAAAB":
        print("Data is already encrypted")
        return data

    encrypted = fernet.encrypt(data)

    return encrypted



def decrypt(key: bytes) -> dict:   
    enc_payload = get_payload()
    fernet = Fernet(key)

    try:

        if not  enc_payload[:7] == "gAAAAAB":
            print("Error! the payload is not encrypted")
            return

        #decrypt
        decrypted_payload = fernet.decrypt(enc_payload).decode()
        decrypted_payload = convert_payload_to_dict(decrypted_payload)
        return decrypted_payload
    except InvalidToken:
        mbox.showerror("Error!", "Failed to decrypt due to invalid password!")
        return



def ask_sure_password() -> bool:
    answer = mbox.askyesno(
        "Confirm Password",
        "This password encrypts your vault and cannot be changed.\nLosing it means losing access forever.",
    )
    return answer


def set_master_password(password, oldWindow) -> None:

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

    #get key
    key = derive_key(password)
    
    #get payload
    payload_data = get_payload()
    payload_data = str(payload_data).encode("utf-8")

    encrypted = encrypt(key, payload_data)
    write_enc_data(encrypted)

    decrypted = decrypt(key)
    if decrypted:
        print("Master password set successfully!")
    

    SetupFuncs.show_main_window(oldWindow, key)



def login_user(password: str, oldWindow) -> None:

    key = derive_key(password)

    decrypted = decrypt(key)
    if decrypted:
        print("Login successful!")
        SetupFuncs.show_main_window(oldWindow, key)
    else:
        print("Login failed!")




if __name__ == "__main__":
    pass

    