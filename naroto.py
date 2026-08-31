
import cv2
import mediapipe as mp
import customtkinter as ctk
from PIL import Image
import math

# ==========================================
# ตั้งค่า Theme ของ CustomTkinter
# ==========================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def calculate_distance(point1, point2):
    """ฟังก์ชันคำนวณระยะห่างระหว่าง 2 Landmark เพื่อตรวจจับอิน"""
    return math.hypot(point2.x - point1.x, point2.y - point1.y)

class ShinobiJutsuApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Shinobi Jutsu Challenge - Hand Tracking Engine")
        self.geometry("1280x720")

        # ==========================================
        # การตั้งค่า MediaPipe และกล้อง
        # ==========================================
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
        self.cap = cv2.VideoCapture(0)

        # ==========================================
        # 1. Top Bar (Chakra, Title, Score)
        # ==========================================
        self.top_frame = ctk.CTkFrame(self, height=80, fg_color="#1a1a1a", corner_radius=0)
        self.top_frame.pack(side="top", fill="x")
        
        # หลอด Chakra
        self.chakra_bar = ctk.CTkFrame(self.top_frame, width=300, height=20, fg_color="#00d4ff")
        self.chakra_bar.pack(side="left", padx=20, pady=20)
        
        self.lbl_title = ctk.CTkLabel(self.top_frame, text="Shinobi Jutsu Challenge", font=("Arial", 24, "bold"))
        self.lbl_title.pack(side="left", expand=True)

        self.lbl_score = ctk.CTkLabel(self.top_frame, text="Combo: 0   Score: 28000", font=("Arial", 18, "bold"), text_color="#ffcc00")
        self.lbl_score.pack(side="right", padx=30)

        # ==========================================
        # 2. Main Content (แบ่งซ้าย-ขวา)
        # ==========================================
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # ------------------------------------------
        # ด้านซ้าย: NINJUTSU CATALOG (Grid)
        # ------------------------------------------
        self.left_panel = ctk.CTkFrame(self.main_frame, width=350, fg_color="#2b2b2b", border_width=2, border_color="#c8a04b")
        self.left_panel.pack(side="left", fill="y", padx=(0, 10))
        self.left_panel.pack_propagate(False) # ล็อกขนาดความกว้าง
        
        self.lbl_catalog = ctk.CTkLabel(self.left_panel, text="NINJUTSU CATALOG\n(12 ZODIAC SEALS)", font=("Arial", 16, "bold"))
        self.lbl_catalog.pack(pady=10)

        self.grid_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.grid_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # ระบบโหลดและตัดรูปภาพ (Auto-Cropping) 
        try:
            source_img = Image.open("image_fdc5bc.jpg")
            img_width, img_height = source_img.size
            cell_w = img_width // 3
            cell_h = img_height // 4
            
            self.seal_images = []
            for i in range(4): # 4 แถว
                for j in range(3): # 3 คอลัมน์
                    left, top = j * cell_w, i * cell_h
                    right, bottom = (j + 1) * cell_w, (i + 1) * cell_h
                    
                    cropped = source_img.crop((left, top, right, bottom))
                    ctk_img = ctk.CTkImage(light_image=cropped, dark_image=cropped, size=(90, 90))
                    self.seal_images.append(ctk_img)
            
            for idx, ctk_img in enumerate(self.seal_images):
                row, col = idx // 3, idx % 3
                box = ctk.CTkLabel(self.grid_frame, text="", image=ctk_img, width=90, height=90, corner_radius=5)
                box.grid(row=row, column=col, padx=5, pady=5)
                
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการโหลดรูปภาพ: {e}")
            seals = ["ชวด", "ฉลู", "ขาล", "เถาะ", "มะโรง", "มะเส็ง", "มะเมีย", "มะแม", "วอก", "ระกา", "จอ", "กุน"]
            for i, name in enumerate(seals):
                row, col = i // 3, i % 3
                box = ctk.CTkLabel(self.grid_frame, text=name, width=90, height=90, fg_color="#404040", corner_radius=5)
                box.grid(row=row, column=col, padx=5, pady=5)

        # ------------------------------------------
        # ด้านขวา: Camera Feed & Game View
        # ------------------------------------------
        self.right_panel = ctk.CTkFrame(self.main_frame, fg_color="#000000", border_width=2, border_color="#c8a04b")
        self.right_panel.pack(side="right", fill="both", expand=True)
        
        self.lbl_camera = ctk.CTkLabel(self.right_panel, text="")
        self.lbl_camera.pack(expand=True, fill="both", padx=5, pady=5)

        # ==========================================
        # 3. Bottom Bar (Combination)
        # ==========================================
        self.bottom_frame = ctk.CTkFrame(self, height=60, fg_color="#1a1a1a")
        self.bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        
        self.lbl_combo = ctk.CTkLabel(self.bottom_frame, text="Seal Combination: [ ? ] ➔ [ ? ] ➔ [ ? ]", font=("Arial", 16, "bold"))
        self.lbl_combo.pack(pady=15)

        # เริ่มต้นลูปกล้อง
        self.update_camera()

    def detect_jutsu(self, hand_landmarks_list):
        """ระบบวิเคราะห์ท่าทางแบบเรียลไทม์"""
        if len(hand_landmarks_list) == 2:
            hand1 = hand_landmarks_list[0].landmark
            hand2 = hand_landmarks_list[1].landmark
            
            # วัดระยะนิ้วชี้ (8) และ นิ้วโป้ง (4) ของทั้งสองมือ
            index_dist = calculate_distance(hand1[8], hand2[8])
            thumb_dist = calculate_distance(hand1[4], hand2[4])
            
            threshold = 0.05 
            if index_dist < threshold and thumb_dist < threshold:
                return "TIGER (ขาล) - CONFIDENCE 98.7%"
                
        return "WAITING FOR POSE..."

    def update_camera(self):
        """ลูปอัปเดตภาพจากกล้องและประมวลผล MediaPipe"""
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            
            # แปลงสีเพื่อส่งให้ MediaPipe และ Tkinter
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            
            detected_pose = "WAITING FOR POSE..."
            
            if results.multi_hand_landmarks:
                detected_pose = self.detect_jutsu(results.multi_hand_landmarks)
                
                # วาดเส้นสเกลเลตันบนมือ
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        rgb_frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

            # --- วาดกราฟิก Overlay ของเกมลงบนภาพ ---
            # ใช้สี RGB สำหรับวาดลงใน rgb_frame โดยตรง
            color_bg = (45, 95, 75)
            color_border = (120, 255, 200)
            text_color = (200, 255, 200)
            
            cv2.rectangle(rgb_frame, (10, 10), (w-10, 50), color_bg, -1)
            cv2.rectangle(rgb_frame, (10, 10), (w-10, 50), color_border, 2)
            cv2.putText(rgb_frame, f"POSE DETECTED: {detected_pose}", (20, 35), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2, cv2.LINE_AA)
            
            # กรอบเล็งเป้าหมายตรงกลาง
            center_x, center_y = w//2, h//2
            box_size = 200
            cv2.rectangle(rgb_frame, (center_x - box_size, center_y - box_size), 
                                     (center_x + box_size, center_y + box_size), color_border, 2)

            # --- นำภาพขึ้นแสดงใน UI ---
            img = Image.fromarray(rgb_frame)
            
            # ดึงขนาดของ Panel ฝั่งขวาเพื่อให้ภาพ Responsive
            panel_width = self.right_panel.winfo_width()
            panel_height = self.right_panel.winfo_height()
            
            if panel_width > 10 and panel_height > 10:
                img = img.resize((panel_width - 10, panel_height - 10), Image.Resampling.LANCZOS)
                
            imgtk = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            
            self.lbl_camera.configure(image=imgtk)
            self.lbl_camera.image = imgtk

        # เรียกซ้ำเพื่ออัปเดตเฟรมถัดไป (15ms ~= 60 FPS)
        self.after(15, self.update_camera)

    def on_closing(self):
        """เคลียร์ทรัพยากรกล้องเมื่อปิดโปรแกรม"""
        self.cap.release()
        self.destroy()

if __name__ == "__main__":
    app = ShinobiJutsuApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()

