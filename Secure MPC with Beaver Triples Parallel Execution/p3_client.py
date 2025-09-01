import socket
import json
import random
import time


HOST = '127.0.0.1'
PORT_P0 = 6000
PORT_P1 = 6001
PORT_P3 = 7000
SLOTS = 2 # Number of multiplication in parallel

def send_json(conn, obj):
    conn.sendall(json.dumps(obj).encode())

def recv_json(conn):
    return json.loads(conn.recv(4096).decode())

x, y = [], []

for i in range(SLOTS):
    xi = random.randint(10**5, 10**6)
    yi = random.randint(10**5, 10**6)
    x.append(xi)
    y.append(yi)

print("\n[P3] 1st Multiplication:")
print(f"[P3] x={x[0]}, y={y[0]}, \nproduct={x[0]*y[0]}")
print("\n[P3] 2nd Multiplication:")
print(f"[P3] x={x[1]}, y={y[1]}, \nproduct={x[1]*y[1]}")


x0, x1, y0, y1 = [], [], [], []
for i in range(SLOTS):
    xi0 = random.randint(1, x[i])
    yi0 = random.randint(1, y[i])
    x0.append(xi0); x1.append(x[i]-xi0)
    y0.append(yi0); y1.append(y[i]-yi0)

# Send Share of x and y to p0
s0 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s0.connect((HOST, PORT_P0))
send_json(s0, {'x0': x0, 'y0': y0})
s0.close()

# Send Share of x and y to p1
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect((HOST, PORT_P1))
send_json(s1, {'x1': x1, 'y1': y1})
s1.close()

# The results of two multiplication 
z0 = z1 = None

start = time.time() # Timer Start

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind((HOST, PORT_P3))
srv.listen(2)   # accepting 2 connections from P0 and P1

for i in range(2):   
    conn, address = srv.accept()
    data = recv_json(conn)
    if "z0" in data: 
        z0 = data["z0"]
    if "z1" in data: 
        z1 = data["z1"]
    conn.close()

srv.close()

end = time.time()

z = [z0[i] + z1[i] for i in range(SLOTS)]

print("\n[P3] Final results:", z)
print(f"\n[P3] Latency = {(end-start)*1000:.2f} ms\n")
