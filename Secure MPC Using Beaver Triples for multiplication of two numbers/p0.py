import socket, json

HOST = '127.0.0.1'
PORT_P0 = 6000  
PORT_P1 = 6001  


def recv_json(conn):
    return json.loads(conn.recv(1024).decode())

def send_json(conn, obj):
    conn.sendall(json.dumps(obj).encode()) 


srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
srv.bind((HOST, PORT_P0)) 
srv.listen(5) 
print("[P0] Listening on", PORT_P0)


# Receive x0, y0 from P3
conn_p3, _ = srv.accept()
vals = recv_json(conn_p3)
x0 = vals['x0']
y0 = vals['y0']
print("[P0] x0=",x0)
print("[P0] y0=",y0)
conn_p3.close()


# Receive Beaver triple from p2
conn_p2, address = srv.accept()
data = recv_json(conn_p2)
a0 = data['a0']
b0 = data['b0']
c0 = data['c0']
print("[P0] a0,b0,c0 =",a0,b0,c0)
conn_p2.close()


# Compute d0, e0 
d0 = x0 - a0
e0 = y0 - b0
print("[P0] d0,e0 =", d0, e0)


# send d0 and e0 to p1
conn_p1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn_p1.connect((HOST, PORT_P1))
send_json(conn_p1, {'d0': d0, 'e0': e0})

# Receive d1,e1 from P1 
de_rev = recv_json(conn_p1)
d1 = de_rev['d1']
e1 = de_rev['e1']
conn_p1.close()

# Compute d,e 
d = d0 + d1
e = e0 + e1

z0 = c0 + d * b0 + e * a0 + d * e

print("[P0] z0 =", z0)

srv.close()
