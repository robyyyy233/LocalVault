import os
import json
from datetime import datetime
import secrets
from pathlib import Path




def print_with_time(message: str) -> None:
    time = datetime.now().strftime("%H:%M:%S")
    print(f"[{time}]  {message}")

def check_first_time_use() -> bool:
    #todo: is first time use create the payload list and put the tabs inside first
    #todo: change the entry label
    pass

def get_config_file_path() -> Path:
    #get config path
    appdata_path = os.getenv("APPDATA")
    folder_path = os.path.join(appdata_path, "LocalVault")
    config_path = os.path.join(folder_path, "config.json")
    return config_path

def check_vault(folder_path) -> bool:
    file_name = "Vault.dat"
    vault_location = folder_path + file_name

    if os.path.exists(vault_location):
        print_with_time("Vault already exists")
        return True
    else:
        print_with_time("Vault does not exist")
        return False



def create_vault(vault_path: Path):

    config_path = get_config_file_path()

    #open config
    with open(config_path, "r") as config_read:
        config = json.load(config_read)
        vault_list = config["Vault"]
        vault_version: str = vault_list["vault_version"]
        vault_magic_string: str = vault_list["vault_magic_string"]


    #generate salt and vault id
    salt_bytes = secrets.token_bytes(16)
    vault_id = secrets.token_hex(16)

    salt_hex = salt_bytes.hex()

    data = {"Metadata": {"Magic": vault_magic_string,
                         "Version": vault_version,
                         "kdf": "pbkdf2_hmac_sha256",
                         "iterations": 600_000,
                         "salt": salt_hex,
                         "vault_id": vault_id}}

    with open(vault_path, "w") as file:
        file.write(json.dumps(data, indent=4))
        print(f"Created Vault : {vault_path.name}")
        print(f"Vault path: {vault_path} ")

    with open(config_path, "w") as config_write:
        config["Vault"]["current_vault"] = str(vault_path)
        json.dump(config, config_write, indent=4)




if __name__ == "__main__":
    pass
