from pathlib import Path
import json
import random as rnd
from tkinter import messagebox
import sys
import os
import customtkinter as ctk




def show_main_window(oldWindow) -> None:

    # import main window here to avoid circular import
    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    )
    from GuiLib.MainWindow import MainWindow

    oldWindow.destroy()
    mainWindow = MainWindow()
    mainWindow.mainloop()


# Creates the folder where the master password and the passwords are stored
def create_folder() -> str:

    Folder_Name: str = "PasswordManager"

    folder_path = Path.home() / "Documents" / Folder_Name

    if folder_path.exists():
        print(f"Folder already exists at {folder_path}")
    else:
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"Folder created at {folder_path}")

    return folder_path


def check_user_has_master_password(pathToFolder: str) -> bool:
    name = "Vault.json"
    file_path = pathToFolder / name

    if not pathToFolder.exists():
        return False

    if not file_path.exists():
        return False


    with open(file_path, "r") as vault:
        try:
            data = json.load(vault)
        except json.JSONDecodeError:
            data = {}

    if data.get("password"):
        return True
    else:
        return False


def create_master_password_file(pathToFolder: str) -> str:

    file_name: str = "Vault.json"
    file_path = pathToFolder / file_name

    if not file_path.exists():
        with open(file_path, "w") as f:
            f.write("{}")  # Create an empty JSON object
        print(f"Master password file created at {file_path}")
    else:
        print(f"Master password file already exists at {file_path}")

    return str(file_path)



def set_master_password(vault_path: str, master_password: str, loginWindow) -> None:

    with open(vault_path, "w") as vault:
        data = {"password": master_password}
        json.dump(data, vault, indent=4)
        print("Master password set successfully.")

    # show main app window
    show_main_window(loginWindow)


def show_message_box(master_entry, loginWindow, pathToFolder: str) -> None:

    # Path to the vault file
    file_name: str = "Vault.json"
    file_path = pathToFolder / file_name

    # Check if the master password entry is empty
    if master_entry.get() == "":
        messagebox.showerror(
            title="Error",
            message="Master password cannot be empty. Please enter a valid password.",
        )
        return

    # Message box with yes and no options
    result = messagebox.askyesno(
        title="Important Message",
        message="Have you saved your master password in a secure place?\nIf you lose or forget it, you will not be able to access your saved passwords.\nAre you sure you want to continue?",
    )

    # call set password function
    if result:
        set_master_password(file_path, master_entry.get(), loginWindow)


def loginUser(
    password: str, loginWindow, entry: ctk.CTkEntry, pathToFolder: str
) -> None:

    # Path to the vault file
    file_name: str = "Vault.json"
    file_path = pathToFolder / file_name

    if password == "":
        return

    with open(file_path, "r") as f:
        vaultData = json.load(f)
        vaultPassword = vaultData["password"]

    if password == vaultPassword:
        print("Login Succesful")
        show_main_window(loginWindow)
    else:
        print("Password does not match")
        entry.delete(0, "end")

        # Show error message box
        messagebox.showerror(
            "Login Failed", "Incorrect master password. Please try again."
        )


if __name__ == "__main__":
    # loginUser("")
    # check_user_has_master_password()
    pass
