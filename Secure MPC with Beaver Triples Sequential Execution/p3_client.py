import socket, json, random

HOST = '127.0.0.1'
PORT_P0 = 6000
PORT_P1 = 6001

def send_json(conn, obj):
    conn.sendall(json.dumps(obj).encode())

# Generate big random x, y and y_next
x = random.randint(10**5, 10**6)  # large random number
y = random.randint(10**5, 10**6)
y_next = random.randint(10**5, 10**6)

print("\n[P3] --- First Multiplication ---")
print(f"[P3] x={x}, y={y}, \nProduct={x*y}")
print("\n[P3] --- Second Multiplication ---")
print(f"[P3] x={x*y}, y={y_next}, \nProduct={x*y*y_next}\n")

# Create shares
x0 = random.randint(1, x - 1)
x1 = x - x0
y0 = random.randint(1, y - 1)
y1 = y - y0
y0_next= random.randint(1, y_next-1)
y1_next = y_next - y0_next


# Send to P0
s0 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s0.connect((HOST, PORT_P0))
send_json(s0, {'x0': x0, 'y0': y0, 'y0_next': y0_next})
s0.close()

# Send to P1
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect((HOST, PORT_P1))
send_json(s1, {'x1': x1, 'y1': y1, 'y1_next': y1_next})
s1.close()

