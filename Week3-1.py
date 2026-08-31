#Widgets + Layout
import customtkinter as ctk
ctk.set_appearance_mode("system")  # โหมดสีเข้ม
#"System" (ค่าเริ่มต้น): เปลี่ยนไปตามการตั้งค่าของระบบปฏิบัติการ
#"Dark": บังคับให้เป็นโหมดสีเข้ม (Dark Mode)
#"Light": บังคับให้เป็นโหมดสีสว่าง (Light Mode)
ctk.set_default_color_theme("blue")  # ธีมสีฟ้า
#"blue"	สีน้ำเงินมาตรฐาน (ค่าเริ่มต้น)
#"dark-blue"	สีน้ำเงินเข้ม
#"green"	สีเขียว
app = ctk.CTk()
app.title("Widget App")  # ตั้งชื่อหน้าต่าง   
app.geometry("400x400")  # กำหนดขนาดหน้าต่าง

# CTKlabel
label = ctk.CTkLabel(app, text="Hello CTK!", font=("Arial", 20))
label.pack(pady=20)

# CTKbutton
btn = ctk.CTkButton(app, text="Click here", font=("Arial", 16),width=120, height=40)
btn.pack(pady=20)

# CTKentry (input)
entry = ctk.CTkEntry(app, placeholder_text="Enter your name", width=200, height=40)
entry.pack(pady=20)

# CTKcheckbox 
checkbox = ctk.CTkCheckBox(app, text="I agree to the terms and conditions", font=("Arial", 14))
checkbox.pack(pady=20)

#CTKSLIDER
slider = ctk.CTkSlider(app, from_=0, to=100, width=200)
slider.pack(pady=20)

app.mainloop()    