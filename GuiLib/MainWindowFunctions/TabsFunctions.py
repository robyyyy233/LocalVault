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
    
    self.tab_buttons = []
    
    # render new tabs
    Tabs = self.vault_data.get("Tabs", [])
    for tab in Tabs:
        button = ctk.CTkButton(self.TabsFrameLocation, fg_color="#1a1c1f", text_color="#ffffff",
                                text=tab, corner_radius=6, width=170,
                                height=40, font=("Arial", 20),
                                hover_color="#31508D",
                                command=lambda t=tab: print(f"Clicked on tab: {t}"))
        button.pack(pady=5, anchor="nw")
        self.tab_buttons.append(button)
        
    Tabs = None
    del Tabs
    

def delete_tab_mode(self):
    """Toggle delete mode on/off. When on, clicking a tab deletes it."""
    self.delete_tab_mode = not self.delete_tab_mode

    if self.delete_tab_mode:
        # DELETE MODE ON — change button appearance & reconfigure tab buttons
        self.delete_tab_button.configure(fg_color="#6B1C1C", text="Cancel")

        for btn in self.tab_buttons:
            tab_name = btn.cget("text")
            
            #all buttons can be deleted beside "All"
            if not btn.cget("text") == "All":
                btn.configure(
                    fg_color="#9A3131",
                    hover_color="#B03838",
                    command=lambda t=tab_name: delete_tab(self, t),
                )
            else:
                btn.configure(command=lambda t=tab_name: messagebox.showinfo("INFO", f'"{t}" tab cannot be deleted!'))
            
    else:
        # DELETE MODE OFF — restore normal appearance & commands
        self.delete_tab_button.configure(fg_color="#9A3131", text="Delete Tab")

        for btn in self.tab_buttons:
            tab_name = btn.cget("text")
            btn.configure(
                fg_color="#1a1c1f",
                hover_color="#31508D",
                command=lambda t=tab_name: print(f"Clicked on tab: {t}"),
            )


def delete_tab(self, tab_name):
    """Delete a tab by name after confirmation."""
    confirm = messagebox.askyesno("Delete Tab", f"Are you sure you want to delete '{tab_name}'?")
    if not confirm:
        return

    if tab_name in self.vault_data.get("Tabs", []):
        self.vault_data["Tabs"].remove(tab_name)

        # Encrypt and write back
        encrypted = VaultUnlock.encrypt(self.vault_key, str(self.vault_data).encode("utf-8"))
        VaultUnlock.write_enc_data(encrypted)
        self.vault_data = VaultUnlock.decrypt(self.vault_key)

    # Exit delete mode and re-render
    self.delete_tab_mode = False
    self.delete_tab_button.configure(fg_color="#9A3131", text="Delete Tab")
    render_tabs(self)
    
        


