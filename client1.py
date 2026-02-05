import socket
import cv2
import struct
import time

SERVER_HOST = "your-app-name.herokuapp.com"
SERVER_PORT = 443   # Heroku TCP via proxy

WIDTH = 640
HEIGHT = 480
JPEG_QUALITY = 30

sock = socket.create_connection((SERVER_HOST, SERVER_PORT))
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

print("▶ TX connesso al relay")

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

frames = 0
t0 = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    ok, enc = cv2.imencode(
        ".jpg", frame,
        [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY]
    )
    if not ok:
        continue

    data = enc.tobytes()
    header = struct.pack("!I", len(data))

    sock.sendall(header + data)

    frames += 1
    if time.time() - t0 >= 1:
        print(f"[TX] FPS={frames}")
        frames = 0
        t0 = time.time()

    if cv2.waitKey(1) == 27:
        break

cap.release()
sock.close()
