import socket
import json
import random

HOST = '127.0.0.1'
PORT_P0 = 6000
PORT_P1 = 6001
SLOTS = 2

def send_json(conn, obj):
    conn.sendall(json.dumps(obj).encode())

a, b, c = [], [], []

for i in range(SLOTS):
    ai = random.randint(10**5, 10**6)
    bi = random.randint(10**5, 10**6)
    a.append(ai)
    b.append(bi)
    c.append(ai * bi)

print("\n[P2] 1st Beaver Triples")
print(f"[P2] a={a[0]}, b={b[0]}, c={c[0]}")
print("\n[P2] 2nd Beaver Triples")
print(f"[P2] a={a[1]}, b={b[1]}, c={c[1]}")

a0, a1 = [], []
b0, b1 = [], []
c0, c1 = [], []

for i in range(SLOTS):
    ai0 = random.randint(1, a[i])
    bi0 = random.randint(1, b[i])
    ci0 = random.randint(1, c[i])

    a0.append(ai0)
    a1.append(a[i] - ai0)

    b0.append(bi0)
    b1.append(b[i] - bi0)

    c0.append(ci0)
    c1.append(c[i] - ci0)

# Send the beaver triples to p0
s0 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s0.connect((HOST, PORT_P0))
send_json(s0, {'a0': a0, 'b0': b0, 'c0': c0})
s0.close()

# Send the beaver triples to p1
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect((HOST, PORT_P1))
send_json(s1, {'a1': a1, 'b1': b1, 'c1': c1})
s1.close()
