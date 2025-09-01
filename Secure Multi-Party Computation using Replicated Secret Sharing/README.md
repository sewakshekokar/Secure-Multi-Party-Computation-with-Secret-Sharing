# MPC using Replicated Secret Sharing

This project implements a **3-party secure multi-party computation (MPC)** protocol
using **Replicated Secret Sharing (RSS)** with **PRG-based zero sharing**.

## 🔹 Overview

- **Goal:** Compute the product of two secret inputs `x` and `y` without revealing them
  to any individual party.
- **Parties:**  
  - `P0`, `P1`, `P2`: Hold replicated shares of `x` and `y`, perform local computation.  
  - `P3_client`: Dealer that distributes replicated shares and PRG seeds.

- **Security:** Each party masks its partial result `zᵢ` with a random share `φᵢ` such that  
  \[
  φ₀ + φ₁ + φ₂ = 0
  \]  
  The masks are generated using PRGs from shared seeds, so no party (or dealer) knows all φ’s.

- **Correctness:** When masked values are reconstructed:  
  \[
  z₀' + z₁' + z₂' = (z₀ + z₁ + z₂) + (φ₀+φ₁+φ₂) = x \cdot y
  \]

## 🔹 Protocol Flow

1. **Client (P3):**
   - Chooses random inputs `x`, `y`.
   - Splits them into replicated shares:  
     - `x0+x1+x2 = x`,  
     - `y0+y1+y2 = y`.  
   - Generates PRG seeds (`k0`, `k1`, `k2`) shared on a ring:
     - `k0`: shared between P0 & P1  
     - `k1`: shared between P1 & P2  
     - `k2`: shared between P2 & P0  
   - Sends each party its shares + two seeds + counter.

2. **Parties (P0, P1, P2):**
   - Receive `(xᵢ, xᵢ₊₁), (yᵢ, yᵢ₊₁), (k_self, k_prev), ctr`.
   - Compute local multiplication share `zᵢ`.
   - Generate zero share:
     ```
     φᵢ = PRG(k_self, ctr) − PRG(k_prev, ctr) mod Q
     ```
   - Mask value: `zᵢ′ = zᵢ + φᵢ mod Q`.
   - Send `zᵢ′` to left neighbor, receive from right neighbor.
   - Each party now holds a **replicated product share**.

3. **Reconstruction:**  
   Collect one masked share from each party and sum mod Q → yields `x*y`.

## 🔹 Running the Code

1. Open **3 terminals** for the parties and run:
   ```bash
   python p0.py
   python p1.py
   python p2.py
   ```

2. In a **4th terminal**, run the client:
   ```bash
   python p3_client.py
   ```

3. Each party will display:
   - Its input shares
   - Local product share `zᵢ`
   - Zero share `φᵢ`
   - Masked share `zᵢ′`
   - Final replicated product pair

4. The sum of all masked shares equals `x*y mod Q`.

## 🔹 File Structure
- `p0.py` – Party 0  
- `p1.py` – Party 1  
- `p2.py` – Party 2  
- `p3_client.py` – Client that distributes shares and seeds

## 🔹 Example Output

```
[P3] x=548092, y=503239, x*y=275821269988
[P0] z0=629259307, phi0=383239297, z0'=12498597
[P1] z1=261658661, phi1=406752255, z1'=668410916
[P2] z2=930350102, phi2=210008455, z2'=140358550

Reconstructed: z0'+z1'+z2' = 821268063 mod Q
Expected: (x*y) mod Q = 821268063
```

