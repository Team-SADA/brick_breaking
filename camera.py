import cv2
import numpy as np
import mediapipe as mp


class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.face_detection = mp.solutions.face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)

    def get_x(self):
        success, frame = self.cap.read()
        if not success:
            return -1
        frame = cv2.flip(frame, 1)
        # 특정한 색상의 영역 중 가장 큰 영역을 찾는다
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.face_detection.process(image)

        if results.detections:
            for detection in results.detections:
                bounding_box = detection.location_data.relative_bounding_box
                bounding_box.width *= 1.4
                bounding_box.height *= 1.4
                bounding_box.xmin -= bounding_box.width * 0.15
                bounding_box.ymin -= bounding_box.height * 0.15
                left = int(max(min(bounding_box.xmin, 1), 0) * frame.shape[1])
                top = int(max(min(bounding_box.ymin, 1), 0) * frame.shape[0])
                right = int(max(min(bounding_box.xmin + bounding_box.width, 1), 0) * frame.shape[1])
                bottom = int(max(min(bounding_box.ymin + bounding_box.height, 1), 0) * frame.shape[0])
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, "player", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
                # pos=((x_min, y_min), (x_max, y_max))

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
        self.face_detection.close()
        cv2.destroyAllWindows()
