import cv2

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
font=cv2.FONT_HERSHEY_SIMPLEX
org = (50, 100)
x = 0

while cv2.waitKey(1) != ord('q'):
    ret, frame = capture.read()
    frame = cv2.flip(frame, 1)
    frame = frame[80:640, :]
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    y_filter = cv2.inRange(hsv, (5, 150, 130), (9, 255, 250))
    yellow = cv2.bitwise_and(hsv, hsv, mask=y_filter)

    yellow = cv2.cvtColor(yellow, cv2.COLOR_HSV2BGR)
    yellow = cv2.cvtColor(yellow, cv2.COLOR_BGR2GRAY)

    ret, yellow = cv2.threshold(yellow, 1, 255, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    yellow = cv2.morphologyEx(yellow, cv2.MORPH_OPEN, kernel, iterations=10)
    yellow = cv2.morphologyEx(yellow, cv2.MORPH_OPEN, kernel, iterations=5)

    contours, hierarchy = cv2.findContours(yellow, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        M = cv2.moments(cnt)

        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        x = cx

        cv2.circle(frame, (cx, cy), 5, (0, 0, 0), -1)
        cv2.circle(yellow, (cx, cy), 5, (0, 0, 0), -1)

    cv2.putText(frame, f"{x}", org, font, 1, (255, 0, 0), 2)

    cv2.imshow("VideoFramei", frame)
    cv2.imshow("VideoFrame", yellow)

capture.release()
cv2.destroyAllWindows()