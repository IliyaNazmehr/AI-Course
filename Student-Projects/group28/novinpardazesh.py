import cv2 as cv
import numpy as np

# =========================
# CVZONE MODULES
# =========================
from cvzone.FaceDetectionModule import FaceDetector
from cvzone.FaceMeshModule import FaceMeshDetector

# =========================
# HAAR CASCADE LOAD
# =========================
face_cascade = cv.CascadeClassifier(
    cv.data.haarcascades + "haarcascade_frontalface_default.xml"
)
eye_cascade = cv.CascadeClassifier(
    cv.data.haarcascades + "haarcascade_eye.xml"
)
smile_cascade = cv.CascadeClassifier(
    cv.data.haarcascades + "haarcascade_smile.xml"
)

# =========================
# CAMERA INITIALIZATION
# =========================
cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

# =========================
# CVZONE DETECTORS
# =========================
face_detector = FaceDetector(minDetectionCon=0.6, modelSelection=0)
mesh_detector = FaceMeshDetector(maxFaces=1)

# =========================
# MAIN LOOP
# =========================
while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera error")
        break

    # =========================
    # PREPROCESSING
    # =========================
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # =========================
    # HAAR FACE DETECTION
    # =========================
    faces_haar = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(60, 60)
    )

    for (x, y, w, h) in faces_haar:
        cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)

        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        # -------------------------
        # EYE DETECTION
        # -------------------------
        eyes = eye_cascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.1,
            minNeighbors=10,
            minSize=(20, 20)
        )
        for (ex, ey, ew, eh) in eyes:
            cv.rectangle(
                roi_color,
                (ex, ey),
                (ex + ew, ey + eh),
                (0, 255, 0),
                2
            )

        # -------------------------
        # SMILE DETECTION (LOWER FACE)
        # -------------------------
        smiles = smile_cascade.detectMultiScale(
            roi_gray[h // 2:, :],
            scaleFactor=1.7,
            minNeighbors=25,
            minSize=(25, 25)
        )

        for (sx, sy, sw, sh) in smiles:
            cv.rectangle(
                roi_color,
                (sx, sy + h // 2),
                (sx + sw, sy + sh + h // 2),
                (0, 0, 255),
                2
            )

    # =========================
    # CVZONE FACE DETECTION
    # =========================
    frame, bboxs = face_detector.findFaces(frame, draw=True)

    if bboxs:
        face_info = bboxs[0]
        cx, cy = face_info["center"]
        score = int(face_info["score"][0] * 100)

        cv.circle(frame, (cx, cy), 6, (255, 0, 0), cv.FILLED)
        cv.putText(
            frame,
            f"Confidence: {score}%",
            (cx - 80, cy - 20),
            cv.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 0, 0),
            2
        )

    # =========================
    # FACE MESH DETECTION
    # =========================
    frame, faces = mesh_detector.findFaceMesh(frame, draw=True)

    if faces:
        face = faces[0]

        # -------------------------
        # SAMPLE LANDMARKS
        # -------------------------
        left_eye = face[33]
        right_eye = face[263]
        nose_tip = face[1]
        mouth_left = face[61]
        mouth_right = face[291]

        cv.circle(frame, left_eye, 3, (0, 255, 255), cv.FILLED)
        cv.circle(frame, right_eye, 3, (0, 255, 255), cv.FILLED)
        cv.circle(frame, nose_tip, 3, (255, 255, 0), cv.FILLED)

        cv.line(frame, mouth_left, mouth_right, (0, 255, 0), 2)

    # =========================
    # DISPLAY
    # =========================
    cv.imshow("Hybrid Face Analysis System", frame)

    key = cv.waitKey(1) & 0xFF
    if key == 27:
        break

# =========================
# CLEANUP
# =========================
cap.release()
cv.destroyAllWindows()
