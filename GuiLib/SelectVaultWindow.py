from tkinter import PhotoImage

import customtkinter as ctk

from .VaultWindowFunctions import VaultSelectFunctions as VaultSelectFuncs

class SelectVaultWindow(ctk.CTkToplevel):
    def __init__(self, master=None, CurrentVaultMain=None):
        super().__init__()

        # Appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.configure(fg_color="#0f1215")

        self.title("Vault options")
        self.geometry("350x200")
        self.resizable(False, False)


        self.rowconfigure((0,1,2), weight=1)
        self.columnconfigure((0,1), weight=1)

        #Main Frame
        self.MainFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.MainFrame.grid(row=0, column=0, rowspan=3, columnspan=3, sticky="nsew", pady=(10,10), padx=(10,10))

        self.MainFrame.rowconfigure((0, 1, 2), weight=1)
        self.MainFrame.columnconfigure((0, 1), weight=1)

        #Buttons Frame
        self.ButtonsFrame = ctk.CTkFrame(self.MainFrame, fg_color="transparent", height=70)
        self.ButtonsFrame.grid(row=0, column=0, columnspan=3, sticky="new", pady=(10,10), padx=(10,10))

        #Open Vault button
        self.OpenVault = ctk.CTkButton(self.ButtonsFrame, fg_color="#2563eb", text_color="#e6edf3",
            text="Open Vault", corner_radius=10, width=125, height=50, font=("Arial", 20, "bold"),
            border_width=1, border_color="#1e3a8a", hover_color="#1d4ed8",
            command=lambda: VaultSelectFuncs.select_vault_path(self.CurrentVault))
        self.OpenVault.grid(row=0, column=0, sticky="ew", pady=(10,10), padx=(10,10))

        # Create Vault
        self.CreateVault = ctk.CTkButton(self.ButtonsFrame, fg_color="#2563eb", text_color="#e6edf3",
                                       text="Create Vault", corner_radius=10, width=125, height=50,
                                       font=("Arial", 20, "bold"),
                                       border_width=1, border_color="#1e3a8a", hover_color="#1d4ed8",
                                       command=lambda: VaultSelectFuncs.select_new_vault_path(self.CurrentVault))
        self.CreateVault.grid(row=0, column=1, sticky="ew", pady=(10, 10), padx=(20, 10))


        #Current vault Frame
        self.CurrentVaultFrame = ctk.CTkFrame(self.MainFrame, fg_color="transparent", height=70)
        self.CurrentVaultFrame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10,10), padx=(10,10))


        #Current Vault Label
        self.CurrentVault = ctk.CTkLabel(self.CurrentVaultFrame, text_color="#ffffff", text="Current Vault: ", font=("Arial", 16, "bold"))
        self.CurrentVault.grid(row=0, column=0, sticky="ew")
        VaultSelectFuncs.show_current_vault_path(self.CurrentVault, 2)

        self.attributes('-topmost', True)
        self.update()
        self.focus_force()


        self.protocol("WM_DELETE_WINDOW", lambda: VaultSelectFuncs.on_close_toplevel(self, CurrentVaultMain, master))






if __name__ == "__main__":

    #show window
    window = SelectVaultWindow()
    window.mainloop()
