import socket, json, random, secrets

HOST='127.0.0.1'
PORT_P0=6000
PORT_P1=6001
PORT_P2=6002

def send_json(sock,obj): sock.sendall(json.dumps(obj).encode())

def hexkey(n=16): return secrets.token_bytes(n).hex()

# Pick random inputs in [1e5, 1e6]
x = random.randint(10**5, 10**6)
y = random.randint(10**5, 10**6)

# Split x and y into shares  
x0 = random.randint(0, x)
x1 = random.randint(0, x-x0)
x2 = x - x0 - x1

y0 = random.randint(0, y)
y1 = random.randint(0, y-y0)
y2 = y - y0 - y1

# PRG seeds on ring (P0-P1), (P1-P2), (P2-P0), and gate counter
k0 = hexkey(16)   
k1 = hexkey(16)   
k2 = hexkey(16)   
ctr = 1

print(f"[P3] x={x}, y={y}, x*y={x*y}")
print(f"[P3] x-shares: {x0}, {x1}, {x2}  (sum={x0+x1+x2})")
print(f"[P3] y-shares: {y0}, {y1}, {y2}  (sum={y0+y1+y2})")
print(f"[P3] seeds: k0={k0[:8]}..  k1={k1[:8]}..  k2={k2[:8]}..  ctr={ctr}")


# Send to P0: (x0,x1), (y0,y1), phi0
s=socket.socket()
s.connect((HOST,PORT_P0))
send_json(s, {
    "x_i": x2, "x_ip1": x0,
    "y_i": y2, "y_ip1": y0,
    "k_self": k2,   # with P0
    "k_prev": k1,   # with P1
    "ctr": ctr
})
s.close()

# Send to P1: (x1,x2), (y1,y2), phi1
s=socket.socket()
s.connect((HOST,PORT_P1))
send_json(s, {
    "x_i": x0, "x_ip1": x1,
    "y_i": y0, "y_ip1": y1,
    "k_self": k0,   # with P1
    "k_prev": k2,   # with P2
    "ctr": ctr
})
s.close()

# Send to P2: (x2,x0), (y2,y0), phi2
s=socket.socket()
s.connect((HOST,PORT_P2))
send_json(s, {
    "x_i": x1, "x_ip1": x2,
    "y_i": y1, "y_ip1": y2,
    "k_self": k1,   # with P2
    "k_prev": k0,   # with P0
    "ctr": ctr
})
s.close()

print("[P3] sent replicated shares + PRG seeds to P0, P1, P2")
print("[P3] reconstruct tip: z = (z0' + z1' + z2') % Q  (collect one masked per index)")
