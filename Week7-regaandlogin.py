import customtkinter as ctk
from tkinter import messagebox   # ใช้ messagebox จาก tkinter ปกติ
ctk.set_appearance_mode("dark")  # โหมดสีเข้ม
ctk.set_default_color_theme("blue")  # ธีมสีฟ้า
app = ctk.CTk()
app.title("Login Form")
app.geometry("400x380")

user_db = {
    "admin": "1234"
}

def show_frame(frame):
    frame.tkraise()

for f in (ctk.CTkFrame, ):
    pass

frame_login    = ctk.CTkFrame(app)
frame_register = ctk.CTkFrame(app)
frame_home     = ctk.CTkFrame(app)

for frame in (frame_login, frame_register, frame_home):
    frame.place(relwidth=1, relheight=1)
# ==========================================
# หน้าที่ 1 — LOGIN
# ==========================================    
ctk.CTkLabel(frame_login, text="Login", font=("Arial", 22, "bold")).pack(pady=20)
ctk.CTkLabel(frame_login, text="Username:", font=("Arial", 22, "bold")).pack(pady=5)
entry_login_user = ctk.CTkEntry(frame_login, placeholder_text="Enter username", width=250, height=40)
entry_login_user.pack(pady=5)
ctk.CTkLabel(frame_login, text="Password:", font=("Arial", 22, "bold")).pack(pady=5)
entry_login_pass = ctk.CTkEntry(frame_login, placeholder_text="Enter password", width=250, height=40, show="*")
entry_login_pass.pack(pady=5)
label_login_msg = ctk.CTkLabel(frame_login, text="", font=("Arial", 14))
label_login_msg.pack(pady=10)
def login():
    user = entry_login_user.get().strip()
    pas = entry_login_pass.get().strip()
    if user == "" or pas == "":
        messagebox.showerror("Error", "All fields are required.")
        label_login_msg.configure(text="Please enter both username and password.", text_color="red")
        return
    elif user in user_db and user_db[user] == pas:
        label_login_msg.configure(text="Login successful!", text_color="green")
        entry_login_user.delete(0, "end")
        entry_login_pass.delete(0, "end")   
        messagebox.showinfo("Welcome", f"Welcome back, {user}!")
        show_frame(frame_home)
    else:
        label_login_msg.configure(text="Invalid username or password.", text_color="red")
        messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")
        
ctk.CTkButton(frame_login, text="Login", font=("Arial", 16), width=250, height=40, command=login).pack(pady=10)
ctk.CTkButton(frame_login, text="Don't have an account? Register", width=250, fg_color="transparent", border_width=1, command=lambda: show_frame(frame_register)).pack(pady=5)
# ==========================================
# หน้าที่ 2 — REGISTER
# ==========================================
ctk.CTkLabel(frame_register, text="Registration", font=("Arial", 22, "bold")).pack(pady=20)
ctk.CTkLabel(frame_register, text="Username:", font=("Arial", 14)).pack()
entry_reg_user = ctk.CTkEntry(frame_register, placeholder_text="Enter username", width=250, height=40)
entry_reg_user.pack(pady=5)
ctk.CTkLabel(frame_register, text="Password:", font=("Arial", 14)).pack()
entry_reg_pass = ctk.CTkEntry(frame_register, placeholder_text="Enter password", width=250, height=40, show="*")
entry_reg_pass.pack(pady=5)
ctk.CTkLabel(frame_register, text="Confirm Password:", font=("Arial", 14)).pack()
entry_reg_confirm = ctk.CTkEntry(frame_register, placeholder_text="Confirm password", width=250, height=40, show="*")
entry_reg_confirm.pack(pady=5)
label_reg_msg = ctk.CTkLabel(frame_register, text="", font=("Arial", 14))
label_reg_msg.pack(pady=10)
check_var = ctk.IntVar()
ctk.CTkCheckBox(frame_register, text="I agree to the terms and conditions", variable=check_var).pack(pady=10)
def register():
    user = entry_reg_user.get().strip()
    pas = entry_reg_pass.get().strip()
    conp = entry_reg_confirm.get().strip()
    if user == "" or pas == "" or conp == "":
        messagebox.showerror("Error", "All fields are required.")
        entry_reg_user.delete(0, "end")
        entry_reg_pass.delete(0, "end")
        entry_reg_confirm.delete(0, "end")
        check_var.set(0)
        label_reg_msg.configure(text="Please fill in all fields.", text_color="red")        
        return
    elif user in user_db:
        messagebox.showerror("Error", "Username already exists.")
        entry_reg_user.delete(0, "end")
        entry_reg_pass.delete(0, "end")
        entry_reg_confirm.delete(0, "end")
        check_var.set(0)
        return
    elif pas != conp:
        messagebox.showerror("Error", "Passwords do not match.")
        entry_reg_user.delete(0, "end")
        entry_reg_pass.delete(0, "end")
        entry_reg_confirm.delete(0, "end")
        check_var.set(0)
        return
    elif check_var.get() == 0:
        messagebox.showerror("Error", "You must agree to the terms and conditions.")
        entry_reg_user.delete(0, "end")
        entry_reg_pass.delete(0, "end")
        entry_reg_confirm.delete(0, "end")
        check_var.set(0)
        return
    else:
        user_db[user] = pas
        messagebox.showinfo("Success", f"Registration successful!\nUsername: {user}\nPassword: {pas}")
        entry_reg_user.delete(0, "end")
        entry_reg_pass.delete(0, "end")
        entry_reg_confirm.delete(0, "end")
        check_var.set(0)
        show_frame(frame_login)
        lambda: entry_login_user.focus_set()
ctk.CTkButton(frame_register, text="Register", font=("Arial", 16), width=250, height=40, command=register).pack(pady=10)
ctk.CTkButton(frame_register, text="Already have an account? Login", width=250, fg_color="transparent", border_width=1, command=lambda: show_frame(frame_login)).pack(pady=5)



show_frame(frame_login)
app.after(100, lambda: entry_login_user.focus_set())
app.mainloop()
