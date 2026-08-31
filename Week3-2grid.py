import customtkinter as ctk

app = ctk.CTk()
app.title("Grid Layout")  # ตั้งชื่อหน้าต่าง
app.geometry("400x400")  # กำหนดขนาดหน้าต่าง

app.grid_rowconfigure(1, weight=1)  # กำหนดให้แถวที่ 1 มีน้ำหนัก 1
label_name = ctk.CTkLabel(app, text="Name:")
label_name.grid(row=0, column=0, padx=20, pady=10, sticky="w")  # จัดวาง Label ชื่อที่แถว 0 คอลัมน์ 0
entry_name = ctk.CTkEntry(app, placeholder_text="Enter your name")
entry_name.grid(row=0, column=1, padx=20, pady=10, sticky="ew")  # จัดวาง Entry ชื่อที่แถว 0 คอลัมน์ 1

label_email = ctk.CTkLabel(app, text="Email:")
label_email.grid(row=1, column=0, padx=20, pady=10, sticky="w")  # จัดวาง Label อีเมลที่แถว 1 คอลัมน์ 0
entry_email = ctk.CTkEntry(app, placeholder_text="Enter your email")
entry_email.grid(row=1, column=1, padx=20, pady=10, sticky="ew")  # จัดวาง Entry อีเมลที่แถว 1 คอลัมน์ 1

btn_submit = ctk.CTkButton(app, text="Submit", width=100)
btn_submit.grid(row=2, column=0, columnspan=2, pady=20)  # จัดวางปุ่ม Submit ที่แถว 2 คอลัมน์ 0-1
app.after(100, lambda: entry_name.focus_set())
app.mainloop()

#"ew" (East + West): ยืด Widget ให้เต็มความกว้างของช่อง (ซ้ายไปขวา)
#"ns" (North + South): ยืด Widget ให้เต็มความสูงของช่อง (บนลงล่าง)
#"nsew": ยืด Widget ให้ เต็มพื้นที่ช่องทั้งสี่ด้าน (นิยมใช้มากที่สุดเพื่อให้ UI ดูสมมาตร)

#"n"ชิดบนNorth"s"ชิดล่างSouth"e"ชิดขวาEast"w"ชิดซ้ายWest
#"ne"ชิดขวาบน"nw"ชิดซ้ายบน"se"ชิดขวาล่าง"sw"ชิดซ้ายล่าง
#"ew"ยืดซ้าย-ขวาEntry, กล่องกรอกข้อมูล"ns"ยืดบน-ล่างListbox, พื้นที่สูง"nsew"ยืดทุกทิศFrame, Text area
'''
nw    n    ne
  ┌───┬───┬───┐
  │↖  │ ↑ │  ↗│
w ├───┼───┼───┤ e
  │ ← │[w]│ → │
  ├───┼───┼───┤
  │↙  │ ↓ │  ↘│
  └───┴───┴───┘
sw    s    se

ไม่ระบุ = Widget อยู่กลางช่องพอดี
"nsew" = ยืดเต็มช่องทุกด้าน
'''