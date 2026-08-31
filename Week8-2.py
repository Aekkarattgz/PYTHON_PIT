import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Login Form")
app.geometry("400x520")
app.resizable(False, False)

user_db = {"admin": "1234"}

def show_frame(frame):
    frame.tkraise()

frame_login    = ctk.CTkFrame(app)
frame_register = ctk.CTkFrame(app)
frame_Cal      = ctk.CTkFrame(app)

for frame in (frame_login, frame_register, frame_Cal):
    frame.place(relwidth=1, relheight=1)

# ==========================================
# หน้าที่ 1 — LOGIN
# ==========================================
ctk.CTkLabel(frame_login, text="Login", font=("Arial", 22, "bold")).pack(pady=20)
ctk.CTkLabel(frame_login, text="Username:", font=("Arial", 14)).pack()
entry_login_user = ctk.CTkEntry(frame_login, placeholder_text="Enter username", width=250, height=40)
entry_login_user.pack(pady=5)
ctk.CTkLabel(frame_login, text="Password:", font=("Arial", 14)).pack()
entry_login_pass = ctk.CTkEntry(frame_login, placeholder_text="Enter password", width=250, height=40, show="*")
entry_login_pass.pack(pady=5)

label_login_msg = ctk.CTkLabel(frame_login, text="", font=("Arial", 14))
label_login_msg.pack(pady=10)

def login():
    user = entry_login_user.get().strip()
    pas  = entry_login_pass.get().strip()
    if user == "" or pas == "":
        label_login_msg.configure(text="⚠️ Please enter both username and password.", text_color="orange")
        return
    if user in user_db and user_db[user] == pas:
        label_login_msg.configure(text="")
        entry_login_user.delete(0, "end")
        entry_login_pass.delete(0, "end")
        messagebox.showinfo("Welcome", f"Welcome back, {user}!")
        go_to_calc()
    else:
        label_login_msg.configure(text="❌ Invalid username or password.", text_color="red")

entry_login_pass.bind("<Return>", lambda e: login())

ctk.CTkButton(frame_login, text="Login", font=("Arial", 16),
    width=250, height=40, command=login).pack(pady=5)
ctk.CTkButton(frame_login, text="Don't have an account? Register",
    width=250, fg_color="transparent", border_width=1,
    command=lambda: show_frame(frame_register)).pack(pady=5)

# ==========================================
# หน้าที่ 2 — REGISTER
# ==========================================
ctk.CTkLabel(frame_register, text="Registration", font=("Arial", 22, "bold")).pack(pady=15)
ctk.CTkLabel(frame_register, text="Username:", font=("Arial", 14)).pack()
entry_reg_user = ctk.CTkEntry(frame_register, placeholder_text="Enter username", width=250, height=40)
entry_reg_user.pack(pady=4)
ctk.CTkLabel(frame_register, text="Password:", font=("Arial", 14)).pack()
entry_reg_pass = ctk.CTkEntry(frame_register, placeholder_text="Enter password", width=250, height=40, show="*")
entry_reg_pass.pack(pady=4)
ctk.CTkLabel(frame_register, text="Confirm Password:", font=("Arial", 14)).pack()
entry_reg_confirm = ctk.CTkEntry(frame_register, placeholder_text="Confirm password", width=250, height=40, show="*")
entry_reg_confirm.pack(pady=4)

check_var = ctk.IntVar()
ctk.CTkCheckBox(frame_register, text="I agree to the terms and conditions",
    variable=check_var).pack(pady=8)

label_reg_msg = ctk.CTkLabel(frame_register, text="", font=("Arial", 14))
label_reg_msg.pack(pady=3)

def clear_register():
    entry_reg_user.delete(0, "end")
    entry_reg_pass.delete(0, "end")
    entry_reg_confirm.delete(0, "end")
    check_var.set(0)

def register():
    user = entry_reg_user.get().strip()
    pas  = entry_reg_pass.get().strip()
    conp = entry_reg_confirm.get().strip()
    if user == "" or pas == "" or conp == "":
        label_reg_msg.configure(text="⚠️ Please fill in all fields.", text_color="orange")
        return
    if user in user_db:
        label_reg_msg.configure(text="❌ Username already exists.", text_color="red")
        clear_register()
        return
    if pas != conp:
        label_reg_msg.configure(text="❌ Passwords do not match.", text_color="red")
        clear_register()
        return
    if check_var.get() == 0:
        label_reg_msg.configure(text="⚠️ Please agree to the terms.", text_color="orange")
        return
    user_db[user] = pas
    messagebox.showinfo("Success", f"Registration successful!\nUsername: {user}")
    label_reg_msg.configure(text="")
    clear_register()
    show_frame(frame_login)

