---
label: "IV"
subtitle: "Paradigms & limits"
group: "Data structures & algorithms"
order: 4
---
Level IV — Paradigms & limits
Greedy, divide & conquer, DP, reductions, hardness, approximation.

## 1. Greedy algorithms
- Build solution step-by-step; each step makes the locally best choice.
- Correctness needs proof: often exchange argument or matroid structure.
- Counterexample habit: if greedy fails, smallest input where it diverges from optimal.
- Classic: activity selection, Huffman coding, MST (Kruskal/Prim), fractional knapsack.
- 0/1 knapsack is not greedy-safe — need DP.

## 2. Divide & conquer
- Split problem into subproblems, solve recursively, combine results.
- Runtime from recurrence: mergesort, closest pair, Strassen-style ideas.
- Master theorem helps bound T(n) = aT(n/b) + f(n) for many recurrences.
- Contrast with DP: subproblems overlap → pure divide & conquer may redo work.

## 3. Dynamic programming
- Optimal substructure: optimal solution built from optimal subsolutions.
- Overlapping subproblems: same subproblem many times → memoize or tabulate.
- Top-down memoization vs bottom-up table: same complexity; trade recursion depth.
- State design is the hard part: dimensions = subproblems you index.
- Examples: Fibonacci, LCS, edit distance, subset sums, knapsack variants.

## 4. DP vs greedy — decision checklist
- Greedy if local choices cannot trap you (proved).
- DP when optimal answer depends on overlapping smaller structured instances.
- Try: write recurrence first; if exponential naive tree → memoize.

## 5. Reductions
- Reduce problem A to B: solving B lets you solve A with little overhead.
- If A reduces to B and A is hard → B is at least as hard (complexity lower bounds).
- SAT, NP-completeness chain: many problems reduce to each other.
- Practically: reuse solver libraries by encoding your problem as known form.

## 6. P, NP, NP-hardness (practical framing)
- P: decision problems solvable in polynomial time (efficient in theory land).
- NP: solutions verifiable in polynomial time (certificate checked quickly).
- NP-complete: in NP and every NP problem reduces to it — hardest in NP.
- NP-hard: at least as hard as NP-complete; need not be in NP.
- Real solvers: SAT/SMT, ILP, CP — exponential worst case; often OK on instances.

## 7. When exact is too expensive
- Approximation algorithms: proven ratio vs optimum for optimization versions.
- Heuristics / metaheuristics: no guarantee; tune for speed or quality (GA, SA, etc.).
- FPT: fixed-parameter tractable — exponential only in parameter k, poly in n.
- Pick exact DP vs heuristic based on n, time budget, and failure cost.

## 8. Remember & rehearse
- Write recurrence for LCS or edit distance and trace one small table.
- One greedy proof sketch in words (exchange).
- Name one problem in NP you cannot solve reliably in poly time (e.g. TSP decision).
