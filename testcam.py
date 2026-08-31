import cv2

# ลองเรียก /dev/video0 ก่อน
cap = cv2.VideoCapture(0) 

# หากกล้องนี้รองรับความละเอียดสูง สามารถตั้งค่าเพิ่มเติมได้
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

if not cap.isOpened():
    print("ไม่สามารถเปิดกล้องได้ ลองเปลี่ยน index เป็น 1")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("ไม่สามารถรับเฟรมภาพได้")
        break

    # แสดงผลภาพ
    cv2.imshow('Insta360 One X2', frame)

    # กด 'q' เพื่อออก
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()