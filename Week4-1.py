#Frame and Layout
import customtkinter as ctk
ctk.set_appearance_mode("dark")  # โหมดสีเข้ม
ctk.set_default_color_theme("blue")  # ธีมสีฟ้า
app = ctk.CTk()
app.title("Frame and Layout")  # ตั้งชื่อหน้าต่าง
app.geometry("500x400")  # กำหนดขนาดหน้าต่าง
#สร้าง Frame
frame1 = ctk.CTkFrame(app, width=200, height=300)
frame1.pack(side="left", padx=20, pady=20)  # จัดวาง Frame1 ทางซ้าย

ctk.CTkLabel(frame1, text="Menu", font=("Arial", 16, "bold")).pack(pady=10)
ctk.CTkButton(frame1, text="Home", width=150).pack(pady=5)
ctk.CTkButton(frame1, text="Profile", width=150).pack(pady=5)
ctk.CTkButton(frame1, text="Logout", width=150).pack(pady=5)

#สร้าง Frame2
frame2 = ctk.CTkFrame(app, width=300, height=300)
frame2.pack(side="right", padx=20, pady=20)  # จัดวาง Frame2 ทางขวา

ctk.CTkLabel(frame2, text="Content Area", font=("Arial", 16, "bold")).pack(pady=10)
ctk.CTkLabel(frame2, text="Welcome to the content area!", font=("Arial", 14)).pack(pady=10)

app.mainloop()

