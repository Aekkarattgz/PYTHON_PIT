import cv2                          # เรียกใช้ OpenCV สำหรับจัดการภาพ/กล้อง
import mediapipe as mp              # เรียกใช้ MediaPipe สำหรับตรวจจับร่างกาย/มือ
# เปลี่ยนมาใช้ Holistic แทน Pose
mp_holistic = mp.solutions.holistic # ดึงโมดูล Holistic (รวม Pose + มือ + ใบหน้า)
holistic = mp_holistic.Holistic(
    min_detection_confidence=0.7,   # เกณฑ์ความมั่นใจขั้นต่ำตอน "ค้นหา" คน/มือครั้งแรก
    min_tracking_confidence=0.7     # เกณฑ์ความมั่นใจขั้นต่ำตอน "ติดตาม" จุดเดิมในเฟรมถัดไป
                                     # (Pose เดี่ยวไม่มีค่านี้ เพราะ Holistic ซับซ้อนกว่า ต้องคุมทั้งสองจังหวะ)
)
mp_draw = mp.solutions.drawing_utils
                                     # ดึงเครื่องมือช่วยวาดจุด/เส้นลงบนภาพ

cap = cv2.VideoCapture(0)           # เปิดกล้อง (0 = กล้องตัวแรกของเครื่อง)
while True:                         # วนลูปอ่านภาพทีละเฟรมไปเรื่อยๆ
    ret, frame = cap.read()         # อ่าน 1 เฟรมจากกล้อง
    if not ret:                     # ถ้าอ่านภาพไม่สำเร็จ
        break                       # ออกจากลูป
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                     # แปลงสีเป็น RGB ก่อนส่งเข้าโมเดล (เหมือน Pose เดี่ยว)
    results = holistic.process(rgb) # ส่งภาพเข้าโมเดล Holistic
                                     # ได้ผลลัพธ์ 3 ส่วนพร้อมกัน: pose, left_hand, right_hand
    # 1. วาดโครงสร้างร่างกาย (Pose)
    if results.pose_landmarks:      # ถ้าเจอโครงร่างร่างกาย
        mp_draw.draw_landmarks(
            frame, results.pose_landmarks,
            mp_holistic.POSE_CONNECTIONS
                                     # เส้นเชื่อมร่างกายทั้งตัว (เหมือนใน Pose เดี่ยว)
        )
    # 2. วาดรายละเอียดมือซ้าย (Left Hand - 21 จุด)
    if results.left_hand_landmarks: # ถ้าเจอมือซ้ายในเฟรม
        mp_draw.draw_landmarks(
            frame, results.left_hand_landmarks,
            mp_holistic.HAND_CONNECTIONS
                                     # เส้นเชื่อมของมือ (นิ้วแต่ละข้อ ฝ่ามือ) — ใช้แพทเทิร์นเดียวกันทั้งสองมือ
        )
    # 3. วาดรายละเอียดมือขวา (Right Hand - 21 จุด)
    if results.right_hand_landmarks:# ถ้าเจอมือขวาในเฟรม
        mp_draw.draw_landmarks(
            frame, results.right_hand_landmarks,
            mp_holistic.HAND_CONNECTIONS
        )
    cv2.imshow("Holistic Tracking (Pose + Hands)", frame)
                                     # แสดงภาพผลลัพธ์ในหน้าต่าง
    if cv2.waitKey(1) & 0xFF == ord("q"):
                                     # กด "q" เพื่อออกจากลูป
        break
cap.release()                       # ปิดกล้อง
cv2.destroyAllWindows()             # ปิดหน้าต่างทั้งหมด