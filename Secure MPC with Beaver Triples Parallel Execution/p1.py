import socket
import json
import threading

HOST = '127.0.0.1'
PORT_P1 = 6001
PORT_P3 = 7000   # send z1 to P3

SLOTS = 2  # Number of parallel multiplications

def recv_json(conn):
    return json.loads(conn.recv(4096).decode())

def send_json(conn, obj):
    conn.sendall(json.dumps(obj).encode())

triple_shares = None
input_shares = None
results = [None] * SLOTS

def handle_slot(slot_id, srv):

    # Get d0 and e0 from p0
    conn_p0, address = srv.accept()
    vals = recv_json(conn_p0)
    d0 = vals['d']
    e0 = vals['e']

    # triple and input shares
    a1 = triple_shares[0][slot_id]
    b1 = triple_shares[1][slot_id]
    c1 = triple_shares[2][slot_id]
    x1 = input_shares[0][slot_id]
    y1 = input_shares[1][slot_id]

    # Compute d1 and e1
    d1 = x1 - a1
    e1 = y1 - b1

    # Compute d and e
    d = d0 + d1
    e = e0 + e1

    z1 = c1 + d * b1 + e * a1
    results[slot_id] = z1

    # Send back to P0
    send_json(conn_p0, {'d': d1, 'e': e1})
    conn_p0.close()

def accept_loop():
    global triple_shares, input_shares

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT_P1))
    srv.listen(5)
    print("[P1] Listening...")

    # Get triples from P2
    conn_p2, address = srv.accept()
    t = recv_json(conn_p2)
    triple_shares = (t['a1'], t['b1'], t['c1'])
    conn_p2.close()

    # Get inputs from P3
    conn_p3, address = srv.accept()
    input_data = recv_json(conn_p3)
    input_shares = (input_data['x1'], input_data['y1'])

    print("\n[P1] 1st Multiplication Shares")
    print("[P1] x1, y1 =", input_shares[0][0],input_shares[1][0])
    print("\n[P1] 2nd Multiplication Shares")
    print("[P1] x1, y1 =", input_shares[0][1],input_shares[1][1])
    conn_p3.close()

    # Start threads for each slot
    threads = []
    for slot in range(SLOTS):
        th = threading.Thread(target=handle_slot, args=(slot, srv))
        threads.append(th)
        th.start()

    for th in threads:
        th.join()

    print("\n[P1] Results (z1 shares):", results)

    # Send results to P3
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((HOST, PORT_P3))
    send_json(c, {'z1': results})
    c.close()
    srv.close()

if __name__ == "__main__":
    accept_loop()
