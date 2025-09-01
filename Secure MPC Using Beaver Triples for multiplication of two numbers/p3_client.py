import socket, json, random

HOST = '127.0.0.1'
PORT_P0 = 6000
PORT_P1 = 6001

def send_json(conn, obj):
    conn.sendall(json.dumps(obj).encode())

# Generate big random x and y
x = random.randint(10**5, 10**6)  # large random number
y = random.randint(10**5, 10**6)

# Create shares
x0 = random.randint(1, x - 1)
x1 = x - x0
y0 = random.randint(1, y - 1)
y1 = y - y0

print(f"[P3] x={x}, y={y}")
print(f"[P3] Sending shares: P0 -> (x0={x0}, y0={y0}), P1 -> (x1={x1}, y1={y1})")


# Send to P0
s0 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s0.connect((HOST, PORT_P0))
send_json(s0, {'x0': x0, 'y0': y0})
s0.close()

# Send to P1
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect((HOST, PORT_P1))
send_json(s1, {'x1': x1, 'y1': y1})
s1.close()
