import customtkinter as ctk
ctk.set_appearance_mode("dark")  # โหมดสีเข้ม 
ctk.set_default_color_theme("blue")  # ธีมสีฟ้า

app = ctk.CTk()
app.title("CTK App")  # ตั้งชื่อหน้าต่าง
app.geometry("400x300")  # กำหนดขนาดหน้าต่าง

ctk.CTkLabel(app, text="Calculator", font=("Arial", 24)).pack(pady=20)
frame_input = ctk.CTkFrame(app,fg_color="transparent")
frame_input.pack(pady=10)

ctk.CTkLabel(frame_input, text="Number 1:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_num1 = ctk.CTkEntry(frame_input, width=150,placeholder_text=" ")
entry_num1.grid(row=0, column=1, padx=5, pady=5)

ctk.CTkLabel(frame_input, text="Number 2:").grid(row=1, column=0, padx=5, pady=5)
entry_num2 = ctk.CTkEntry(frame_input, width=150,placeholder_text="")
entry_num2.grid(row=1, column=1, padx=5, pady=5)

label_calc_result = ctk.CTkLabel(app, text="Result: ", font=("Arial", 16))
label_calc_result.pack(pady=10)

frame_btn = ctk.CTkFrame(app,fg_color="transparent")
frame_btn.pack(pady=10)

for i, op in enumerate(["+", "-", "*", "/"]):
    ctk.CTkButton(frame_btn, text=op, width=80, height=40, font=("Arial", 16), command=lambda o=op: calculate(o)).grid(row=0, column=i, padx=5)
    
def calculate(op):
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        if op == "+":
            result = num1 + num2
        elif op == "-":
            result = num1 - num2
        elif op == "*":
            result = num1 * num2
        elif op == "/":
            if num2 == 0:
                label_calc_result.configure(text="Cannot divide by zero!")
                return
            result = num1 / num2
        result_str = int(result) if result == int(result) else round(result, 4)
        label_calc_result.configure(text=f"Result: {num1} {op} {num2} = {result_str}", text_color="white")
    except ValueError:
        label_calc_result.configure(text="Please enter valid numbers!", text_color="orange")
app.after(100, lambda: entry_num1.focus_set())
app.mainloop()