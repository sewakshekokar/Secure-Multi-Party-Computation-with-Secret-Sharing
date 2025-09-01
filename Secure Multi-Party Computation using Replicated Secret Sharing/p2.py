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


print("[P2] listening on", PORT_P2)
srv=socket.socket()
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind((HOST,PORT_P2))
srv.listen(5)

conn,_=srv.accept()
input=recv_json(conn)
conn.close()

x2,x0 = input["x_i"], input["x_ip1"]
y2,y0 = input["y_i"], input["y_ip1"]
k_self = input["k_self"]    # k0 shared with P1
k_prev = input["k_prev"]    # k2 shared with P2
ctr    = input["ctr"]

print(f"[P2] shares x2={x2}, x0={x0}, y2={y2}, y0={y0}, ctr={ctr}")

z2 = modq(x2*y2 + x2*y0 + x0*y2)

phi2 = modq(PRG_hex(k_self, ctr) - PRG_hex(k_prev, ctr))
z2m = modq(z2 + phi2)

print(f"[P2] z2={z2}, phi2={phi2}, z2'={z2m}")

# Send LEFT to P1
s=socket.socket()
s.connect((HOST,PORT_P1))
send_json(s, {"from":"P2","z_masked":z2m})
s.close()

# Receive RIGHT from P0
conn,_=srv.accept(); msg=recv_json(conn)
conn.close()
assert msg["from"]=="P0"
z0m = msg["z_masked"]
print(f"[P2] replicated product shares = (z2'={z2m}, z0'={z0m})")

srv.close()
