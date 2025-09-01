import socket, json, hashlib

HOST='127.0.0.1'
PORT_P0=6000
PORT_P1=6001
PORT_P2=6002



# Field modulus (large prime). If you want plain ints, set Q=0
Q = 1_000_000_007
def modq(x): return x % Q if Q else x

def recv_json(conn): 
    return json.loads(conn.recv(65536).decode())
def send_json(sock,obj): 
    sock.sendall(json.dumps(obj).encode())

def PRG_hex(key_hex, ctr):
    """Pseudo-random generator: SHA256(key||ctr) -> int mod Q"""
    key = bytes.fromhex(key_hex)
    h = hashlib.sha256(key + ctr.to_bytes(8,'big')).digest()
    return int.from_bytes(h[:8], 'big') % (Q if Q else (1 << 61))


print("[P1] listening on", PORT_P1)
srv=socket.socket()
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind((HOST,PORT_P1))
srv.listen(5)

conn,_=srv.accept()
input=recv_json(conn)
conn.close()

x1 = input["x_i"]
x2 = input["x_ip1"]
y1 = input["y_i"]
y2 = input["y_ip1"]
k_self = input["k_self"]    # k0 shared with P1
k_prev = input["k_prev"]    # k2 shared with P2
ctr    = input["ctr"]
print(f"[P1] shares x1={x1}, x2={x2}, y1={y1}, y2={y2}, ctr={ctr}")

z1 = modq(x1*y1 + x1*y2 + x2*y1)

phi1 = modq(PRG_hex(k_self, ctr) - PRG_hex(k_prev, ctr))
z1m = modq(z1 + phi1)
print(f"[P1] z1={z1}, phi1={phi1}, z1'={z1m}")

# Send LEFT to P0
s=socket.socket()
s.connect((HOST,PORT_P0))
send_json(s, {"from":"P1","z_masked":z1m})
s.close()

# Receive RIGHT from P2
conn,_=srv.accept(); msg=recv_json(conn)
conn.close()
assert msg["from"]=="P2"
z2m = msg["z_masked"]
print(f"[P1] replicated product shares = (z1'={z1m}, z2'={z2m})")

srv.close()
