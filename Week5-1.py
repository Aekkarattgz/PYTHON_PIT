# ระบบเมนูบนหน้าต่าง
import customtkinter as ctk
from tkinter import Menu, messagebox   # ใช้ messagebox จาก tkinter ปกติ

ctk.set_appearance_mode("dark")  # โหมดสีเข้ม
ctk.set_default_color_theme("blue")  # ธีมสีฟ้า
app = ctk.CTk()
app.title("Menu Demo")  # ตั้งชื่อหน้าต่าง
app.geometry("400x300")  # กำหนดขนาดหน้าต่าง

#create menu
menubar = Menu(app)

#menu file
file_menu = Menu(menubar, tearoff=0)
file_menu.add_command(label="New", command=lambda: messagebox.showinfo("Menu", "New File"))
file_menu.add_command(label="Open", command=lambda: messagebox.showinfo("Menu", "Open File"))
file_menu.add_separator()
file_menu.add_command(label="Exit", command=app.quit)
menubar.add_cascade(label="File", menu=file_menu)

#mene help
help_menu = Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=lambda: messagebox.showinfo("Menu", "This is a menu demo."))
menubar.add_cascade(label="Help", menu=help_menu)

app.config(menu=menubar)
app.mainloop()