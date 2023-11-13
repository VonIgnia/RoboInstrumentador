import cv2
import numpy as np

# all_camera_idx_available = []

# for camera_idx in range(10):
#     cap = cv2.VideoCapture(camera_idx)
#     if cap.isOpened():
#         print(f'Camera index available: {camera_idx}')
#         all_camera_idx_available.append(camera_idx)
#         cap.release()

cap = cv2.VideoCapture("/dev/video1")

while True:
    ret, frame = cap.read()
    if ret:
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()