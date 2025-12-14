import customtkinter as ctk

from TopLevelPasswordFunctions import SavePasswordTopLevelFunctions as MainFunctions



# Todo: delete later
def generate_password(self):
    print("Password generate button is clicked")

def generate_email(self):
    print("Email generator button is clicked")

def save_password(self):
    print("Password save button is clicked")




class AddPasswordTopLevel(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        #window configurate
        self.title("New Password")
        self.geometry("410x490")
        self.resizable(False, False)

        #main window grid
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)



        self.Main_Frame : ctk.CTkFrame = ctk.CTkFrame(self, fg_color="#1A1C1F")
        self.Main_Frame.grid(row=0, column=0, rowspan=3, columnspan=3, sticky="nsew", padx=(0,0), pady=(0,0) )

        #main frame grid layout
        self.Main_Frame.grid_columnconfigure(0, weight=1)
        self.Main_Frame.grid_columnconfigure(1, weight=1)
        self.Main_Frame.grid_columnconfigure(2, weight=1)
        self.Main_Frame.grid_columnconfigure(3, weight=1)

        self.Main_Frame.grid_rowconfigure(0, weight=0)
        self.Main_Frame.grid_rowconfigure(1, weight=0)
        self.Main_Frame.grid_rowconfigure(2, weight=0)
        self.Main_Frame.grid_rowconfigure(3, weight=0)
        self.Main_Frame.grid_rowconfigure(4, weight=1)




        #Email label , entry , generate button
        self.EmailLabel = ctk.CTkLabel(self.Main_Frame, text_color="#ffffff", text="Email", font=("Arial", 22), anchor="w" )
        self.EmailLabel.grid(row=0, column=0, sticky="new", padx=(15,0), pady=(15,0))

        #Frame that holds both the entry and generate button
        self.EmailFrame = ctk.CTkFrame(self.Main_Frame, fg_color="transparent", corner_radius=0)
        self.EmailFrame.grid(row=0, column=0, columnspan=4, sticky="ew", padx=(10,10), pady=(45,0))

        self.EmailFrame.columnconfigure((0,1,2,3,4,5,6), weight=1)


        #Email entry + generate button
        self.EmailEntry = ctk.CTkEntry(self.EmailFrame, fg_color="#24272B", text_color="#ffffff", height=40,
                                          corner_radius=0, font=("Arial", 18), border_width=1,
                                          border_color="#3A3D41")
        self.EmailEntry.grid(row=0, column=0, columnspan=6, sticky="ew", padx=(0,0), pady=(0,0))

        self.EmailGenerateButton = ctk.CTkButton(self.EmailFrame, fg_color="#24272B", text_color="#ffffff",
                                                    corner_radius=0, width=40, font=("Arial", 20), text="Generate",
                                                    border_width=1, border_color="#3A3D41",hover_color="#3A3D41",
                                                    command= lambda: generate_email(self)) #todo: change later
        self.EmailGenerateButton.grid(row=0, column=6, sticky="nsew", padx=(0,0), pady=(0,0))






        #Password label, entry , generate button
        self.PasswordLabel = ctk.CTkLabel(self.Main_Frame, text_color="#ffffff", text="Password", font=("Arial", 22),
                                          anchor="w")
        self.PasswordLabel.grid(row=1, column=0, sticky="new", padx=(15, 0), pady=(15, 0))

        # Frame that holds both the entry and generate button
        self.PasswordFrame = ctk.CTkFrame(self.Main_Frame, fg_color="transparent", corner_radius=0)
        self.PasswordFrame.grid(row=1, column=0, columnspan=4, sticky="ew", padx=(10, 10), pady=(45, 0))

        self.PasswordFrame.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        # Password entry + generate button
        self.PasswordEntry = ctk.CTkEntry(self.PasswordFrame, fg_color="#24272B", text_color="#ffffff", height=40,
                                          corner_radius=0, font=("Arial", 18), border_width=1,
                                          border_color="#3A3D41")
        self.PasswordEntry.grid(row=0, column=0, columnspan=6, sticky="new", padx=(0, 0), pady=(0, 0))

        self.PasswordGenerateButton = ctk.CTkButton(self.PasswordFrame, fg_color="#24272B", text_color="#ffffff",
                                                    corner_radius=0, width=40, font=("Arial", 20), text="Generate",
                                                    border_width=1, border_color="#3A3D41",hover_color="#3A3D41",
                                                    command=lambda: generate_password(self))  # todo: change later
        self.PasswordGenerateButton.grid(row=0, column=6, sticky="nsew", padx=(0, 0), pady=(0, 0))




        #Site label , entry
        self.SiteLabel = ctk.CTkLabel(self.Main_Frame, text_color="#ffffff", text="Site", font=("Arial", 22), anchor="w" )
        self.SiteLabel.grid(row=2, column=0, sticky="new", padx=(15,0), pady=(15,0))

        #Frame that holds both the entry and generate button
        self.SiteFrame = ctk.CTkFrame(self.Main_Frame, fg_color="transparent", corner_radius=0)
        self.SiteFrame.grid(row=2, column=0, columnspan=4, sticky="ew", padx=(10,10), pady=(45,0))

        self.SiteFrame.columnconfigure((0,1,2), weight=1)

        #Site entry
        self.SiteEntry = ctk.CTkEntry(self.SiteFrame, fg_color="#24272B", text_color="#ffffff", height=40,
                                          corner_radius=0, font=("Arial", 18), border_width=1,
                                          border_color="#3A3D41")
        self.SiteEntry.grid(row=0, column=0, columnspan=3, sticky="ew", padx=(0,0), pady=(0,0))





        #Label for textbox
        self.OptionalLabel = ctk.CTkLabel(self.Main_Frame, text_color="#ffffff", text="Optional",
                                          font=("Arial", 22),anchor="w",)
        self.OptionalLabel.grid(row=3, column=0, sticky="new", padx=(15,0), pady=(15,0))

        self.OptionalFrame = ctk.CTkFrame(self.Main_Frame, fg_color="transparent", corner_radius=0)
        self.OptionalFrame.grid(row=3, column=0, columnspan=4, sticky="ew", padx=(10,10), pady=(45,0))

        for i in range(3):
            self.OptionalFrame.columnconfigure(i, weight=1)
            self.OptionalFrame.rowconfigure(i, weight=1)


        self.OptionalTextBox = ctk.CTkTextbox(self.OptionalFrame, fg_color="#24272B", text_color="#ffffff",
                                              height=100,width=250, corner_radius=0, font=("Arial", 18), border_width=1,)
        self.OptionalTextBox.grid(row=0, column=0,  columnspan=3, sticky="nsew", padx=(0,0), pady=(0,0))



        #Save and cancel button
        self.ButtonsFrame = ctk.CTkFrame(self.Main_Frame, fg_color="transparent", corner_radius=0)
        self.ButtonsFrame.grid(row=4, column=0, columnspan=4, sticky="ew", padx=(10,10), pady=(10,10))

        self.ButtonsFrame.columnconfigure((0,1,2,3,4,5,6,7), weight=1)
        self.ButtonsFrame.rowconfigure(0, weight=0)

        self.SaveButton = ctk.CTkButton(self.ButtonsFrame, fg_color="#24272B", text_color="#ffffff",
                                        text="Save", corner_radius=10, width=100,height=40, font=("Arial", 20),
                                        border_width=1, border_color="#3A3D41",hover_color="#3A3D41",
                                        command=lambda: save_password(self))
        self.SaveButton.grid(row=0, column=7, sticky="nse", padx=(0,5), pady=(0,0))

        self.CancelButton = ctk.CTkButton(self.ButtonsFrame, fg_color="#24272B", text_color="#ffffff",
                                        text="Cancel", corner_radius=10, width=100, height=40, font=("Arial", 20),
                                        border_width=1, border_color="#3A3D41", hover_color="#3A3D41",
                                        command=lambda: MainFunctions.close_window(self))
        self.CancelButton.grid(row=0, column=6, sticky="nse", padx=(25, 0), pady=(0, 0))


    #todo: add a tabs button to select tabs for sorting

    #todo: add a settings tab to main window to change generator settings (password/email)



if __name__ == "__main__":

    window = AddPasswordTopLevel()
    window.mainloop()
