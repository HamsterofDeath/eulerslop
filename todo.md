# Project Euler — Unsolved Problems

Published range: 1-1007
Total solved: 1006 / 1007
Missing: 1 problem

Known answers are in known_answers.md; these still need solution files.

---

- 1006 — Fibonacci Subwords (Ψ(10^18) mod 101001001)

  Notes: brute-force factor enumeration verified for k <= ~60 and the
  intercept-sweep identity Ψ(k) = sum of v_r² along the sorted {j/φ}
  breakpoint sweep is validated exactly for k <= 120.  A polylog
  aggregation of the sweep for k = 10^18 is still missing.
