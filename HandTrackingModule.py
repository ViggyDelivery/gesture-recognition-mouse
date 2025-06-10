import cv2
import mediapipe as mp
import time
import pyautogui as gui
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class HandDetector:
    def __init__(self, mode=False, max_hands=1, complexity=1, min_detect=0.5, min_track=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.complexity = complexity
        self.min_detect = min_detect
        self.min_track = min_track
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.max_hands, self.complexity, self.min_detect, self.min_track)
        self.mpDraw = mp.solutions.drawing_utils
        self.tips = [4, 8, 12, 16, 20]
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw and (id in self.tips):
                    cv2.circle(img, (cx, cy), 8, (255, 0, 255), cv2.FILLED)
        return lmList

    def distance(self, x1, y1, x2, y2):
        xVal = (x2 - x1) ** 2
        yVal = (y2 - y1) ** 2
        return int(math.sqrt(xVal + yVal))

    def click(self, x1, y1, x2, y2):
        if self.distance(x1, y1, x2, y2) < 23:
            gui.click()

    def volumeUp(self, x1, y1, x2, y2):
        if self.distance(x1, y1, x2, y2) < 23 and self.volume.GetMasterVolumeLevel() < 0.0:
            currentVolume = self.volume.GetMasterVolumeLevel()
            self.volume.SetMasterVolumeLevel(currentVolume + 1.04167, None)

    def volumeDown(self, x1, y1, x2, y2):
        if self.distance(x1, y1, x2, y2) < 23 and self.volume.GetMasterVolumeLevel() < 0.0:
            currentVolume = self.volume.GetMasterVolumeLevel()
            self.volume.SetMasterVolumeLevel(currentVolume - 1.04167, None)

    def cursor(self, img, x1, y1):
        self.frameHeight, self.frameWidth, _ = img.shape
        gui.moveTo(x1 * 1920 / self.frameWidth, y1 * 1080 / self.frameHeight)

def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    cTime = 0
    detector = HandDetector()
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            detector.click(lmList[4][1], lmList[4][2], lmList[8][1], lmList[8][2])
            detector.volumeUp(lmList[4][1], lmList[4][2], lmList[12][1], lmList[12][2])
            detector.volumeDown(lmList[4][1], lmList[4][2], lmList[16][1], lmList[16][2])
            detector.cursor(img, lmList[8][1], lmList[8][2])
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
