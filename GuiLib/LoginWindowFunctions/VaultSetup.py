import os
import json
from datetime import datetime




#todo: if first time use create the vault and write the metadata inside
#todo: if second time use try to decrypt the vault if decrypt error InvalidToken show an error message box and close the app

def print_with_time(message: str) -> None:
    time = datetime.now().strftime("%H:%M:%S")
    print(f"[{time}]  {message}")


#todo: let the user chose the vault location
#todo: let him chose if the vault exists and he only selects it or create a new one




def check_vault(folder_path) -> bool:
    file_name = "Vault.dat"
    vault_location = folder_path + file_name

    if os.path.exists(vault_location):
        print_with_time("Vault already exists")
        return True
    else:
        print_with_time("Vault does not exist")
        return False



def create_vault(folder_path, salt, vault_id):

    os.makedirs(folder_path, exist_ok=True)

    file_name = "Vault.bin"
    vault_location = os.path.join(folder_path, file_name)


    data = {"Metadata": {"Magic": "PasswordManager",
                         "Version": 1,
                         "Next_ID": 1,
                         "kdf": "pbkdf2_hmac_sha256",
                         "iterations": 600_000,
                         "salt": salt,
                         "vault_id": vault_id}}


    with open(vault_location, "w") as file:
        file.write(json.dumps(data, indent=4))




if __name__ == "__main__":
    pass
