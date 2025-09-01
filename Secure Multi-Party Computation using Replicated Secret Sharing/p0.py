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


srv=socket.socket()
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind((HOST,PORT_P0))
srv.listen(5)
print("[P0] listening on", PORT_P0)

# Receive shares + phi0 from client
conn,address=srv.accept()
input=recv_json(conn)
conn.close()

x0 = input["x_i"]
x1 = input["x_ip1"]
y0 = input["y_i"]
y1 = input["y_ip1"]
k_self = input["k_self"]    # k0 shared with P1
k_prev = input["k_prev"]    # k2 shared with P2
ctr    = input["ctr"]

print(f"[P0] shares x0={x0}, x1={x1}, y0={y0}, y1={y1}, ctr={ctr}")

# Local multiplication (3 terms)
z0 = modq(x0*y0 + x0*y1 + x1*y0)

# Zero-sharing with PRG
phi0 = modq(PRG_hex(k_self, ctr) - PRG_hex(k_prev, ctr))
z0m = modq(z0 + phi0)
print(f"[P0] z0={z0}, phi0={phi0}, z0'={z0m}")

# Send masked to LEFT (P2)
s=socket.socket() 
s.connect((HOST,PORT_P2))
send_json(s, {"from":"P0","z_masked":z0m})
s.close()

# Receive masked from RIGHT (P1)
conn,_=srv.accept()
input=recv_json(conn)
conn.close()
assert input["from"]=="P1"
z1m = input["z_masked"]
print(f"[P0] replicated product shares = (z0'={z0m}, z1'={z1m})")

srv.close()
