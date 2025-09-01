import socket, json, random

HOST = '127.0.0.1'
PORT_P0 = 6000
PORT_P1 = 6001


def send_json(conn, obj):
    conn.sendall(json.dumps(obj).encode())

# Generate Beaver triple (a, b, c)
a = random.randint(1, 1000)  # can be small or big
b = random.randint(1, 1000)
c = a * b
print(f"[P2] Beaver triple: a={a}, b={b}, c={c}")

# Split Beaver triple into shares
a0 = random.randint(0, a)
a1 = a - a0
b0 = random.randint(0, b)
b1 = b - b0
c0 = random.randint(0, c)
c1 = c - c0


# Send to P0
s0 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s0.connect((HOST, PORT_P0))
send_json(s0, {'a0': a0, 'b0': b0, 'c0': c0})
s0.close()

# Send to P1
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect((HOST, PORT_P1))
send_json(s1, {'a1': a1, 'b1': b1, 'c1': c1})
s1.close()
