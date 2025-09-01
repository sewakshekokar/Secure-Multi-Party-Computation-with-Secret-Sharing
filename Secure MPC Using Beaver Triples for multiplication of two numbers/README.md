# Secure Multi-Party Computation (MPC) with Secret Sharing

This project demonstrates a simple **secure multi-party computation (MPC)** protocol using **additive secret sharing** and **Beaver triples**.  
It involves four parties (`P0`, `P1`, `P2`, and `P3`) that work together to compute the product of two secret values `x` and `y` **without revealing them**.

---

## Project Structure

- **`p0.py`** – Party P0: Receives shares from P3 and interacts with P1 and P2.  
- **`p1.py`** – Party P1: Receives shares from P3 and interacts with P0 and P2.  
- **`p2_helper.py`** – Party P2: Generates **Beaver triples** `(a, b, c)` with secret shares to enable secure multiplication.  
- **`p3_client.py`** – Party P3 (Client): Holds the secret inputs `(x, y)`, splits them into additive shares, and distributes them to P0 and P1.  

---

## Protocol Overview

1. **Secret Sharing**
   - P3 picks random integers `x` and `y`.
   - It generates additive shares:
     ```python
     x = x0 + x1
     y = y0 + y1
     ```
   - P3 sends `(x0, y0)` to P0 and `(x1, y1)` to P1.

2. **Beaver Triples (by P2)**
   - P2 generates a Beaver triple `(a, b, c)` where `c = a * b`.
   - P2 splits `(a, b, c)` into random shares `(a0, b0, c0)` and `(a1, b1, c1)` for P0 and P1.

3. **Secure Multiplication**
   - P0 and P1 compute masked differences:
     ```python
     e = (x_share - a_share)
     f = (y_share - b_share)
     ```
   - They exchange results and compute product shares securely.

4. **Reconstruction**
   - P0 and P1 can reconstruct the result of `x * y` without learning each other’s inputs.

---

## How to Run

Open **four terminal windows** (for P0, P1, P2, and P3).

1. Start the servers in this order:

   ```bash
   python3 p0.py
   python3 p1.py
   python3 p2_helper.py
   python3 p3_client.py


Example Output
[P3] x=234567, y=876543
[P3] Sending shares: P0 -> (x0=..., y0=...), P1 -> (x1=..., y1=...)
[P2] Beaver triple: a=123, b=456, c=56088
...
[Result] Securely computed x*y = 205231271881


## Workflow Diagram

```mermaid
flowchart TD
    P3["P3 (Client)\nGenerates x, y\nSplits into shares"] 
    P0["P0\nReceives (x0, y0)"] 
    P1["P1\nReceives (x1, y1)"] 
    P2["P2 (Helper)\nGenerates Beaver triples"]

    %% Connections
    P3 -->|"x0, y0"| P0
    P3 -->|"x1, y1"| P1

    P2 -->|"a0, b0, c0"| P0
    P2 -->|"a1, b1, c1"| P1

    P0 <-->|"exchange masked values"| P1

    P0 -->|"share of result"| P0
    P1 -->|"share of result"| P1

    %% Final step
    P0 & P1 -->|"Reconstruct x * y"| Result["Final Secure Product"]
