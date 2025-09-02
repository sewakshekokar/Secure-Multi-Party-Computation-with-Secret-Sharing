# Secure Multiplication with Beaver Triples (Parallel Execution)

This project implements **Secure Multi-Party Computation (MPC)** for multiplication using **Beaver triples**.  
It demonstrates **parallel secure multiplications** across multiple parties using Python sockets and threading.

---

## Parties

- **P0**: Holds secret shares of inputs and Beaver triples. Computes partial multiplication shares `z0`.
- **P1**: Holds secret shares of inputs and Beaver triples. Computes partial multiplication shares `z1`.
- **P2 (Helper)**: Generates **Beaver triples** `(a, b, c = a*b)` and distributes random additive shares to `P0` and `P1`.
- **P3 (Client)**: Provides the original inputs `(x, y)` by splitting them into random shares and sending to `P0` and `P1`.  
  After computation, collects results `z0` and `z1` to reconstruct the final product.

---

## How It Works

1. **Beaver Triple Generation**  
   `P2` generates random Beaver triples `(a, b, c)` for each multiplication.  
   These are secret-shared between `P0` and `P1`.

2. **Input Sharing**  
   `P3` generates random additive shares of inputs `(x, y)` and sends them to `P0` and `P1`.

3. **Secure Multiplication**  
   - `P0` and `P1` exchange masked values `d = x - a`, `e = y - b`.  
   - Each computes its share of the product (`z0`, `z1`).  
   - This is done in **parallel** for multiple slots using threads.

4. **Reconstruction**  
   `P3` receives `z0` from `P0` and `z1` from `P1`, and reconstructs the product `z = z0 + z1`.  
   It also measures the **latency**.

---

## Running the Protocol

Open **4 terminals** and run the parties in the following order:

```bash


# Terminal 1 (P0)
python p0.py

# Terminal 2 (P1)
python p1.py

# Terminal 3 (Helper)
python p2_helper.py

# Terminal 4 (Client)
python p3_client.py
