import socket
import os
import struct
import threading
import time

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 5000))

print("🚀 Server RELAY avviato", flush=True)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(2)

print(f"✅ In ascolto su porta {PORT}", flush=True)

clients = []

def handle_client(conn, addr):
    print(f"🔌 Client connesso: {addr}", flush=True)
    clients.append(conn)

    try:
        while True:
            header = conn.recv(4)
            if not header:
                break

            size = struct.unpack("!I", header)[0]
            data = b""
            while len(data) < size:
                packet = conn.recv(size - len(data))
                if not packet:
                    return
                data += packet

            # inoltra a tutti tranne il mittente
            for c in clients:
                if c != conn:
                    c.sendall(header + data)

    except Exception as e:
        print("❌ Errore client:", e, flush=True)
    finally:
        clients.remove(conn)
        conn.close()
        print(f"❌ Client disconnesso: {addr}", flush=True)

while True:
    conn, addr = sock.accept()
    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
