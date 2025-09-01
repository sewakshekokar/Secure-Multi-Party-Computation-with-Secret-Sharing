import socket, json, time

HOST = '127.0.0.1'
PORT_P1 = 6001  
PORT_P0 = 6000  

def recv_json(conn):
    return json.loads(conn.recv(1024).decode())

def send_json(conn, obj):
    conn.sendall(json.dumps(obj).encode())

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind((HOST, PORT_P1))
srv.listen(5)
print("[P1] Listening on", PORT_P1)

# Receive x1,y1,y1_next from P3
conn_p3, _ = srv.accept()
vals = recv_json(conn_p3)
x1 = vals['x1']
y1 = vals['y1']
y1_next = vals['y1_next']
conn_p3.close()

# Receive Beaver triple from P2
conn_p2, _ = srv.accept()
data = recv_json(conn_p2)
a1 = data['a1']
b1 = data['b1']
c1 = data['c1']
print("[P1] Beaver triple =", a1,b1,c1)
conn_p2.close()

# ----------------- First Multiplication -----------------
start = time.time()  # START timer

print("\n[P1] --- First Multiplication ---")

print("[P0] x1 =",x1)
print("[P0] y1 =",y1)

# Receive d0 and e0 from p0
conn_p0, _ = srv.accept()
vals = recv_json(conn_p0)
d0 = vals['d0']
e0 = vals['e0']

# Compute d1 and e1 and send to p0
d1 = x1 - a1
e1 = y1 - b1
send_json(conn_p0, {'d1': d1, 'e1': e1})

# Compute d and e
d = d0 + d1
e = e0 + e1

# Compute z1
z1 = c1 + d * b1 + e * a1
print("[P1] z1 =", z1)
conn_p0.close()

# receive z0 and send z1 back
conn_p0, _ = srv.accept()
z0 = recv_json(conn_p0)['z0']
send_json(conn_p0, {'z1': z1})
conn_p0.close()

z_first = z0 + z1
print("[P1] z  =", z_first)

# ----------------- Second Multiplication -----------------
print("\n[P1] --- Second Multiplication ---")

x1 = z1
y1 = y1_next

print("[P0] x1 =",x1)
print("[P0] y1 =",y1_next)
# Compute d1 ad e1
d1 = x1 - a1
e1 = y1 - b1

# Receive d0 and e0
conn_p0, _ = srv.accept()
vals = recv_json(conn_p0)
d0 = vals['d0']
e0 = vals['e0']

# Send d1 and e1 to p0
send_json(conn_p0, {'d1': d1, 'e1': e1})
conn_p0.close()

# Compute d and e
d = d0 + d1
e = e0 + e1

# Compute z1
z1 = c1 + d * b1 + e * a1
print("[P1] z1 =", z1)


# receive z0 and send z1 back
conn_p0, _ = srv.accept()
z0 = recv_json(conn_p0)['z0']
send_json(conn_p0, {'z1': z1})
conn_p0.close()

z_second = z0 + z1
print("[P1] z =", z_second)


end = time.time()  # END timer
latency = (end - start) * 1000   # in milliseconds
print(f"\n[P0] latency = {latency:.3f} ms\n")


conn_p0.close()
srv.close()
