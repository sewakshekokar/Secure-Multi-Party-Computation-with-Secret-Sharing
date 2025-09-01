import socket, json

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

# Receive x0, y0 from P3
conn_p3, _ = srv.accept()
vals = recv_json(conn_p3)
x1 = vals['x1']
y1 = vals['y1']
print("[P1] x1=",x1)
print("[P1] y1=",y1)
conn_p3.close()

# Receive Beaver triple from p2
conn_p2, address = srv.accept()
data = recv_json(conn_p2)
a1 = data['a1']
b1 = data['b1']
c1 = data['c1']
print("[P1] a1,b1,c1 =",a1,b1,c1)
conn_p2.close()

# Compute d1, e1 
d1 = x1 - a1
e1 = y1 - b1
print("[P1] d1,e1 =", d1, e1)

# Receive d0,e0 from P0 
conn_p0, address = srv.accept()
de_rev = recv_json(conn_p0)
d0 = de_rev['d0']
e0 = de_rev['e0']


# send d1 and e1 to p0
send_json(conn_p0, {'d1': d1, 'e1': e1})
conn_p0.close()

# Compute d,e
d = d0 + d1
e = e0 + e1

z1 = c1 + d * b1 + e * a1  

print("[P1] z1 =", z1)

srv.close()
