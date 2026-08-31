import cv2                          # เรียกใช้ OpenCV สำหรับจัดการภาพ/กล้อง
import mediapipe as mp              # เรียกใช้ MediaPipe สำหรับตรวจจับร่างกาย
mp_pose = mp.solutions.pose         # ดึงโมดูล Pose ออกมาจาก MediaPipe
pose = mp_pose.Pose(min_detection_confidence=0.7)
                                     # สร้างโมเดล Pose พร้อมตั้งเกณฑ์ความมั่นใจขั้นต่ำ 0.7 (70%)
                                     # ถ้าโมเดลมั่นใจน้อยกว่านี้ จะถือว่ายังไม่เจอคน
mp_draw = mp.solutions.drawing_utils
                                     # ดึงเครื่องมือช่วยวาดจุด/เส้นลงบนภาพ
cap = cv2.VideoCapture(0)           # เปิดกล้อง (0 = กล้องตัวแรกของเครื่อง)
while True:                         # วนลูปอ่านภาพทีละเฟรมไปเรื่อยๆ
    ret, frame = cap.read()         # อ่าน 1 เฟรมจากกล้อง
                                     # ret = True/False ว่าอ่านสำเร็จไหม, frame = ภาพที่ได้
    if not ret:                     # ถ้าอ่านภาพไม่สำเร็จ (เช่น กล้องหลุด)
        break                       # ออกจากลูปทันที
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                     # แปลงสีภาพจาก BGR (ที่ OpenCV ใช้) เป็น RGB
                                     # เพราะ MediaPipe ต้องการภาพแบบ RGB เท่านั้น
    results = pose.process(rgb)     # ส่งภาพ RGB เข้าโมเดล Pose
                                     # ได้ผลลัพธ์เป็นตำแหน่ง landmark ทั้งหมด (หรือ None ถ้าไม่เจอคน)
    if results.pose_landmarks:      # ถ้าตรวจเจอคนในเฟรม (มี landmark ส่งกลับมา)
        mp_draw.draw_landmarks(
            frame, results.pose_landmarks,
                                     # วาดจุด landmark ทั้งหมดลงบน frame (ภาพต้นฉบับ ไม่ใช่ rgb)
            mp_pose.POSE_CONNECTIONS
                                     # เส้นเชื่อมทั้งตัว บอกว่าจุดไหนต้องต่อกับจุดไหน
                                     # เช่น ไหล่ต่อกับข้อศอก ข้อศอกต่อกับข้อมือ
        )
    cv2.imshow("Pose Tracking", frame)
                                     # แสดงภาพผลลัพธ์ในหน้าต่างชื่อ "Pose Tracking"
    if cv2.waitKey(1) & 0xFF == ord("q"):
                                     # รอกดคีย์บอร์ด 1 มิลลิวินาที
                                     # ถ้ากดปุ่ม "q" ให้ออกจากลูป
        break
cap.release()                       # ปิดการใช้งานกล้อง คืนทรัพยากรให้ระบบ
cv2.destroyAllWindows()             # ปิดหน้าต่างแสดงภาพทั้งหมดที่เปิดไว้