#Event Handling
import customtkinter as ctk
ctk.set_appearance_mode("dark")  # โหมดสีเข้ม
ctk.set_default_color_theme("blue")  # ธีมสีฟ้า
app = ctk.CTk()
app.title("Event Handling")  # ตั้งชื่อหน้าต่าง
app.geometry("400x400")  # กำหนดขนาดหน้าต่าง

#ฟังก์ชันสำหรับจัดการเหตุการณ์เมื่อปุ่มถูกคลิก
def button_click():
    name = enty.get()  # ดึงข้อมูลจากช่องกรอกข้อความ
    if name == "": # ตรวจสอบว่าช่องกรอกข้อความไม่ว่างเปล่า
        label_result.configure(text="Enteryour name: ")
    else:
        label_result.configure(text="Hello " + name + "!")

#widget ต่างๆ
enty = ctk.CTkEntry(app, placeholder_text="Enter your name", width=200, height=40)
enty.pack(pady=20)

btn = ctk.CTkButton(app, text="Confirm", font=("Arial", 16),width=120, height=40, command=button_click)
btn.pack(pady=20)

label_result = ctk.CTkLabel(app, text="", font=("Arial", 20))
label_result.pack(pady=20)
app.mainloop()