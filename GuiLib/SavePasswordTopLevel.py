import customtkinter as ctk

from GuiLib.TopLevelPasswordFunctions import SavePasswordTopLevelFunctions as MainFunctions
from GuiLib.GeneratePasswordsFunctions import GeneratePasswordsFunctions as GPassFuncs
from GuiLib.GenerateSettingsFunctions import GenerateSettingsFunctions as GSettingsFuncs




class AddPasswordTopLevel(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("New Password")
        self.geometry("410x580")
        self.resizable(False, False)

        self.after(250, lambda: (self.attributes("-topmost", True), self.lift(), self.focus_force()))
        self.after(450, lambda: self.attributes("-topmost", False))

        # main window grid
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)

        self.Main_Frame = ctk.CTkFrame(self, fg_color="#1A1C1F")
        self.Main_Frame.grid(row=0, column=0, rowspan=3, columnspan=3, sticky="nsew")

        for i in range(4):
            self.Main_Frame.grid_columnconfigure(i, weight=1)

        for i in range(5):
            self.Main_Frame.grid_rowconfigure(i, weight=0)
        self.Main_Frame.grid_rowconfigure(5, weight=1)


        # ── Email ──
        self.EmailLabel = ctk.CTkLabel(self.Main_Frame, text_color="#ffffff", text="Email",
                                       font=("Arial", 22), anchor="w")
        self.EmailLabel.grid(row=0, column=0, sticky="new", padx=(15, 0), pady=(15, 0))

        self.SettingsButton = ctk.CTkButton(self.Main_Frame, text="⚙", font=("Arial", 20),
                                            fg_color="transparent", text_color="#9a9a9a",
                                            hover_color="#3A3D41", width=40, height=40,
                                            command=lambda: GSettingsFuncs.show_generate_settings(master))
        self.SettingsButton.grid(row=0, column=3, sticky="ne", padx=(0, 8), pady=(5, 0))

        self.EmailFrame = ctk.CTkFrame(self.Main_Frame, fg_color="transparent", corner_radius=0)
        self.EmailFrame.grid(row=0, column=0, columnspan=4, sticky="ew", padx=(10, 10), pady=(45, 0))
        self.EmailFrame.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        self.EmailEntry = ctk.CTkEntry(self.EmailFrame, fg_color="#24272B", text_color="#ffffff", height=40,
                                       corner_radius=0, font=("Arial", 18), border_width=1, border_color="#3A3D41")
        self.EmailEntry.grid(row=0, column=0, columnspan=6, sticky="ew")

        self.EmailGenerateButton = ctk.CTkButton(self.EmailFrame, fg_color="#24272B", text_color="#ffffff",
                                                 corner_radius=0, width=40, font=("Arial", 20), text="Generate",
                                                 border_width=1, border_color="#3A3D41", hover_color="#3A3D41",
                                                 command=lambda: GPassFuncs.generate_and_display_email(self))
        self.EmailGenerateButton.grid(row=0, column=6, sticky="nsew")


        # ── Password ──
        self.PasswordLabel = ctk.CTkLabel(self.Main_Frame, text_color="#ffffff", text="Password",
                                          font=("Arial", 22), anchor="w")
        self.PasswordLabel.grid(row=1, column=0, sticky="new", padx=(15, 0), pady=(15, 0))

        self.PasswordFrame = ctk.CTkFrame(self.Main_Frame, fg_color="transparent", corner_radius=0)
        self.PasswordFrame.grid(row=1, column=0, columnspan=4, sticky="ew", padx=(10, 10), pady=(45, 0))
        self.PasswordFrame.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        self.PasswordEntry = ctk.CTkEntry(self.PasswordFrame, fg_color="#24272B", text_color="#ffffff", height=40,
                                          corner_radius=0, font=("Arial", 18), border_width=1, border_color="#3A3D41")
        self.PasswordEntry.grid(row=0, column=0, columnspan=6, sticky="ew")

        self.PasswordGenerateButton = ctk.CTkButton(self.PasswordFrame, fg_color="#24272B", text_color="#ffffff",
                                                    corner_radius=0, width=40, font=("Arial", 20), text="Generate",
                                                    border_width=1, border_color="#3A3D41", hover_color="#3A3D41",
                                                    command=lambda: GPassFuncs.generate_and_display_password(self))
        self.PasswordGenerateButton.grid(row=0, column=6, sticky="nsew")


        # ── Site ──
        self.SiteLabel = ctk.CTkLabel(self.Main_Frame, text_color="#ffffff", text="Site",
                                      font=("Arial", 22), anchor="w")
        self.SiteLabel.grid(row=2, column=0, sticky="new", padx=(15, 0), pady=(15, 0))

        self.SiteFrame = ctk.CTkFrame(self.Main_Frame, fg_color="transparent", corner_radius=0)
        self.SiteFrame.grid(row=2, column=0, columnspan=4, sticky="ew", padx=(10, 10), pady=(45, 0))
        self.SiteFrame.columnconfigure((0, 1, 2), weight=1)

        self.SiteEntry = ctk.CTkEntry(self.SiteFrame, fg_color="#24272B", text_color="#ffffff", height=40,
                                      corner_radius=0, font=("Arial", 18), border_width=1, border_color="#3A3D41")
        self.SiteEntry.grid(row=0, column=0, columnspan=3, sticky="ew")


        # ── Tab selector ──
        self.TabLabel = ctk.CTkLabel(self.Main_Frame, text_color="#ffffff", text="Tab",
                                     font=("Arial", 22), anchor="w")
        self.TabLabel.grid(row=3, column=0, sticky="new", padx=(15, 0), pady=(15, 0))

        all_tabs = master.vault_data.get("Tabs", []) if master and hasattr(master, "vault_data") else []
        tabs = [t for t in all_tabs if t != "All"] or ["All"]

        self.TabOptionMenu = ctk.CTkOptionMenu(self.Main_Frame, values=tabs,
                                               fg_color="#24272B", text_color="#ffffff",
                                               button_color="#3A3D41", button_hover_color="#4A4D51",
                                               dropdown_fg_color="#24272B", dropdown_text_color="#ffffff",
                                               dropdown_hover_color="#3A3D41",
                                               font=("Arial", 18), height=40, corner_radius=0)
        self.TabOptionMenu.grid(row=3, column=0, columnspan=4, sticky="ew", padx=(10, 10), pady=(45, 0))
        self.TabOptionMenu.set(tabs[0])


        # ── Optional ──
        self.OptionalLabel = ctk.CTkLabel(self.Main_Frame, text_color="#ffffff", text="Optional",
                                          font=("Arial", 22), anchor="w")
        self.OptionalLabel.grid(row=4, column=0, sticky="new", padx=(15, 0), pady=(15, 0))

        self.OptionalFrame = ctk.CTkFrame(self.Main_Frame, fg_color="transparent", corner_radius=0)
        self.OptionalFrame.grid(row=4, column=0, columnspan=4, sticky="ew", padx=(10, 10), pady=(45, 0))
        for i in range(3):
            self.OptionalFrame.columnconfigure(i, weight=1)
            self.OptionalFrame.rowconfigure(i, weight=1)

        self.OptionalTextBox = ctk.CTkTextbox(self.OptionalFrame, fg_color="#24272B", text_color="#ffffff",
                                              height=80, width=250, corner_radius=0, font=("Arial", 18),
                                              border_width=1)
        self.OptionalTextBox.grid(row=0, column=0, columnspan=3, sticky="nsew")


        # ── Save / Cancel ──
        self.ButtonsFrame = ctk.CTkFrame(self.Main_Frame, fg_color="transparent", corner_radius=0)
        self.ButtonsFrame.grid(row=5, column=0, columnspan=4, sticky="ew", padx=(10, 10), pady=(10, 10))
        self.ButtonsFrame.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        self.SaveButton = ctk.CTkButton(self.ButtonsFrame, fg_color="#24272B", text_color="#ffffff",
                                        text="Save", corner_radius=10, width=100, height=40, font=("Arial", 20),
                                        border_width=1, border_color="#3A3D41", hover_color="#3A3D41",
                                        command=lambda: MainFunctions.save_password(self, master))
        self.SaveButton.grid(row=0, column=7, sticky="nse", padx=(0, 5))

        self.CancelButton = ctk.CTkButton(self.ButtonsFrame, fg_color="#24272B", text_color="#ffffff",
                                          text="Cancel", corner_radius=10, width=100, height=40, font=("Arial", 20),
                                          border_width=1, border_color="#3A3D41", hover_color="#3A3D41",
                                          command=lambda: MainFunctions.close_window(self))
        self.CancelButton.grid(row=0, column=6, sticky="nse", padx=(25, 0))


if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()
    window = AddPasswordTopLevel(master=root)
    window.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()
