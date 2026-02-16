import json , ast
from pathlib import Path
import customtkinter as ctk
from tkinter import messagebox

from GuiLib.VaultFunctions import VaultUnlock as VaultUnlock



def destroy_window(self):
    self.destroy()

def show_top_level(self, TopLevel, tabsFrameLocation):
    # Check if we already created an instance
    if hasattr(self, "top_window") and self.top_window.winfo_exists():
        self.top_window.lift()
        self.top_window.focus_force()
        return

    # Create and store the instance
    self.top_window = TopLevel(self, tabsFrameLocation)
    
    
def add_tab(mainWin, tab_name, top_window):
    
    if not tab_name or tab_name.strip() == "":
        messagebox.showerror("Error", "Tab name cannot be empty.")
        return
    
    if "Tabs" not in mainWin.vault_data:
        raise KeyError("The 'Tabs' key is missing in the vault data.")

    Tabs = mainWin.vault_data["Tabs"]
    for tab in Tabs:
        if tab.lower() == tab_name.lower():
            messagebox.showerror("Error", "A tab with this name already exists.")
            return
    
    if not tab_name.istitle():
        tab_name = tab_name.title()
    
    Tabs = None
    del Tabs
    
    mainWin.vault_data["Tabs"].append(tab_name)
    
    #encrypt and write back to vault
    encrypted = VaultUnlock.encrypt(mainWin.vault_key, str(mainWin.vault_data).encode("utf-8"))
    VaultUnlock.write_enc_data(encrypted)
    mainWin.vault_data = VaultUnlock.decrypt(mainWin.vault_key)
    render_tabs(mainWin)
    
    # Close the top-level window after adding the tab
    top_window.destroy()


#render tabs
def render_tabs(self):
    
    # delete all previous tabs
    for widget in self.TabsFrameLocation.winfo_children():
        widget.destroy()
        
    
    # render new tabs
    Tabs = self.vault_data.get("Tabs", [])
    for tab in Tabs:
        button = ctk.CTkButton(self.TabsFrameLocation, fg_color="#1a1c1f", text_color="#ffffff",
                                text=tab, corner_radius=6, width=170,
                                height=40, font=("Arial", 20),
                                hover_color="#31508D",
                                command=lambda t=tab: print(f"Clicked on tab: {t}"))
        button.pack(pady=5, anchor="nw")
        self.buttons.append(button)
        
    Tabs = None
    del Tabs
    
        


