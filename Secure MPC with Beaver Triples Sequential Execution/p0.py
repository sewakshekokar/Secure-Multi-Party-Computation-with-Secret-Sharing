import socket, json, time

HOST = '127.0.0.1'
PORT_P0 = 6000  
PORT_P1 = 6001  

def recv_json(conn):
    return json.loads(conn.recv(1024).decode())

def send_json(conn, obj):
    conn.sendall(json.dumps(obj).encode())

# Create Socket
srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind((HOST, PORT_P0))
srv.listen(5)
print("[P0] Listening on", PORT_P0)

# Receive x0,y0,y0_next from P3
conn_p3, _ = srv.accept()
vals = recv_json(conn_p3)
x0 = vals['x0']
y0 = vals['y0']
y0_next = vals['y0_next']
conn_p3.close()

# Receive Beaver triple from P2
conn_p2, _ = srv.accept()
data = recv_json(conn_p2)
a0 = data['a0']
b0 = data['b0']
c0 = data['c0']
print("[P0] Beaver triple =", a0,b0,c0)
conn_p2.close()

# --------- First Multiplication ----------
print("\n[P0] --- First Multiplication ---")
start = time.time()  

print("[P0] x0 =",x0)
print("[P0] y0 =",y0)

# Compute d0 and e0
d0 = x0 - a0
e0 = y0 - b0

# Send d0 and e0 to p1
conn_p1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn_p1.connect((HOST, PORT_P1))
send_json(conn_p1, {'d0': d0, 'e0': e0})

# Receive d1 and e1 from p1
de_rev = recv_json(conn_p1)
d1 = de_rev['d1']
e1 = de_rev['e1']

# Compute d and e
d = d0 + d1
e = e0 + e1

# Compute z0
z0 = c0 + d * b0 + e * a0 + d * e
print("[P0] z0 =", z0)
conn_p1.close()


# send z0 and get z1
conn_p1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn_p1.connect((HOST, PORT_P1))
send_json(conn_p1, {'z0': z0})
z1 = recv_json(conn_p1)['z1']
conn_p1.close()

z_first = z0 + z1
print("[P0] z =", z_first)

# ------------ Second Multiplication ------------
print("\n[P0] --- Second Multiplication ---")
x0 = z0
y0 = y0_next

print("[P0] x0 =",x0)
print("[P0] y0 =",y0_next)

# Compute d0 and e0
d0 = x0 - a0
e0 = y0 - b0

# Send d0 and e0 to p1
conn_p1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn_p1.connect((HOST, PORT_P1))
send_json(conn_p1, {'d0': d0, 'e0': e0})

# Receive d1 and e1 from p1
de_rev = recv_json(conn_p1)
d1 = de_rev['d1']
e1 = de_rev['e1']
d = d0 + d1
e = e0 + e1
z0 = c0 + d * b0 + e * a0 + d * e
print("[P0] z0 =", z0)
conn_p1.close()

# send z0 and get z1
conn_p1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn_p1.connect((HOST, PORT_P1))
send_json(conn_p1, {'z0': z0})
z1 = recv_json(conn_p1)['z1']
conn_p1.close()

z_second = z0 + z1
print("[P0] z =", z_second)


end = time.time()  
latency = (end - start) * 1000   
print(f"\n[P0] latency = {latency:.3f} ms\n")

conn_p1.close()
srv.close()
