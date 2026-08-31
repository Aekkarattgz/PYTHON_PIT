import customtkinter as ctk
from tkinter import messagebox   # ใช้ messagebox จาก tkinter ปกติ

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Messagebox Demo")
app.geometry("350x250")

def show_ifo():
    messagebox.showinfo("Information", "This is an info message.")
def show_warning():
    messagebox.showwarning("Warning", "This is a warning message.")
def show_error():
    messagebox.showerror("Error", "This is an error message.")
def ask_question():
    result = messagebox.askquestion("Question", "Do you like CTK?")
    if result == "yes":
        label.configure(text="You like CTK!")
    else:
        label.configure(text="You don't like CTK.")

ctk.CTkButton(app, text="Show Info", command=show_ifo).pack(pady=10)
ctk.CTkButton(app, text="Show Warning", command=show_warning).pack(pady=10)
ctk.CTkButton(app, text="Show Error", command=show_error).pack(pady=10)
ctk.CTkButton(app, text="Ask Question", command=ask_question).pack(pady=10)


label = ctk.CTkLabel(app, text="")
label.pack(pady=10)

app.mainloop()