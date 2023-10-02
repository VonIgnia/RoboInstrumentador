import cv2
#import mediapipe

print (cv2.__version__)

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if ret:
        cv2.imshow('frame', frame)
        if cv2.waitkey(1):
            break
    else:
        print("no return")

cap.release()
cv2.destroyAllWindows()