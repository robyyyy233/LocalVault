import customtkinter as ctk
from tkinter import messagebox as mbox
from GuiLib.LoginWindowFunctions import VaultSetup

#for encrypting
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


PASSWORD_MINIMUM_LENGTH = 8

#todo: later
def derive_key(password: str) -> bytes:
    #get current salt
    #derivate the key
    #return key
    pass

def encrypt(message: bytes, key: bytes) -> bytes:
    pass

def decrypt(message: bytes, key: bytes) -> bytes:
    pass



def ask_sure_password() -> bool:
    answer = mbox.askyesno("Confirm Password", "This password encrypts your vault and cannot be changed.\nLosing it means losing access forever.")
    return answer


def set_master_password(Entry: ctk.CTkEntry) -> None:
    #Get password
    password = Entry.get()

    if password == "" or len(password) < PASSWORD_MINIMUM_LENGTH:
        mbox.showerror("Error", f"Password must be at least {PASSWORD_MINIMUM_LENGTH} characters")
        return

    #Ask with messagebox if user is sure this is the password
    answer = ask_sure_password()
    if not answer:
        return

   #create payload
    VaultSetup.create_payload()

    #encryp the tabs and passwords
    #decrypt right after login
    #show main window
    pass


if __name__ == "__main__":
    ask_sure_password()