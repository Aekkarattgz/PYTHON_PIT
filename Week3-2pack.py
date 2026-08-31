import customtkinter as ctk

app = ctk.CTk()
app.geometry("400x400")  # กำหนดขนาดหน้าต่าง
app.title("Pack Layout")  # ตั้งชื่อหน้าต่าง

label1 = ctk.CTkLabel(app, text="Label 1", width=100, height=50, fg_color="red",text_color="white")
label1.pack(pady=10,fill="x",padx=20)  # จัดวาง Label1 และเพิ่มระยะห่างแนวตั้ง

label2 = ctk.CTkLabel(app, text="Label 2", width=100, height=50, fg_color="green")
label2.pack(pady=10,fill="x",padx=20)  # จัดวาง Label2 และเพิ่มระยะห่างแนวตั้ง

btn = ctk.CTkButton(app, text="Click Me", width=100, height=50, fg_color="blue",text_color="white")
btn.pack(pady=10,fill="x",padx=20)  # จัดวางปุ่มและเพิ่มระยะห่างแนวตั้ง

app.mainloop()
"""
fg_color Foreground Colorสีของ ตัว Widget เอง (พื้นหลังของกล่อง)
text_color Text Colorสีของ ตัวอักษร ข้างใน
bg_color Background Colorสีของ พื้นหลังหน้าต่าง ที่ Widget วางอยู่

"""
