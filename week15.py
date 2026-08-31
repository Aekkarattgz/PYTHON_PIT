import customtkinter as ctk
import cv2
from PIL import Image
from tkinter import filedialog
from inference_sdk import InferenceHTTPClient
import threading
import time


# ---------------- Roboflow ----------------
API_KEY = "6FtNkcbQXhver54UVFeC"
MODEL_ID = "test-x223k/find-cola-and-pepsi-2-rfdetr-small-t1"

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key=API_KEY
)


# ---------------- GUI ----------------
ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.geometry("900x700")
app.title("Cola Pepsi Detection")


title = ctk.CTkLabel(
    app,
    text="Cola & Pepsi Detection",
    font=("Arial", 28, "bold")
)
title.pack(pady=15)


image_label = ctk.CTkLabel(
    app,
    text="เลือกเปิดกล้อง หรืออัปโหลดภาพ"
)
image_label.pack(pady=10)


status = ctk.CTkLabel(
    app,
    text="พร้อมใช้งาน",
    font=("Arial", 16)
)
status.pack(pady=10)


cap = None
camera_on = False

predictions = []
detecting = False
last_detect = 0


# ============================================================
# วาดกรอบ
# ============================================================

def draw_boxes(frame, preds):

    for p in preds:

        x = p["x"]
        y = p["y"]
        w = p["width"]
        h = p["height"]

        name = p["class"]
        conf = p["confidence"]

        x1 = int(x - w / 2)
        y1 = int(y - h / 2)
        x2 = int(x + w / 2)
        y2 = int(y + h / 2)

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        text = f"{name} {conf * 100:.1f}%"

        cv2.putText(
            frame,
            text,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    return frame


# ============================================================
# แสดงภาพบน CustomTkinter
# ============================================================

def show_image(frame):

    frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    img = Image.fromarray(frame)

    img.thumbnail((800, 500))

    ctk_img = ctk.CTkImage(
        light_image=img,
        dark_image=img,
        size=img.size
    )

    image_label.configure(
        image=ctk_img,
        text=""
    )

    # เก็บ reference
    image_label.image = ctk_img


# ============================================================
# AI ตรวจภาพจากกล้อง
# ============================================================

def detect_camera(frame):

    global predictions
    global detecting

    try:

        result = client.infer(
            frame,
            model_id=MODEL_ID
        )

        predictions = result["predictions"]

        app.after(
            0,
            lambda: status.configure(
                text=f"ตรวจพบ {len(predictions)} วัตถุ"
            )
        )

    except Exception as e:

        print("ERROR:", e)

    detecting = False


# ============================================================
# Webcam
# ============================================================

def update_camera():

    global last_detect
    global detecting

    if not camera_on:
        return

    ret, frame = cap.read()

    if not ret:
        return

    # ----------------------------
    # AI ตรวจทุก 0.8 วินาที
    # ----------------------------

    now = time.time()

    if now - last_detect > 0.8 and not detecting:

        detecting = True
        last_detect = now

        frame_ai = frame.copy()

        threading.Thread(
            target=detect_camera,
            args=(frame_ai,),
            daemon=True
        ).start()

    # ----------------------------
    # วาดผลล่าสุด
    # ----------------------------

    frame = draw_boxes(
        frame,
        predictions
    )

    show_image(frame)

    # กล้องประมาณ 30 FPS
    app.after(
        30,
        update_camera
    )


# ============================================================
# เปิดกล้อง
# ============================================================

def open_camera():

    global cap
    global camera_on
    global predictions

    if camera_on:
        return

    predictions = []

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():

        status.configure(
            text="เปิดกล้องไม่ได้"
        )

        return

    camera_on = True

    status.configure(
        text="เปิดกล้องแล้ว"
    )

    update_camera()


# ============================================================
# หยุดกล้อง
# ============================================================

def stop_camera():

    global camera_on
    global cap

    camera_on = False

    if cap:

        cap.release()
        cap = None

    status.configure(
        text="หยุดกล้องแล้ว"
    )


# ============================================================
# Upload Image
# ============================================================

def upload_image():

    stop_camera()

    path = filedialog.askopenfilename(
        filetypes=[
            (
                "Image",
                "*.jpg *.jpeg *.png *.bmp"
            )
        ]
    )

    if not path:
        return

    status.configure(
        text="กำลังตรวจสอบ..."
    )

    app.update()

    # อ่านรูป
    frame = cv2.imread(path)

    if frame is None:

        status.configure(
            text="อ่านรูปไม่ได้"
        )

        return

    try:

        # ส่งรูปให้ AI
        result = client.infer(
            path,
            model_id=MODEL_ID
        )

        preds = result["predictions"]

        # วาดกรอบ
        frame = draw_boxes(
            frame,
            preds
        )

        # แสดงรูป
        show_image(frame)

        status.configure(
            text=f"ตรวจพบ {len(preds)} วัตถุ"
        )

    except Exception as e:

        print(e)

        status.configure(
            text="เรียก Model ไม่สำเร็จ"
        )


# ============================================================
# Buttons
# ============================================================

button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10)


btn_camera = ctk.CTkButton(
    button_frame,
    text="📷 เปิดกล้อง",
    command=open_camera,
    width=180,
    height=45
)

btn_camera.grid(
    row=0,
    column=0,
    padx=10
)


btn_upload = ctk.CTkButton(
    button_frame,
    text="🖼 อัปโหลดภาพ",
    command=upload_image,
    width=180,
    height=45
)

btn_upload.grid(
    row=0,
    column=1,
    padx=10
)


btn_stop = ctk.CTkButton(
    button_frame,
    text="⏹ หยุดกล้อง",
    command=stop_camera,
    width=180,
    height=45
)

btn_stop.grid(
    row=0,
    column=2,
    padx=10
)


# ============================================================
# Run
# ============================================================

app.mainloop()