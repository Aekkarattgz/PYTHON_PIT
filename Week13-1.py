import cv2 # OpenCV
import mediapipe as mp #ใช้ตรวจจับมือและตำแหน่งข้อต่าง ๆ ของมือ

mp_hands = mp.solutions.hands # เรียกใช้งานส่วน Hands ของ MediaPipe
hands = mp_hands.Hands(min_detection_confidence=0.7, max_num_hands=2)  # กำหนดความมั่นใจขั้นต่ำในการตรวจจับมือ 2 มือ
mp_draw = mp.solutions.drawing_utils # สร้าง Landmark บนภาพ

# จุดปลายนิ้ว และข้อนิ้วที่ใช้เทียบ (ตามลำดับ: โป้ง, ชี้, กลาง, นาง, ก้อย)
TIP_IDS = [4, 8, 12, 16, 20]
PIP_IDS = [3, 6, 10, 14, 18]

cap = cv2.VideoCapture(0) # เปิดกล้องตัวที่ 0

while True:
    # อ่านภาพจากกล้อง 1 Frame ret = อ่านภาพสำเร็จหรือไม่ frame = ภาพที่อ่านได้
    ret, frame = cap.read()
    if not ret:
        break
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)   # ส่วนที่ 6 : แปลงสีภาพ
    results = hands.process(rgb) # ส่งภาพเข้า MediaPipe Hands

    finger_count = 0   # รวมนิ้วจากทุกมือ เริ่มนับก่อนเข้าลูป

    if results.multi_hand_landmarks: # ถ้า MediaPipe ตรวจพบมือ
        # วนดูมือแต่ละข้างที่ตรวจพบ idx = ลำดับของมือ
        # hand_landmarks = จุด Landmark ของมือนั้น
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # วาดจุดและเส้น Landmark ลงบนภาพ
            #enumerate() คือฟังก์ชันในตัวที่ใช้เพิ่มตัวนับหรือดัชนี (Index) ให้กับข้อมูลที่วนซ้ำได้
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # อ่านว่าเป็นมือ Left หรือ Right
            label = results.multi_handedness[idx].classification[0].label
            lm = hand_landmarks.landmark  # เก็บ Landmark ทั้งหมดของมือนี้
            fingers_up = [] 

            # นิ้วโป้ง: ทิศทางกลับกันระหว่างมือซ้าย-ขวา ต้องเช็ค label ด้วย
            if label == "Right":
                fingers_up.append(1 if lm[TIP_IDS[0]].x < lm[PIP_IDS[0]].x else 0)
            # ถ้าเป็นมือซ้าย ให้เช็คทิศทางกลับกัน
            else: 
                fingers_up.append(1 if lm[TIP_IDS[0]].x > lm[PIP_IDS[0]].x else 0)

            # นิ้วที่เหลือ: เทียบแกน y (ปลายนิ้วอยู่สูงกว่าข้อ = เหยียด)
            for i in range(1, 5):
                if lm[TIP_IDS[i]].y < lm[PIP_IDS[i]].y:
                    fingers_up.append(1)
                else:
                    fingers_up.append(0)

            finger_count += sum(fingers_up)   # บวกสะสม ไม่ใช่เขียนทับ

    cv2.putText(frame, f"Fingers: {finger_count}", (30, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

    cv2.imshow("Finger Counter", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()