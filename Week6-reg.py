import customtkinter as ctk
from tkinter import messagebox
ctk.set_appearance_mode("dark")  # โหมดสีเข้ม
ctk.set_default_color_theme("blue")  # ธีมสีฟ้า
app = ctk.CTk()
app.title("Registration Form")  # ตั้งชื่อหน้าต่าง
app.geometry("400x500")  # กำหนดขนาดหน้าต่าง

user_db = {
    "admin": "1234"
    
    }  # จำลองฐานข้อมูลผู้ใช้ด้วยพจนานุกรม

ctk.CTkLabel(app, text="Registration", font=("Arial", 22, "bold")).pack(pady=20)
ctk.CTkLabel(app, text="Username:", font=("Arial", 14)).pack()
entry_username = ctk.CTkEntry(app, placeholder_text="Enter username", width=250, height=40)
entry_username.pack(pady=5)
ctk.CTkLabel(app, text="Password:", font=("Arial", 14)).pack()
entry_password = ctk.CTkEntry(app, placeholder_text="Enter password", width=250, height=40, show="*")
entry_password.pack(pady=5)
ctk.CTkLabel(app, text="Confirm Password:", font=("Arial", 14)).pack()
entry_confirm = ctk.CTkEntry(app, placeholder_text="Confirm password", width=250, height=40, show="*")
entry_confirm.pack(pady=5)
label_result = ctk.CTkLabel(app, text="", font=("Arial", 14)).pack(pady=10)
check_var = ctk.IntVar()
ctk.CTkCheckBox(app, text="I agree to the terms and conditions", variable=check_var).pack(pady=10)
def register():
    name = entry_username.get()
    pas = entry_password.get()
    conp = entry_confirm.get()
    if name == "" or pas == "" or conp == "":
        messagebox.showerror("Error", "All fields are required.")      
        return
    elif pas != conp:
        messagebox.showerror("Error", "Passwords do not match.")
        return
    elif check_var.get() == 0:
        messagebox.showerror("Error", "You must agree to the terms and conditions.")
        return
    else:
        user_db[name] = pas
        messagebox.showinfo("Success", f"Registration successful!\nUsername: {name}\nPassword: {pas}")
    for e in [entry_username, entry_password, entry_confirm]:
        e.delete(0, "end")
    check_var.set(0)
ctk.CTkButton(app, text="Register", font=("Arial", 16), width=250, height=40, command=register).pack(pady=10)
ctk.CTkButton(app, text="Already have an account? Login", width=250, fg_color="transparent", border_width=1, command=lambda: print("Login functionality would go here")).pack(pady=5)
app.after(100, lambda: entry_username.focus_set())
app.mainloop()