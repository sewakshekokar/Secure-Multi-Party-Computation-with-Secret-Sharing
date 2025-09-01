import socket
import json
import threading

HOST = '127.0.0.1'
PORT_P0 = 6000
PORT_P1 = 6001
PORT_P3 = 7000   # to send z0 to P3

SLOTS = 2  # Number of parallel multiplications

def recv_json(conn):
    return json.loads(conn.recv(4096).decode())

def send_json(conn, obj):
    conn.sendall(json.dumps(obj).encode())

triple_shares = None
input_shares = None
results = [None] * SLOTS

def handle_slot(slot_id):

    a0 = triple_shares[0][slot_id]
    b0 = triple_shares[1][slot_id]
    c0 = triple_shares[2][slot_id]
    x0 = input_shares[0][slot_id]
    y0 = input_shares[1][slot_id]

    d0 = x0 - a0
    e0 = y0 - b0

    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.connect((HOST, PORT_P1))
    send_json(s1, {'slot': slot_id, 'd': d0, 'e': e0})

    # Get d1 and e1 from p1
    vals = recv_json(s1)
    d1 = vals['d']
    e1 = vals['e']
    s1.close()

    # Compute d and e
    d = d0 + d1
    e = e0 + e1

    z0 = c0 + d * b0 + e * a0 + d * e
    results[slot_id] = z0

def accept_loop():
    global triple_shares, input_shares

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT_P0))
    srv.listen(5)
    print("[P0] Listening...")

    # Get triples from P2
    conn_p2, address = srv.accept()
    t = recv_json(conn_p2)
    triple_shares = (t['a0'], t['b0'], t['c0'])
    conn_p2.close()

    # Get inputs from P3
    conn_p3, address = srv.accept()
    input_data = recv_json(conn_p3)
    input_shares = (input_data['x0'], input_data['y0'])

    print("\n[P0] 1st Multiplication Shares")
    print("[P0] x0, y0 =", input_shares[0][0],input_shares[1][0])
    print("\n[P0] 2nd Multiplication Shares")
    print("[P0] x0, y0 =", input_shares[0][1],input_shares[1][1])
    conn_p3.close()

    threads = []
    for slot in range(SLOTS):
        th = threading.Thread(target=handle_slot, args=(slot,))
        threads.append(th)
        th.start()

    for th in threads:
        th.join()

    print("\n[P0] Results (z0 shares):", results)

    # Send results back to P3
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((HOST, PORT_P3))
    send_json(c, {'z0': results})
    c.close()
    srv.close()

if __name__ == "__main__":
    accept_loop()
