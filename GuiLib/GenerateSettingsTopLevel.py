import customtkinter as ctk
from GuiLib.GenerateSettingsFunctions import GenerateSettingsFunctions as GSettingsFuncs


class GenerateSettingsTopLevel(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        # window configure
        self.title("Generator Settings")
        self.geometry("450x350")
        self.resizable(False, False)

        self.after(250, lambda: (self.attributes("-topmost", True), self.lift(), self.focus_force()))
        self.after(450, lambda: self.attributes("-topmost", False))

        #gets password settings and email settings
        self.password_generator_settings, self.email_generator_settings = GSettingsFuncs.get_generator_settings()

        # ── Variables ──
        self.lowercase_var = ctk.BooleanVar(value=self.password_generator_settings["lower"])
        self.uppercase_var = ctk.BooleanVar(value=self.password_generator_settings["upper"])
        self.numbers_var = ctk.BooleanVar(value=self.password_generator_settings["numbers"])
        self.symbols_var = ctk.BooleanVar(value=self.password_generator_settings["symbols"])
        self.length_var = ctk.IntVar(value=self.password_generator_settings["length"])
        self.email_numbers_var = ctk.IntVar(value=self.email_generator_settings["numbers_length"])
        self.email_domain = self.email_generator_settings["domain"]



        # main window grid
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)

        self.Main_Frame = ctk.CTkFrame(self, fg_color="#1A1C1F")
        self.Main_Frame.grid(row=0, column=0, rowspan=3, columnspan=3, sticky="nsew", padx=(0, 0), pady=(0, 0))

        # main frame grid layout
        for i in range(4):
            self.Main_Frame.grid_columnconfigure(i, weight=1)

        self.Main_Frame.grid_rowconfigure(0, weight=0)
        self.Main_Frame.grid_rowconfigure(1, weight=0)
        self.Main_Frame.grid_rowconfigure(2, weight=0)
        self.Main_Frame.grid_rowconfigure(3, weight=0)
        self.Main_Frame.grid_rowconfigure(4, weight=0)
        self.Main_Frame.grid_rowconfigure(5, weight=1)

        # ── Password Generator Section ──

        self.PasswordGenLabel = ctk.CTkLabel(self.Main_Frame, text_color="#ffffff", text="Password Generator",
                                             font=("Arial", 22), anchor="w")
        self.PasswordGenLabel.grid(row=0, column=0, columnspan=4, sticky="nw", padx=(15, 0), pady=(10, 0))

        # Separator
        self.PasswordSeparator = ctk.CTkFrame(self.Main_Frame, fg_color="#3A3D41", height=1)
        self.PasswordSeparator.grid(row=0, column=0, columnspan=4, sticky="ew", padx=(15, 15), pady=(40, 0))

        # Characters toggle frame
        self.CharsFrame = ctk.CTkFrame(self.Main_Frame, fg_color="transparent", corner_radius=0)
        self.CharsFrame.grid(row=1, column=0, columnspan=4, sticky="ew", padx=(10, 10), pady=(5, 0))

        for i in range(4):
            self.CharsFrame.columnconfigure(i, weight=1)

        # abc (lowercase)
        self.LowercaseToggle = ctk.CTkSwitch(self.CharsFrame, text="Lowercase (abc)", font=("Arial", 18),
                                             text_color="#ffffff", fg_color="#3A3D41",
                                             progress_color="#2563eb", button_color="#ffffff",
                                             button_hover_color="#e0e0e0",
                                             variable=self.lowercase_var,
                                             command=lambda: GSettingsFuncs.enforce_at_least_one(self.lowercase_var, self.uppercase_var, self.numbers_var, self.symbols_var, self.lowercase_var))
        self.LowercaseToggle.grid(row=0, column=0, padx=(5, 5), pady=(6, 6), sticky="w")

        # ABC (uppercase)
        self.UppercaseToggle = ctk.CTkSwitch(self.CharsFrame, text="Uppercase (ABC)", font=("Arial", 18),
                                             text_color="#ffffff", fg_color="#3A3D41",
                                             progress_color="#2563eb", button_color="#ffffff",
                                             button_hover_color="#e0e0e0",
                                             variable=self.uppercase_var,
                                             command=lambda: GSettingsFuncs.enforce_at_least_one(self.lowercase_var, self.uppercase_var, self.numbers_var, self.symbols_var, self.uppercase_var))
        self.UppercaseToggle.grid(row=0, column=1, padx=(5, 5), pady=(6, 6), sticky="w")

        # 123 (numbers)
        self.NumbersToggle = ctk.CTkSwitch(self.CharsFrame, text="Numbers (0-9)", font=("Arial", 18),
                                           text_color="#ffffff", fg_color="#3A3D41",
                                           progress_color="#2563eb", button_color="#ffffff",
                                           button_hover_color="#e0e0e0",
                                           variable=self.numbers_var,
                                           command=lambda: GSettingsFuncs.enforce_at_least_one(self.lowercase_var, self.uppercase_var, self.numbers_var, self.symbols_var, self.numbers_var))
        self.NumbersToggle.grid(row=1, column=0, padx=(5, 5), pady=(6, 6), sticky="w")

        # !@# (symbols)
        self.SymbolsToggle = ctk.CTkSwitch(self.CharsFrame, text="Symbols (!@#)", font=("Arial", 18),
                                           text_color="#ffffff", fg_color="#3A3D41",
                                           progress_color="#2563eb", button_color="#ffffff",
                                           button_hover_color="#e0e0e0",
                                           variable=self.symbols_var,
                                           command=lambda: GSettingsFuncs.enforce_at_least_one(self.lowercase_var, self.uppercase_var, self.numbers_var, self.symbols_var, self.symbols_var))
        self.SymbolsToggle.grid(row=1, column=1, padx=(5, 5), pady=(6, 6), sticky="w")

        # Password length slider
        self.LengthFrame = ctk.CTkFrame(self.Main_Frame, fg_color="transparent", corner_radius=0)
        self.LengthFrame.grid(row=2, column=0, columnspan=4, sticky="ew", padx=(10, 10), pady=(5, 0))

        self.LengthFrame.columnconfigure(0, weight=0)
        self.LengthFrame.columnconfigure(1, weight=1)
        self.LengthFrame.columnconfigure(2, weight=0)

        self.LengthLabel = ctk.CTkLabel(self.LengthFrame, text_color="#ffffff", text="Length",
                                        font=("Arial", 18), anchor="w")
        self.LengthLabel.grid(row=0, column=0, padx=(5, 10), pady=(3, 3), sticky="w")

        self.LengthSlider = ctk.CTkSlider(self.LengthFrame, from_=8, to=20, number_of_steps=12,
                                          fg_color="#3A3D41", progress_color="#2563eb",
                                          button_color="#ffffff", button_hover_color="#e0e0e0",
                                          variable=self.length_var,
                                          command=lambda val: self.LengthValueLabel.configure(text=str(int(val))))
        self.LengthSlider.grid(row=0, column=1, padx=(5, 10), pady=(3, 3), sticky="ew")

        self.LengthValueLabel = ctk.CTkLabel(self.LengthFrame, text_color="#ffffff",
                                             text=str(self.length_var.get()),
                                             font=("Arial", 18), width=30, anchor="e")
        self.LengthValueLabel.grid(row=0, column=2, padx=(0, 10), pady=(3, 3), sticky="e")

        # ── Email Generator Section ──

        self.EmailSectionLabel = ctk.CTkLabel(self.Main_Frame, text_color="#ffffff", text="Email Generator",
                                              font=("Arial", 22), anchor="w")
        self.EmailSectionLabel.grid(row=3, column=0, columnspan=4, sticky="nw", padx=(15, 0), pady=(12, 0))

        # Separator
        self.EmailSeparator = ctk.CTkFrame(self.Main_Frame, fg_color="#3A3D41", height=1)
        self.EmailSeparator.grid(row=3, column=0, columnspan=4, sticky="ew", padx=(15, 15), pady=(40, 0))

        # Email domain frame
        self.EmailDomainFrame = ctk.CTkFrame(self.Main_Frame, fg_color="transparent", corner_radius=0)
        self.EmailDomainFrame.grid(row=4, column=0, columnspan=4, sticky="ew", padx=(10, 10), pady=(5, 0))

        self.EmailDomainFrame.columnconfigure(0, weight=0)
        self.EmailDomainFrame.columnconfigure(1, weight=1)
        self.EmailDomainFrame.columnconfigure(2, weight=0)

        self.DomainLabel = ctk.CTkLabel(self.EmailDomainFrame, text_color="#ffffff", text="Domain",
                                        font=("Arial", 18), anchor="w")
        self.DomainLabel.grid(row=0, column=0, padx=(5, 10), pady=(3, 3), sticky="w")

        self.DomainEntry = ctk.CTkEntry(self.EmailDomainFrame, fg_color="#24272B", text_color="#ffffff",
                                        height=40, corner_radius=0, font=("Arial", 18),
                                        border_width=1, border_color="#3A3D41",
                                        placeholder_text="@gmail.com", placeholder_text_color="#474d59")
        self.DomainEntry.grid(row=0, column=1, columnspan=2, padx=(0, 10), pady=(3, 3), sticky="ew")
        
        if not self.email_domain == "":
            self.DomainEntry.insert(0, self.email_domain)

        self.EmailNumbersLabel = ctk.CTkLabel(self.EmailDomainFrame, text_color="#ffffff", text="Numbers",
                                              font=("Arial", 18), anchor="w")
        self.EmailNumbersLabel.grid(row=1, column=0, padx=(5, 10), pady=(3, 3), sticky="w")

        self.EmailNumbersSlider = ctk.CTkSlider(self.EmailDomainFrame, from_=3, to=6, number_of_steps=3,
                                                fg_color="#3A3D41", progress_color="#2563eb",
                                                button_color="#ffffff", button_hover_color="#e0e0e0",
                                                variable=self.email_numbers_var,
                                                command=lambda val: self.EmailNumbersValueLabel.configure(text=str(int(val))))
        self.EmailNumbersSlider.grid(row=1, column=1, padx=(5, 10), pady=(3, 3), sticky="ew")

        self.EmailNumbersValueLabel = ctk.CTkLabel(self.EmailDomainFrame, text_color="#ffffff",
                                                   text=str(self.email_numbers_var.get()),
                                                   font=("Arial", 18), width=30, anchor="e")
        self.EmailNumbersValueLabel.grid(row=1, column=2, padx=(0, 10), pady=(3, 3), sticky="e")

        # ── Save / Cancel buttons ──

        self.ButtonsFrame = ctk.CTkFrame(self.Main_Frame, fg_color="transparent", corner_radius=0)
        self.ButtonsFrame.grid(row=5, column=0, columnspan=4, sticky="se", padx=(10, 10), pady=(8, 8))

        self.ButtonsFrame.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.ButtonsFrame.rowconfigure(0, weight=0)

        self.SaveButton = ctk.CTkButton(self.ButtonsFrame, fg_color="#24272B", text_color="#ffffff",
                                        text="Save", corner_radius=10, width=100, height=40, font=("Arial", 20),
                                        border_width=1, border_color="#3A3D41", hover_color="#3A3D41",
                                        command=lambda: GSettingsFuncs.save_settings(self))
        self.SaveButton.grid(row=0, column=7, sticky="nse", padx=(10, 5), pady=(0, 0))

        self.CancelButton = ctk.CTkButton(self.ButtonsFrame, fg_color="#24272B", text_color="#ffffff",
                                          text="Cancel", corner_radius=10, width=100, height=40, font=("Arial", 20),
                                          border_width=1, border_color="#3A3D41", hover_color="#3A3D41",
                                          command=lambda: GSettingsFuncs.close_window(self, master))
        self.CancelButton.grid(row=0, column=6, sticky="nse", padx=(0, 0), pady=(0, 0))


if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()
    window = GenerateSettingsTopLevel(master=root)
    window.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()