ctk.CTkButton(frame_register, text="Register", font=("Arial", 16),
    width=250, height=40, command=register).pack(pady=5)
ctk.CTkButton(frame_register, text="Already have an account? Login",
    width=250, fg_color="transparent", border_width=1,
    command=lambda: show_frame(frame_login)).pack(pady=5)

# ==========================================
# หน้าที่ 3 — CALCULATOR (2 ช่องกรอก)
# ==========================================
ctk.CTkLabel(frame_Cal, text="Calculator", font=("Arial", 22, "bold")).pack(pady=10)

frame_input = ctk.CTkFrame(frame_Cal, fg_color="transparent")
frame_input.pack(pady=5)

ctk.CTkLabel(frame_input, text="Number 1:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_num1 = ctk.CTkEntry(frame_input, width=150, placeholder_text="0")
entry_num1.grid(row=0, column=1, padx=5, pady=5)

ctk.CTkLabel(frame_input, text="Number 2:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_num2 = ctk.CTkEntry(frame_input, width=150, placeholder_text="0")
entry_num2.grid(row=1, column=1, padx=5, pady=5)

label_calc_result = ctk.CTkLabel(frame_Cal, text="Result: ", font=("Arial", 15))
label_calc_result.pack(pady=5)

frame_btn = ctk.CTkFrame(frame_Cal, fg_color="transparent")
frame_btn.pack(pady=5)

# ✅ แก้แล้ว — comma ครบทุกตัว
buttons = [
    '7', '8', '9', '+',
    '4', '5', '6', '-',
    '1', '2', '3', '*',
    '0', '.', 'C', '/'
]

def press(key):
    """กดปุ่มตัวเลข — ใส่เลขในช่องที่โฟกัสอยู่"""
    if key in "0123456789.":
        focused = app.focus_get()
        if focused == entry_num2._entry:
            entry_num2.insert("end", key)
        else:
            entry_num1.insert("end", key)
            entry_num1.focus_set()
    elif key == "C":
        entry_num1.delete(0, "end")
        entry_num2.delete(0, "end")
        label_calc_result.configure(text="Result: ", text_color="white")
        entry_num1.focus_set()
    elif key in "+-*/":
        # กดเครื่องหมาย → โฟกัสไปช่อง 2 อัตโนมัติ
        entry_num2.focus_set()
        calculate(key)

def calculate(op):
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        if op == "+":   result = num1 + num2
        elif op == "-": result = num1 - num2
        elif op == "*": result = num1 * num2
        elif op == "/":
            if num2 == 0:
                label_calc_result.configure(text="⚠️ Cannot divide by zero!", text_color="orange")
                return
            result = num1 / num2
        result_str = int(result) if result == int(result) else round(result, 4)
        label_calc_result.configure(
            text=f"Result: {num1} {op} {num2} = {result_str}",
            text_color="white")
        entry_num1.delete(0, "end")
        entry_num2.delete(0, "end")
        entry_num1.focus_set()
    except ValueError:
        label_calc_result.configure(text="⚠️ Please enter valid numbers!", text_color="orange")

# ✅ แก้แล้ว — col > 3 ขึ้นแถวใหม่ (4 คอลัมน์)
row_val, col_val = 0, 0
for btn_text in buttons:
    ctk.CTkButton(frame_btn, text=btn_text, width=65, height=45,
        font=("Arial", 16),
        command=lambda k=btn_text: press(k)
    ).grid(row=row_val, column=col_val, padx=4, pady=4)
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

# ✅ กดคีย์บอร์ดได้เลย
def on_key(event):
    key = event.char
    if key in "0123456789.":
        press(key)
    elif key in "+-*/":
        calculate(key)
    elif key == "\r":   # Enter
        focused = app.focus_get()
        if focused == entry_num2._entry:
            calculate("+")
    elif key == "\x08": # Backspace
        focused = app.focus_get()
        if focused == entry_num2._entry:
            val = entry_num2.get()
            entry_num2.delete(len(val)-1, "end")
        else:
            val = entry_num1.get()
            entry_num1.delete(len(val)-1, "end")

def go_to_calc():
    show_frame(frame_Cal)
    app.bind("<Key>", on_key)        # ✅ ผูก keyboard เฉพาะตอนเข้าหน้า Cal
    app.after(100, lambda: entry_num1.focus_set())

def go_to_login():
    app.unbind("<Key>")              # ✅ ถอด keyboard ก่อนกลับหน้า Login
    show_frame(frame_login)

ctk.CTkButton(frame_Cal, text="Logout",
    width=200, fg_color="transparent", border_width=1, text_color="gray",
    command=go_to_login).pack(pady=8)

# ==========================================
# เริ่มที่หน้า Login
# ==========================================
show_frame(frame_login)
app.mainloop()
