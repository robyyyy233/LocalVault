import customtkinter as ctk
from GuiLib.GenerateSettingsFunctions import GenerateSettingsFunctions as GSettingsFuncs
from GuiLib.GeneratePasswordsFunctions import GeneratePasswordsFunctions as GPassFuncs


class GeneratePasswordsTopLevel(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        # window configure
        self.title("Generate")
        self.geometry("450x340")
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

        for i in range(7):
            self.Main_Frame.grid_rowconfigure(i, weight=0)
        self.Main_Frame.grid_rowconfigure(7, weight=1)

        # ── Title + Settings button ──

        self.TitleLabel = ctk.CTkLabel(self.Main_Frame, text="Generate", text_color="#ffffff",
                                       font=("Arial", 22), anchor="w")
        self.TitleLabel.grid(row=0, column=0, columnspan=3, sticky="nw", padx=(15, 0), pady=(10, 0))

        self.SettingsButton = ctk.CTkButton(self.Main_Frame, text="⚙", font=("Arial", 20),
                                            fg_color="transparent", text_color="#9a9a9a",
                                            hover_color="#3A3D41", width=40, height=40,
                                            command=lambda: GSettingsFuncs.show_generate_settings(master))
        self.SettingsButton.grid(row=0, column=3, sticky="ne", padx=(0, 8), pady=(5, 0))

        # Separator
        self.TopSeparator = ctk.CTkFrame(self.Main_Frame, fg_color="#3A3D41", height=1)
        self.TopSeparator.grid(row=0, column=0, columnspan=4, sticky="ew", padx=(15, 15), pady=(42, 0))

        # ── Password Section ──

        self.PasswordLabel = ctk.CTkLabel(self.Main_Frame, text="Password", text_color="#ffffff",
                                          font=("Arial", 18), anchor="w")
        self.PasswordLabel.grid(row=1, column=0, columnspan=4, sticky="nw", padx=(15, 0), pady=(10, 0))

        # Password entry + copy button
        self.PasswordRowFrame = ctk.CTkFrame(self.Main_Frame, fg_color="transparent")
        self.PasswordRowFrame.grid(row=2, column=0, columnspan=4, sticky="ew", padx=(10, 10), pady=(4, 0))
        self.PasswordRowFrame.columnconfigure(0, weight=1)
        self.PasswordRowFrame.columnconfigure(1, weight=0)

        self.PasswordEntry = ctk.CTkEntry(self.PasswordRowFrame, fg_color="#24272B", text_color="#ffffff",
                                          height=40, corner_radius=0, font=("Arial", 16),
                                          border_width=1, border_color="#3A3D41",
                                          placeholder_text="Click Generate...",
                                          placeholder_text_color="#474d59")
        self.PasswordEntry.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        self.CopyPasswordButton = ctk.CTkButton(self.PasswordRowFrame, text="Copy", font=("Arial", 16),
                                                fg_color="#24272B", text_color="#ffffff", corner_radius=0,
                                                width=70, height=40, border_width=1, border_color="#3A3D41",
                                                hover_color="#3A3D41",
                                                command=lambda: GPassFuncs.copy_to_clipboard(self, self.PasswordEntry.get()))
        self.CopyPasswordButton.grid(row=0, column=1, sticky="e")

        # Generate Password button
        self.GeneratePasswordButton = ctk.CTkButton(self.Main_Frame, text="Generate Password",
                                                    font=("Arial", 18), fg_color="#24272B",
                                                    text_color="#ffffff", corner_radius=0,
                                                    height=40, border_width=1, border_color="#3A3D41",
                                                    hover_color="#3A3D41",
                                                    command=lambda: GPassFuncs.generate_and_display_password(self))
        self.GeneratePasswordButton.grid(row=3, column=0, columnspan=4, sticky="ew", padx=(10, 10), pady=(5, 0))

        # ── Email Section ──

        self.EmailLabel = ctk.CTkLabel(self.Main_Frame, text="Email", text_color="#ffffff",
                                       font=("Arial", 18), anchor="w")
        self.EmailLabel.grid(row=4, column=0, columnspan=4, sticky="nw", padx=(15, 0), pady=(14, 0))

        # Email entry + copy button
        self.EmailRowFrame = ctk.CTkFrame(self.Main_Frame, fg_color="transparent")
        self.EmailRowFrame.grid(row=5, column=0, columnspan=4, sticky="ew", padx=(10, 10), pady=(4, 0))
        self.EmailRowFrame.columnconfigure(0, weight=1)
        self.EmailRowFrame.columnconfigure(1, weight=0)

        self.EmailEntry = ctk.CTkEntry(self.EmailRowFrame, fg_color="#24272B", text_color="#ffffff",
                                       height=40, corner_radius=0, font=("Arial", 16),
                                       border_width=1, border_color="#3A3D41",
                                       placeholder_text="Click Generate...",
                                       placeholder_text_color="#474d59")
        self.EmailEntry.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        self.CopyEmailButton = ctk.CTkButton(self.EmailRowFrame, text="Copy", font=("Arial", 16),
                                             fg_color="#24272B", text_color="#ffffff", corner_radius=0,
                                             width=70, height=40, border_width=1, border_color="#3A3D41",
                                             hover_color="#3A3D41",
                                             command=lambda: GPassFuncs.copy_to_clipboard(self, self.EmailEntry.get()))
        self.CopyEmailButton.grid(row=0, column=1, sticky="e")

        # Generate Email button
        self.GenerateEmailButton = ctk.CTkButton(self.Main_Frame, text="Generate Email",
                                                 font=("Arial", 18), fg_color="#24272B",
                                                 text_color="#ffffff", corner_radius=0,
                                                 height=40, border_width=1, border_color="#3A3D41",
                                                 hover_color="#3A3D41",
                                                 command=lambda: GPassFuncs.generate_and_display_email(self))
        self.GenerateEmailButton.grid(row=6, column=0, columnspan=4, sticky="ew", padx=(10, 10), pady=(5, 0))


if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()
    window = GeneratePasswordsTopLevel(master=root)
    window.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()
