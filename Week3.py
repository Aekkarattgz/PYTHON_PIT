#Main Window
import customtkinter as ctk

#ตั้งค่ารูปแบบของแอปพลิเคชัน
ctk.set_appearance_mode("dark")  # โหมดสีเข้ม
ctk.set_default_color_theme("blue")  # ธีมสีฟ้า

#สร้างหน้าต่างหลักของแอปพลิเคชัน
app = ctk.CTk()
app.title("My CTK App")  # ตั้งชื่อหน้าต่าง
app.geometry("400x300")  # กำหนดขนาดหน้าต่าง

#สั่งให้แอปพลิเคชันแสดงหน้าต่าง
app.mainloop()