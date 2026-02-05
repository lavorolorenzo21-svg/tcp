import socket
import cv2
import struct
import time
import numpy as np

SERVER_HOST = "your-app-name.herokuapp.com"
SERVER_PORT = 443

sock = socket.create_connection((SERVER_HOST, SERVER_PORT))
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

print("▶ RX connesso al relay")

frames = 0
t0 = time.time()

while True:
    header = sock.recv(4)
    if not header:
        break

    size = struct.unpack("!I", header)[0]

    data = b""
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            break
        data += packet

    frame = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    if frame is None:
        continue

    cv2.imshow("RX Video", frame)

    frames += 1
    if time.time() - t0 >= 1:
        print(f"[RX] FPS={frames}")
        frames = 0
        t0 = time.time()

    if cv2.waitKey(1) == 27:
        break

sock.close()
cv2.destroyAllWindows()
