import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Login Form")
app.geometry("400x380")

user_db = {
    "admin": "1234",
    "student01": "abcd"
}

ctk.CTkLabel(app, text="Login", font=("Arial", 22, "bold")).pack(pady=20)

ctk.CTkLabel(app, text="Username:", font=("Arial", 14)).pack()
entry_username = ctk.CTkEntry(app, placeholder_text="Enter username", width=250, height=40)
entry_username.pack(pady=5)

ctk.CTkLabel(app, text="Password:", font=("Arial", 14)).pack()
entry_password = ctk.CTkEntry(app, placeholder_text="Enter password", width=250, height=40, show="*")
entry_password.pack(pady=5)

# แยก 2 บรรทัด เพื่อให้ label_result เก็บ object จริง ไม่ใช่ None
label_result = ctk.CTkLabel(app, text="", font=("Arial", 14))
label_result.pack(pady=10)

def login():
    username = entry_username.get()
    password = entry_password.get()

    if username == "" or password == "":
        label_result.configure(text="กรุณากรอกข้อมูลให้ครบ", text_color="orange")
        return

    if username not in user_db:
        label_result.configure(text="ไม่พบผู้ใช้งาน", text_color="red")
        return

    if user_db[username] != password:
        label_result.configure(text="Password ไม่ถูกต้อง", text_color="red")
        return

    label_result.configure(text=f"ยินดีต้อนรับ {username}", text_color="green")

ctk.CTkButton(app, text="Login", font=("Arial", 16), width=250, height=40, command=login).pack(pady=10)
app.after(100, lambda: entry_username.focus_set())
app.mainloop()