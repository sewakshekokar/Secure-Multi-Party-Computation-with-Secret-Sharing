# Secure Multiparty Computation with Beaver Triples (Sequential Execution)

This project demonstrates a simple **Secure Multiparty Computation (MPC)** protocol for multiplying secret-shared values using **Beaver triples**, implemented in **python**.

The system consists of **four parties**:

- **P0** → Party 0 (computing party)  
- **P1** → Party 1 (computing party)  
- **P2 (Helper)** → Provides Beaver triples  
- **P3 (Client)** → Provides inputs and splits them into shares  

---

## Overview

The goal is to securely compute the product:

1. `z1 = x * y`  
2. `z = z1 * z2`  

**Note:** Here the z2 is y_next.

without revealing `x`, `y`, or `y_next` to any single party.  

This is achieved with **additive secret sharing** and **Beaver triples**:

- Client `P3` splits each input into random shares and sends them to `P0` and `P1`.  
- Helper `P2` generates a random Beaver triple `(a, b, c)` where `c = a*b`.  
- Parties `P0` and `P1` use the shares and the Beaver triple to compute multiplication securely.  

---


## Files

- **`P0.py`** → Party 0 (computes `z0` shares)  
- **`P1.py`** → Party 1 (computes `z1` shares)  
- **`P2_Helper.py`** → Generates Beaver triples and distributes them  
- **`P3_Client.py`** → Provides inputs, generates shares, and distributes them  

---
## Requirements

- Python 3.x  
- Only standard libraries are used:  
  - `socket`  
  - `json`  
  - `random`  
  - `time`
 
---
## Running the Protocol

Open 4 terminals and run the parties in the following order:

1. **Start Party 0**  
   ```bash
   python3 p0.py
2. **Start Party 1**
   ```bash
   python3 p1.py

3. **Start Client (P3)**
   ```bash
    python3 p3_client.py
P3 splits inputs into additive shares and sends them to P0 and P1.

4. **Start Helper (P2)**
   ```bash
    python3 p2_helper.py

P2 distributes Beaver triples to P0 and P1.
   
