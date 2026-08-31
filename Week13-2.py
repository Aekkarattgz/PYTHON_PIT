import cv2
import mediapipe as mp
import customtkinter as ctk
from PIL import Image, ImageDraw
import random
import math
import time

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, max_num_hands=2)
mp_draw = mp.solutions.drawing_utils

CAM_W, CAM_H = 640, 480
TARGET_RADIUS = 40
PUNCH_SPEED_THRESHOLD = 0.04   # ความเร็วขั้นต่ำที่ถือว่าเป็นการต่อย (normalize coordinate/frame)


class BoxingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Boxing Game - MediaPipe")
        self.geometry("750x680")

        # --- UI ---
        self.video_label = ctk.CTkLabel(self, text="")
        self.video_label.pack(pady=10)

        self.score_label = ctk.CTkLabel(self, text="Score: 0", font=("Arial", 24, "bold"))
        self.score_label.pack(pady=5)

        self.time_label = ctk.CTkLabel(self, text="Time: 30", font=("Arial", 18))
        self.time_label.pack(pady=5)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)

        self.btn_start = ctk.CTkButton(btn_frame, text="เริ่มเกม", command=self.start_game)
        self.btn_start.grid(row=0, column=0, padx=10)

        self.btn_stop = ctk.CTkButton(btn_frame, text="หยุด", command=self.stop_game)
        self.btn_stop.grid(row=0, column=1, padx=10)

        # --- State ---
        self.cap = None
        self.running = False
        self.score = 0
        self.time_left = 30
        self.game_start_time = None

        self.target_x = 0
        self.target_y = 0
        self.spawn_new_target()

        # เก็บตำแหน่งกำปั้นเฟรมก่อนหน้า ไว้คำนวณความเร็ว
        self.prev_positions = {}   # key = "Left"/"Right", value = (x, y, time)

    def spawn_new_target(self):
        """สุ่มตำแหน่งเป้าใหม่ เว้นขอบไว้ไม่ให้ชิดขอบจอเกินไป"""
        margin = TARGET_RADIUS + 20
        self.target_x = random.randint(margin, CAM_W - margin)
        self.target_y = random.randint(margin, CAM_H - margin)

    def start_game(self):
        if not self.running:
            self.cap = cv2.VideoCapture(0)
            self.running = True
            self.score = 0
            self.time_left = 30
            self.game_start_time = time.time()
            self.prev_positions = {}
            self.spawn_new_target()
            self.update_frame()
            self.update_timer()

    def stop_game(self):
        self.running = False
        if self.cap:
            self.cap.release()

    def update_timer(self):
        if not self.running:
            return
        elapsed = time.time() - self.game_start_time
        self.time_left = max(0, 30 - int(elapsed))
        self.time_label.configure(text=f"Time: {self.time_left}")

        if self.time_left <= 0:
            self.stop_game()
            self.time_label.configure(text="หมดเวลา!")
        else:
            self.after(500, self.update_timer)

    def check_punch(self, hand_label, fist_x, fist_y, now):
        """เช็คว่ากำปั้นนี้ชนเป้า + เคลื่อนที่เร็วพอไหม"""
        speed = 0
        if hand_label in self.prev_positions:
            px, py, ptime = self.prev_positions[hand_label]
            dt = now - ptime
            if dt > 0:
                dist_moved = math.sqrt((fist_x - px) ** 2 + (fist_y - py) ** 2)
                speed = dist_moved / dt / 30   # ปรับ scale ให้เทียบง่ายกับ threshold

        self.prev_positions[hand_label] = (fist_x, fist_y, now)

        # แปลงพิกัด normalize (0-1) เป็นพิกัดจริงบนภาพ
        px_real = fist_x * CAM_W
        py_real = fist_y * CAM_H
        dist_to_target = math.sqrt((px_real - self.target_x) ** 2 + (py_real - self.target_y) ** 2)

        if dist_to_target < TARGET_RADIUS and speed > PUNCH_SPEED_THRESHOLD:
            return True
        return False

    def update_frame(self):
        if not self.running:
            return

        ret, frame = self.cap.read()
        if ret:
            frame = cv2.resize(frame, (CAM_W, CAM_H))
            frame = cv2.flip(frame, 1)   # กลับภาพซ้าย-ขวา ให้เหมือนมองกระจก ต่อยง่ายขึ้น

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            now = time.time()
            hit_this_frame = False

            if results.multi_hand_landmarks:
                for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    label = results.multi_handedness[idx].classification[0].label
                    # ใช้ข้อมือ (จุด 0) แทนตำแหน่ง "กำปั้น" เพราะเสถียรกว่าปลายนิ้ว
                    wrist = hand_landmarks.landmark[0]

                    if self.check_punch(label, wrist.x, wrist.y, now):
                        hit_this_frame = True

            if hit_this_frame:
                self.score += 1
                self.score_label.configure(text=f"Score: {self.score}")
                self.spawn_new_target()

            # --- วาดเป้าลงบนภาพด้วย PIL (วาดวงกลมสีแดง) ---
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            draw = ImageDraw.Draw(img)
            draw.ellipse(
                [self.target_x - TARGET_RADIUS, self.target_y - TARGET_RADIUS,
                 self.target_x + TARGET_RADIUS, self.target_y + TARGET_RADIUS],
                outline="red", width=5
            )

            self.current_img = ctk.CTkImage(light_image=img, dark_image=img, size=(CAM_W, CAM_H))
            self.video_label.configure(image=self.current_img)

        self.after(15, self.update_frame)


if __name__ == "__main__":
    app = BoxingApp()
    app.mainloop()