import json
from pathlib import Path
from tkinter import filedialog
from tkinter import messagebox
import os

from customtkinter import CTkLabel

from GuiLib.LoginWindowFunctions import VaultSetup as VaultSetup



def show_current_vault_path(Label : CTkLabel, parts) -> None:

    config_path = VaultSetup.get_config_file_path()
    with open(config_path, "r") as config_file_r:
        config = json.load(config_file_r)

    vault_path = Path(config["Vault"]["current_vault"])

    vault_path_short = Path(*vault_path.parts[-parts:])

    vault_path = str(vault_path)

    if vault_path != "None":
        Label.configure(text=f"Current Vault: ...\\{vault_path_short} ", font=("Arial", 16, "bold"))
    else:
        Label.configure(text=f"Current Vault: {vault_path_short} ", font=("Arial", 16, "bold"))






def select_new_vault_path(Label: CTkLabel) -> None:

    #ask the user for the location of the vault
    full_path = filedialog.asksaveasfilename(
        initialdir=Path.home() / "Documents",
        defaultextension=".json",
        filetypes=[("Json files", "*.json")],
    )

    vault_path = Path(full_path)

    if not vault_path.suffix == ".json":
        vault_path = vault_path.with_suffix(".json")


    VaultSetup.create_vault(vault_path)
    show_current_vault_path(Label, 2)




def select_vault_path(Label: CTkLabel) -> None:

    #Let user chose file
    full_path = filedialog.askopenfilename(
        initialdir=Path.home() / "Documents",
        defaultextension=".json",
        filetypes=[("Json files", "*.json")],
    )

    #try to open file selected
    try:
        with open(full_path, "r") as vault_file:
            vault_content = json.load(vault_file)
    except (FileNotFoundError, PermissionError, json.JSONDecodeError):
        messagebox.showerror("Error!", "File not found or not readable")

    config_path = VaultSetup.get_config_file_path()

    #open config file
    with open(config_path, "r") as config_file_r:
        config = json.load(config_file_r)

    #check if the file has metadata
    magic = None
    if isinstance(vault_content, dict):
        meta = vault_content.get("Metadata")
        if isinstance(meta, dict):
            magic = meta.get("Magic")

    #check magic string
    if config["Vault"]["vault_magic_string"] != magic:
        messagebox.showerror("Error!", "File is not a vault. Please try again!")
        return

    #write the path back to config
    with open (config_path, "w") as config_file_w:
        config["Vault"]["current_vault"] = str(full_path)
        json.dump(config, config_file_w, indent=4)

    show_current_vault_path(Label, 2)





def on_close_toplevel(self, Label: CTkLabel) -> None:
    self.destroy()
    show_current_vault_path(Label, 3)


def vault_not_in_saved_location() -> None:\
    messagebox.showerror("Error!", "Vault not in the saved location!\n "
                                   "Please select the new location!")


def check_current_vault_available() -> bool:
    config_path = VaultSetup.get_config_file_path()

    with open(config_path, "r") as config_file_r:
        config = json.load(config_file_r)
        config_vault = config["Vault"]
        current_vault =  config_vault["current_vault"]
        magic_string = config_vault["vault_magic_string"]

    current_vault = Path(current_vault)

    #check if it's still there
    if current_vault != None:
        if os.path.exists(current_vault) and os.path.isfile(current_vault):
            try:
                with open(current_vault, "r") as vault_file:
                    vault = json.load(vault_file)
                    magic = vault["Metadata"]["Magic"]

                if magic == magic_string:
                    return True
                else:
                    return False

            except (FileNotFoundError, PermissionError, json.JSONDecodeError):
                print("Vault not in the location saved!")
                vault_not_in_saved_location()
                return False
        else:
            print("Vault not in the location saved!")
            vault_not_in_saved_location()
            return False
    else:
        return False




if __name__ == "__main__":
    #select_new_vault_path()
    pass
