import cv2
import mediapipe as mp
import customtkinter as ctk
from PIL import Image, ImageDraw
import math
import os

# ==========================================
# ตั้งค่า Theme
# ==========================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def calculate_distance(point1, point2):
    return math.hypot(point2.x - point1.x, point2.y - point1.y)

class ShinobiJutsuApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Shinobi Jutsu Challenge - Hand Tracking Engine")
        self.geometry("1280x720")

        # ตั้งค่า MediaPipe
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.8, min_tracking_confidence=0.8)
        self.cap = cv2.VideoCapture(0)

        # ตัวแปรควบคุมลำดับด่าน
        self.current_step = 0
        self.seals_names = ["ชวด", "ฉลู", "ขาล", "เถาะ", "มะโรง", "มะเส็ง", "มะเมีย", "มะแม", "วอก", "ระกา", "จอ", "กุน"]

        # ==========================================
        # 1. Top Bar
        # ==========================================
        self.top_frame = ctk.CTkFrame(self, height=80, fg_color="#1a1a1a", corner_radius=0)
        self.top_frame.pack(side="top", fill="x")
        
        self.chakra_bar = ctk.CTkFrame(self.top_frame, width=300, height=20, fg_color="#00d4ff")
        self.chakra_bar.pack(side="left", padx=20, pady=20)
        
        self.lbl_title = ctk.CTkLabel(self.top_frame, text="Shinobi Jutsu Challenge", font=("Arial", 24, "bold"))
        self.lbl_title.pack(side="left", expand=True)

        self.lbl_score = ctk.CTkLabel(self.top_frame, text="Combo: 0   Score: 28000", font=("Arial", 18, "bold"), text_color="#ffcc00")
        self.lbl_score.pack(side="right", padx=30)

        # ==========================================
        # 2. Main Content
        # ==========================================
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # ------------------------------------------
        # Left Panel (Catalog - แสดงภาพเต็มเป็นพื้นหลัง)
        # ------------------------------------------
        self.left_panel = ctk.CTkFrame(self.main_frame, width=380, fg_color="#2b2b2b", border_width=2, border_color="#c8a04b")
        self.left_panel.pack(side="left", fill="y", padx=(0, 10))
        self.left_panel.pack_propagate(False) 
        
        self.lbl_catalog_title = ctk.CTkLabel(self.left_panel, text="NINJUTSU SEQUENCE", font=("Arial", 16, "bold"))
        self.lbl_catalog_title.pack(pady=10)

        # ------------------------------------------
        # ระบบโหลดรูปภาพอัจฉริยะ (แก้ปัญหารูปไม่ขึ้น)
        # ------------------------------------------
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_name = "images.jpg"
        image_path = os.path.join(current_dir, image_name)

        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"หาไฟล์ไม่เจอที่:\n{image_path}")

            self.base_pil_image = Image.open(image_path).convert("RGBA")
            self.base_pil_image = self.base_pil_image.resize((360, 480), Image.Resampling.LANCZOS)
            
            self.lbl_catalog_img = ctk.CTkLabel(self.left_panel, text="")
            self.lbl_catalog_img.pack(expand=True, padx=10, pady=(0, 10))
            
            # วาด UI ของ Catalog ครั้งแรก
            self.update_catalog_ui()
            
        except Exception as e:
            # สร้างกล่องสีเทาและแสดง Error สีแดงถ้าโหลดรูปไม่สำเร็จ
            self.base_pil_image = Image.new("RGBA", (360, 480), (80, 80, 80, 255))
            error_msg = f"ไม่สามารถโหลดรูปภาพได้!\n\nโปรดนำรูปไปวางที่:\n{image_path}"
            self.lbl_catalog_img = ctk.CTkLabel(self.left_panel, text=error_msg, text_color="#ff4444", font=("Arial", 14), wraplength=320)
            self.lbl_catalog_img.pack(expand=True, padx=10, pady=(0, 10))

        # ------------------------------------------
        # Right Panel (Camera)
        # ------------------------------------------
        self.right_panel = ctk.CTkFrame(self.main_frame, fg_color="#000000", border_width=2, border_color="#c8a04b")
        self.right_panel.pack(side="right", fill="both", expand=True)
        self.lbl_camera = ctk.CTkLabel(self.right_panel, text="")
        self.lbl_camera.pack(expand=True, fill="both", padx=5, pady=5)

        # ==========================================
        # 3. Bottom Bar
        # ==========================================
        self.bottom_frame = ctk.CTkFrame(self, height=60, fg_color="#1a1a1a")
        self.bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        self.lbl_combo = ctk.CTkLabel(self.bottom_frame, text="Seal Sequence: Rat (ชวด) ➔ Ox (ฉลู) ➔ Tiger (ขาล)", font=("Arial", 16, "bold"))
        self.lbl_combo.pack(pady=15)

        self.update_camera()

    def update_catalog_ui(self):
        """ วาดกรอบสีเขียวโปร่งแสงทับรูปภาพที่ทำผ่านแล้ว """
        # ถ้าไม่มีรูปภาพจริง (ใช้กล่องสีเทา) จะข้ามการวาด
        if not hasattr(self, 'lbl_catalog_img') or self.lbl_catalog_img.cget("text") != "":
            return

        overlay = Image.new('RGBA', self.base_pil_image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        
        w, h = self.base_pil_image.size
        cell_w = w / 3
        cell_h = h / 4

        for i in range(self.current_step):
            if i >= 12: break
            row = i // 3
            col = i % 3
            
            x0, y0 = col * cell_w, row * cell_h
            x1, y1 = x0 + cell_w, y0 + cell_h
            
            # วาดสีเขียวโปร่งแสง (RGBA)
            draw.rectangle([x0, y0, x1, y1], fill=(46, 204, 113, 140))
            
        final_img = Image.alpha_composite(self.base_pil_image, overlay)
        ctk_img = ctk.CTkImage(light_image=final_img, dark_image=final_img, size=(w, h))
        self.lbl_catalog_img.configure(image=ctk_img)
        self.lbl_catalog_img.image = ctk_img

    def detect_jutsu(self, hand_landmarks_list):
        debug_text = ""
        # บังคับให้ต้องเห็นมือ 2 ข้างถึงจะประมวลผล
        if len(hand_landmarks_list) == 2:
            hand1 = hand_landmarks_list[0].landmark
            hand2 = hand_landmarks_list[1].landmark
            
            threshold = 0.12 
            def get_dist(p1, p2):
                return calculate_distance(hand1[p1], hand2[p2])

            if self.current_step == 0:
                dist = get_dist(12, 12)
                debug_text = f"Dist (Mid): {dist:.3f} / {threshold}"
                if dist < threshold:
                    return 0, "RAT (ชวด) - DETECTED!", debug_text
                    
            elif self.current_step == 1:
                dist = get_dist(20, 20)
                debug_text = f"Dist (Pinky): {dist:.3f} / {threshold}"
                if dist < threshold:
                    return 1, "OX (ฉลู) - DETECTED!", debug_text
                    
            elif self.current_step == 2:
                dist_index = get_dist(8, 8)
                dist_thumb = get_dist(4, 4)
                debug_text = f"Idx: {dist_index:.3f}, Thb: {dist_thumb:.3f}"
                if dist_index < threshold and dist_thumb < threshold:
                    return 2, "TIGER (ขาล) - DETECTED!", debug_text
                    
        if self.current_step < len(self.seals_names):
            next_seal = self.seals_names[self.current_step]
            return -1, f"WAITING FOR: {next_seal}...", debug_text
        else:
            return -1, "ALL SEALS COMPLETED!", ""

    def update_camera(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            results = self.hands.process(rgb_frame)
            
            detected_idx = -1
            detected_pose = "WAITING FOR POSE..."
            debug_info = ""
            
            if results.multi_hand_landmarks:
                detected_idx, detected_pose, debug_info = self.detect_jutsu(results.multi_hand_landmarks)
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(rgb_frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

            # อัปเดต UI เมื่อทำท่าผ่าน
            if detected_idx != -1 and detected_idx == self.current_step:
                self.current_step += 1
                self.update_catalog_ui()

            # วาด UI ของกล้อง
            cv2.rectangle(rgb_frame, (10, 10), (w-10, 75), (45, 95, 75), -1)
            cv2.rectangle(rgb_frame, (10, 10), (w-10, 75), (120, 255, 200), 2)
            cv2.putText(rgb_frame, f"POSE: {detected_pose}", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 255, 200), 2)
            cv2.putText(rgb_frame, f"DEBUG: {debug_info}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 200, 100), 1)

            # นำภาพกล้องไปแสดงผล
            img = Image.fromarray(rgb_frame)
            panel_width = self.right_panel.winfo_width()
            panel_height = self.right_panel.winfo_height()
            
            if panel_width > 10 and panel_height > 10:
                img = img.resize((panel_width - 10, panel_height - 10), Image.Resampling.LANCZOS)
                
            imgtk = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            self.lbl_camera.configure(image=imgtk)
            self.lbl_camera.image = imgtk

        self.after(15, self.update_camera)

    def on_closing(self):
        self.cap.release()
        self.destroy()

if __name__ == "__main__":
    app = ShinobiJutsuApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()