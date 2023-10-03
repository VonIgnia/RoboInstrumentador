import cv2


print (cv2.__version__)

cap = cv2.VideoCapture("rtsp://10.103.16.201:554")
print("after IP")

while True:
    ret, frame = cap.read()
    print("after capture")
    if ret:
        cv2.imshow('frame', frame)
        if cv2.waitkey(1):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()