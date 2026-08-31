import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# ช่วงสีแดงสำหรับ HSV
lower_red1 = np.array([0, 120, 70])   
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([180, 255, 255])

# ช่วงสีแดงสำหรับ RGB (R สูง, G ต่ำ, B ต่ำ)
lower_red_rgb = np.array([100, 0, 0])  
upper_red_rgb = np.array([255, 80, 80])

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # mask จาก HSV (แม่นกว่า)
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_hsv = cv2.bitwise_or(mask1, mask2)

    # mask จาก RGB โดยตรง (เทียบให้เห็นว่าไม่เสถียรเท่า)
    mask_rgb = cv2.inRange(rgb, lower_red_rgb, upper_red_rgb)

    cv2.imshow("1. Original (BGR)", frame)
    cv2.imshow("2. HSV", hsv)
    cv2.imshow("3. RGB", rgb)
    cv2.imshow("Mask - HSV (แม่นกว่า)", mask_hsv)
    cv2.imshow("Mask - RGB (เทียบ)", mask_rgb)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()