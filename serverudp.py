import socket
import os
import struct

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 5000))

print("🚀 Server TCP avviato", flush=True)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)

print(f"✅ In ascolto su porta {PORT}", flush=True)

conn, addr = sock.accept()
print(f"🔌 Client connesso da {addr}", flush=True)

while True:
    header = conn.recv(4)
    if not header:
        print("❌ Client disconnesso", flush=True)
        break

    size = struct.unpack("!I", header)[0]

    data = b""
    while len(data) < size:
        packet = conn.recv(size - len(data))
        if not packet:
            break
        data += packet

    print(f"[RX] Frame ricevuto: {len(data)} byte", flush=True)

conn.close()
sock.close()
