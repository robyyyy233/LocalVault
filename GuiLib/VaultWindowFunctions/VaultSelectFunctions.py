import json
from pathlib import Path
from tkinter import filedialog
from tkinter import messagebox
from GuiLib.LoginWindowFunctions import VaultSetup as VaultSetup



def show_current_vault_path(self):

    config_path = VaultSetup.get_config_file_path()
    with open(config_path, "r") as config_file_r:
        config = json.load(config_file_r)

    vault_path = Path(config["Vault"]["current_vault"])

    vault_path_short = Path(*vault_path.parts[-2:])

    self.CurrentVault.configure(text=f"Current Vault: ...\\{vault_path_short} ", font=("Arial", 16, "bold"))




def select_new_vault_path(self):

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
    show_current_vault_path(self)




def select_vault_path(self):

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

    show_current_vault_path(self)





if __name__ == "__main__":
    #select_new_vault_path()
    pass
