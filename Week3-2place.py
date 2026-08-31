import customtkinter as ctk

app = ctk.CTk()
app.title("Place Layout")  # ตั้งชื่อหน้าต่าง
app.geometry("400x400")  # กำหนดขนาดหน้าต่าง

label1 = ctk.CTkLabel(app, text="Label 1", width=100, height=50, fg_color="red",text_color="white")
label1.place(x=50, y=50)  # จัดวาง Label1 ที่ตำแหน่ง (50, 50)
label2 = ctk.CTkLabel(app, text="Label 2", width=100, height=50, fg_color="green")
label2.place(x=200, y=50)  # จัดวาง Label2 ที่ตำแหน่ง (200, 50)
btn = ctk.CTkButton(app, text="Click Me", width=100, height=50, fg_color="blue",text_color="white")
btn.place(relx=0.5, rely=0.5, anchor="center")  # จัดวางปุ่มที่ตำแหน่งกึ่งกลางของหน้าต่าง  
#relx=0.5: วางตำแหน่งที่ 50% ของความกว้างหน้าต่าง (กึ่งกลางแนวนอน)
#rely=0.5: วางตำแหน่งที่ 50% ของความสูงหน้าต่าง (กึ่งกลางแนวตั้ง)
#anchor="center": กำหนดให้จุดศูนย์กลางของปุ่มเป็นตำแหน่งที่กำหนด (relx, rely)
#x=100, y=100	ระบุพิกเซลตายตัว
#relx=0.5, rely=0.5	ระบุตำแหน่งสัมพันธ์ (%)
app.mainloop()
"""
place(x=50, y=50)  นับจาก มุมบนซ้ายของหน้าต่าง เป็น pixel
relx, rely คือ สัดส่วน 0.0 ถึง 1.0 ของขนาดหน้าต่าง
ค่าความหมายrelx=0.5แนวนอน = กึ่งกลางหน้าต่าง (50%)
rely=0.5แนวตั้ง = กึ่งกลางหน้าต่าง (50%)
anchor="center"จุดยึดของ Widget = ตรงกลาง
"""
