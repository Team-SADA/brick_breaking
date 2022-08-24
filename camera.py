import cv2
import numpy as np


class Camera:
    # def __init__(self):
    #     self.capture = cv2.VideoCapture(0)
    #     self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
    #     self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    #     self.font = cv2.FONT_HERSHEY_SIMPLEX
    #     self.org = (50, 100)
    #
    # def get_x(self):
    #     x = -1
    #     ret, frame = self.capture.read()
    #     frame = cv2.flip(frame, 1)
    #     frame = frame[80:640, :]
    #     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #     y_filter = cv2.inRange(hsv, (5, 150, 130), (9, 255, 250))
    #     yellow = cv2.bitwise_and(hsv, hsv, mask=y_filter)
    #     yellow = cv2.cvtColor(yellow, cv2.COLOR_HSV2BGR)
    #     yellow = cv2.cvtColor(yellow, cv2.COLOR_BGR2GRAY)
    #     ret, yellow = cv2.threshold(yellow, 1, 255, cv2.THRESH_BINARY)
    #     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    #     yellow = cv2.morphologyEx(yellow, cv2.MORPH_OPEN, kernel, iterations=10)
    #     yellow = cv2.morphologyEx(yellow, cv2.MORPH_OPEN, kernel, iterations=5)
    #     contours, hierarchy = cv2.findContours(yellow, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #
    #     for cnt in contours:
    #         M = cv2.moments(cnt)
    #         cx = int(M['m10'] / M['m00'])
    #         cy = int(M['m01'] / M['m00'])
    #         x = cx
    #         cv2.circle(frame, (x, cy), 5, (0, 0, 0), -1)
    #     cv2.putText(frame, f"{x}", self.org, self.font, 1, (255, 0, 0), 2)
    #     cv2.imshow("VideoFrame1", frame)
    #     return x
    #
    # def delete(self):
    #     self.capture.release()
    #     cv2.destroyAllWindows()

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    def get_x(self):
        success, frame = self.cap.read()
        if not success:
            return -1
        frame = cv2.flip(frame, 1)
        # 특정한 색상의 영역 중 가장 큰 영역을 찾는다
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower = np.array([140, 127, 127])
        middle1 = np.array([180, 255, 255])
        middle2 = np.array([0, 127, 127])
        upper = np.array([40, 255, 255])

        mask1 = cv2.inRange(hsv, lower, middle1)
        mask2 = cv2.inRange(hsv, middle2, upper)
        mask = mask1 + mask2

        blur = cv2.medianBlur(mask, 5)

        contours, hierarchy = cv2.findContours(blur, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        m = 0
        max_cnt = None
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if m < area:
                m = area
                max_cnt = cnt

        cX = -1
        new = np.zeros(blur.shape).astype(blur.dtype)
        if max_cnt is not None:
            color = [255, 255, 255]
            cv2.fillPoly(new, [max_cnt], color)

            M = cv2.moments(new)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(frame, (cX, cY), 5, (0, 0, 0), -1)
        cv2.imshow('Video Window', frame)
        return cX

    def delete(self):
        self.cap.release()
        cv2.destroyAllWindows()
