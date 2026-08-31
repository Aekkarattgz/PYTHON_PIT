import cv2 # OpenCV
import customtkinter as ctk # CustomTkinter
from PIL import Image # PIL ช้ช่วยจัดการรูปภาพก่อนนำรูปไปแสดงในหน้าต่างโปรแกรม
from ultralytics import YOLOWorld # เป็นตัวโมเดล AI ที่ใช้สำหรับตรวจจับวัตถุในภาพ
import torch # ใช้ตรวจสอบว่าเครื่องมี GPU ที่รองรับ CUDA หรือไม่
 
ctk.set_appearance_mode("dark") # กำหนดให้หน้าตาโปรแกรมใช้โหมดมืด 
ctk.set_default_color_theme("blue")  # กำหนดธีมสีของโปรแกรม

# กำหนด device ให้ชัดเจนจุดเดียว ใช้ตัวแปรนี้ตลอดทั้งไฟล์
DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu" 

model = YOLOWorld("yolov8s-worldv2.pt") # ตัวแปร model ก็คือ "ตัว AI" ที่เราจะใช้ตรวจจับวัตถุ
model.to(DEVICE)                          # ย้ายโมเดลไป device ที่กำหนดตั้งแต่ต้น
model.set_classes(["person", "cell phone", "bottle", "pen"])
model.to(DEVICE)                          # ย้ายโมเดลไปยัง CPU หรือ GPU อีกครั้ง หลังจากมีการตั้ง Class ใหม่
# สร้าง Class ชื่อ App ใช้เป็นตัวควบคุมหน้าต่างและการทำงานทั้งหมดของโปรแกรม
class App(ctk.CTk):
    def __init__(self):
        super().__init__() # เรียกการทำงานพื้นฐานของ CTk
        self.title("YOLO-World + CustomTkinter") # กำหนดชื่อที่แสดงบนแถบด้านบนของหน้าต่าง
        self.geometry("800x680") # กำหนดขนาดหน้าต่าง กว้าง 800 สูง 680

        self.video_label = ctk.CTkLabel(self, text="") # สร้างพื้นที่สำหรับแสดงภาพ
        self.video_label.pack(pady=10) # นำพื้นที่แสดงภาพไปวางในหน้าต่าง
        # สร้างช่องกรอกข้อความ cup, phone, book
        self.entry_classes = ctk.CTkEntry(
            self, placeholder_text="พิมพ์คลาส คั่นด้วย , เช่น cup, phone, book"
        )
        # นำช่องกรอกข้อความไปวางในหน้าต่าง
        self.entry_classes.pack(pady=5, fill="x", padx=20)
        self.btn_set = ctk.CTkButton(self, text="ตั้งคลาสใหม่", command=self.set_classes) # สร้างปุ่ม "ตั้งคลาสใหม่" 
        self.btn_set.pack(pady=5) # นำปุ่มไปวางในหน้าต่าง

        self.btn_start = ctk.CTkButton(self, text="เปิดกล้อง", command=self.start_camera) # สร้างปุ่ม "เปิดกล้อง"
        self.btn_start.pack(pady=5)  # นำปุ่มไปวางในหน้าต่าง

        self.cap = None # ตอนเริ่มต้นยังไม่มีกล้อง จึงกำหนดเป็น None
        self.running = False # False หมายถึงตอนนี้ยังไม่ได้เปิดการทำงานของกล้อง
        self.frame_count = 0 # ใช้นับจำนวน Frame ที่อ่านจากกล้อง

    def set_classes(self): # ฟังก์ชันนี้จะทำงานเมื่อผู้ใช้กดปุ่ม "ตั้งคลาสใหม่"
        text = self.entry_classes.get() # อ่านข้อความที่ผู้ใช้พิมพ์ลงในช่อง
        classes = [c.strip() for c in text.split(",") if c.strip()] # แยกข้อความออกจากกันด้วยเครื่องหมาย comma
        if classes: # ตรวจสอบว่ามี Class ที่ผู้ใช้พิมพ์เข้ามาหรือไม่
            model.set_classes(classes) # จากนั้น AI จะเปลี่ยนไปสนใจสิ่งเหล่านี้
            model.to(DEVICE)              # << จุดสำคัญทุกครั้งที่ set_classes ใหม่ ต้องย้ำ device อีกครั้ง

    def start_camera(self):  # ฟังก์ชันนี้จะทำงานเมื่อกดปุ่ม "เปิดกล้อง"
        if not self.running:  # ตรวจสอบว่าตอนนี้กล้องยังไม่ได้ทำงานหรือไม่
            self.cap = cv2.VideoCapture(0)  # เปิดกล้องตัวที่ 0
            self.running = True  # เปลี่ยนสถานะเป็นกำลังทำงาน
            self.update_frame() # เริ่มกระบวนการอ่านภาพจากกล้อง

    def update_frame(self):
        if not self.running:  # ถ้าโปรแกรมไม่ได้ทำงาน ก็ไม่ต้องทำอะไรต่อ
            return

        ret, frame = self.cap.read()
        if ret:
            self.frame_count += 1 # เพิ่มจำนวน Frame ขึ้น 1
            if self.frame_count % 2 == 0:   # ตรวจจับทุก ๆ 2 Frame วิธีนี้ช่วยลดจำนวนครั้งที่ต้องให้ AI ประมวลผล
                results = model.predict(frame, conf=0.4, device=DEVICE, verbose=False)
                # conf=0.4 = กำหนดระดับความมั่นใจขั้นต่ำประมาณ 40%
                # device=DEVICE = บอกให้โมเดลทำงานบน CPU หรือ GPU ที่เลือกไว้
                # verbose=False = ไม่ต้องแสดงข้อความรายละเอียดการทำงานออกมามากมาย
                frame = results[0].plot()
 
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # แปลงรูปแบบสีของภาพ
            # เปลี่ยนข้อมูลภาพจาก OpenCV ให้กลายเป็นรูปแบบ Image ของ PIL
            img = Image.fromarray(frame_rgb)
            # สร้างรูปภาพสำหรับนำไปแสดงใน CustomTkinter 
            self.current_img = ctk.CTkImage(light_image=img, dark_image=img, size=(640, 480))
            # นำภาพไปแสดงใน video_label
            self.video_label.configure(image=self.current_img)
        #หลังจากผ่านไปประมาณ 15 milliseconds ให้กลับมาเรียก update_frame() อีกครั้ง
        self.after(15, self.update_frame)


if __name__ == "__main__":
    app = App()
    app.mainloop()