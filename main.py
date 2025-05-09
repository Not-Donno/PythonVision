import cv2
import mediapipe as mp
import math

def call_func():
    print("HEIL DONNO")

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
mp_draw = mp.solutions.drawing_utils

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    points = []
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            h, w, c = frame.shape
            cx = int(hand_landmarks.landmark[9].x * w)
            cy = int(hand_landmarks.landmark[9].y * h)
            points.append((cx, cy))
            cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)
    if len(points) == 2:
        cv2.line(frame, points[0], points[1], (255, 0, 0), 3)
        dist = math.hypot(points[0][0] - points[1][0], points[0][1] - points[1][1])
        signal = 0 if dist < 50 else dist
        cv2.putText(frame, f'Signal: {int(signal)}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        if signal < 150:
            call_func()
    cv2.imshow('Donno Daddy', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
