# 🎓 MSc Data Science Notes

*Lecture notes and worked exercises · Sapienza University of Rome*

---

## 📚 Course notes

### First year · First semester

| Course | Notes | Status |
| --- | --- | --- |
| Fundamentals of Statistical Learning | [📖 Open PDF](First%20year/First%20semester/Fundamentals%20of%20Statistical%20Learning/Fundamentals_of_Statistical_Learning_Notes.pdf) · [📋 Cheatsheet PDF](First%20year/First%20semester/Fundamentals%20of%20Statistical%20Learning/Fundamentals_of_Statistical_Learning_Cheatsheet.pdf) | 🟡 In progress |
| Fundamentals of Data Science | [📖 Open PDF](First%20year/First%20semester/Fundamentals%20of%20Data%20Science/Fundamentals_of_Data_Science_Notes.pdf) | 🟡 In progress |
| Algorithmic Methods of Data Mining | [📖 Open PDF](First%20year/First%20semester/Algorithmic%20Methods%20of%20Data%20Mining/Algorithmic_Methods_of_Data_Mining_Notes.pdf) | 🟡 In progress |

### Fundamentals of Statistical Learning · R examples

- [01_lcg.R](First%20year/First%20semester/Fundamentals%20of%20Statistical%20Learning/Code/01_lcg.R) — Define the generator, with step-by-step comments and a numerical example.
- [02_histogram.R](First%20year/First%20semester/Fundamentals%20of%20Statistical%20Learning/Code/02_histogram.R) — Generate values and compare their histogram with the uniform PDF.

<details>
<summary><strong>Fundamentals of Statistical Learning · Lecture checklist</strong></summary>

- [ ] **24 September** — Crash course exercises; completeness to verify.
- [x] **25 September** — Random variables, PMF, PDF and CDF.
- [ ] **30 September** — PMF/PDF/CDF relations and quantiles; lecture boundaries to verify.
- [ ] **1 October** — Simulation, pseudorandom generators and LCG; material included, review pending.
- [ ] **2 October** — LCG in R, histogram and consecutive-pair checks, quantile transform and population generation; blackboard material on distances, loss, risk and convergence integrated. Recent additions marked in red, pending Matteo's review.
- [x] **7 October** — Random vectors, joint/marginal/conditional distributions, independence, copulas and IID samples; likelihood and empirical CDF clarified and reviewed.
- [ ] **8 October** — Transformations of continuous random variables, the example Y = X² and its simulation in R (Topic 06, Part II, slides 4–8); explanations added, pending Matteo's review.
- [ ] **9 October** — Scheduled lecture; notes to cover.
- [ ] **14 October** — Continuous random vectors: joint PDFs, marginalization and conditioning; exponential waiting times, memorylessness and a printer example; worked normalization/CDF/quantile/transformation exercise; mixed binomial model with a latent uniform or Beta success probability, including Beta PDFs and CDFs. Revised against Flavia's notes, with plots and R examples; personal review pending. Final marginal and posterior questions retained as exercises.

</details>

<details>
<summary><strong>Algorithmic Methods of Data Mining · Topics in lecture order</strong></summary>

Compiled from Flavia's handwritten notes up to 12 October. The notes do not date the first lecture; 24 September is inferred from the [first-year timetable](https://sapienzastudents.net/datasci/courses/timetables/per-year/first-year/) (Mon 14–16, Tue 15–19, Thu 14–16) and the [2026/27 calendar](https://sapienzastudents.net/datasci/courses/calendars/2026-27/) (lectures start on 23 September), as the only ADM slot before 28 September.

**24 September**

1. Course organization: homeworks, hackathon and written exam.
2. Definition of data mining; descriptive and predictive tasks.
3. Structured, unstructured and semi-structured data; data cleaning.

**28 September**

4. Types of data: tables, transactions, documents, networks, genomic sequences, climate and behavioural data.
5. Attributes (binary, categorical, numeric) and sparsity; rows as points or vectors; document, transaction, ordered and graph data.
6. Max-Find: pseudocode, correctness by induction, counting steps (3n + 2 and 4n + 2).

**29 September**

7. Asymptotic notation (O, Ω, Θ), dominant terms and growth rates; the base of the logarithm.
8. Lower bounds and optimal algorithms: Max-Find is optimal.
9. Prefix sums: the quadratic algorithm and the linear one.
10. Matrix multiplication: the open gap between n² and n³.
11. Recursion: recursive Fibonacci, its exponential running time, and the linear iterative algorithm.

**1 October**

12. Binary search: algorithm, examples and the Θ(log n) recurrence.
13. Traveling salesman problem and brute force.
14. Decision problems, the classes P and NP, and the P = NP question.
15. NP-completeness and reductions (Max-Find and sorting).

**5 October**

16. NP-completeness recap; SAT and how to prove that a problem is NP-complete.
17. Knapsack, Set cover, Subset sum and Max clique.
18. NP-hard problems.
19. Approximation algorithms and guarantees from a lower bound.

**8 October**

20. Approximability (set cover, max clique); heuristics, greedy knapsack, fractional knapsack and meta-heuristics.
21. Distance functions; Euclidean, Lp, Manhattan, L∞ and Hamming distances.
22. Distances between sets: intersections, binary vectors, Jaccard similarity and distance.

**12 October**

23. Distances between strings: first attempts and their problems.
24. Subsequences, common subsequences and the longest common subsequence.
25. Edit distance, its relation to the LCS, and its recursive formula (start of dynamic programming).

</details>

## About

I write these notes in English to organize what I learn and work through the material in my own words. They are works in progress and may contain mistakes or omissions; use them alongside the lectures and recommended textbooks.

The LaTeX sources are available, but the custom style package `learningnotes.sty` is not included. To compile the sources, replace the package and its custom environments with your own definitions.

🐛 Found an error? [Open an issue](https://github.com/teoang/msc-data-science/issues).
