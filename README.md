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
- [ ] **14 October** — Continuous and mixed random vectors are collected in chapter 4; exponential waiting times, memorylessness, the printer example, and Beta distribution theory are under Common univariate distributions (§3.9). Density estimation and penalization are in chapter 6; the worked normalization/CDF/quantile/transformation exercise is in the random-variable exercise appendix. 

</details>

<details>
<summary><strong>Fundamentals of Statistical Learning · Topics in lecture order</strong></summary>

Compiled from Flavia's handwritten notes up to 16 October, in the order the topics were covered. Her notes start with random variables and date only the last lecture, so earlier topics are listed in order without dates.

**Random variables (Topic 03)**

1. Random variables as maps from the sample space: five coin flips and the dart example.
2. Discrete and continuous variables: PMF and PDF, support, and why P(X = x) = 0 for a continuous variable.
3. The CDF: definition and properties; the PDF as the derivative of the CDF.
4. Discrete example: PMF, step-function CDF, and recovering the PMF from the jumps.
5. Relations between PMF, PDF and CDF.
6. Continuous example (darts): CDF, PDF, indicator functions and interval probabilities.
7. The quantile function: invertible case, general definition, Pareto example (percentiles and median), discrete example (median, 90th percentile, third quartile), and solving F(x) = p numerically.
8. The sample space moves into the background; "famous" distributions.

**Gallery of univariate distributions (Topic 04)**

9. Modelling a psychic's 25 card guesses: Bernoulli model, IID assumptions, and the number of successes as a Binomial.
10. Bernoulli and Binomial distributions; log-odds and the link to logistic regression.
11. Poisson distribution and the Poisson approximation to the Binomial.
12. Uniform distribution; quantile transform and probability transform.
13. Single-parameter exponential families, with Binomial and Normal examples.

**Simulation, Part I (Topic 06)**

14. Why simulate: typical behaviour, variability and rare events; population model and sampling scheme; generative models.
15. Physical simulators; truly random and pseudorandom numbers.
16. First definitions of random vectors and IID random samples.
17. Pseudorandom number generators and seeds in R.
18. Distances between densities (L1, L2, L∞, KL divergence, Wasserstein, Hellinger); when a generator works: worst-case and average loss, a first definition of learning, convergence rates.
19. Checking generated samples: uniformity and independence of consecutive pairs.
20. Linear congruential generator: definition, period, distribution and independence of the samples (k-dimensional equidistribution).
21. Generating discrete random variables; the inverse-transform (quantile) method with continuous and Bernoulli examples in R; its limits (Normal and Box–Muller, dimension p > 1).

**Random vectors**

22. Describing a random vector: individual variables and their dependence; the exam and attendance contingency table.
23. Fully discrete vectors: joint, marginal and conditional PMFs.
24. Independence and distances from independence.
25. Sklar's theorem and copulas; the joint CDF and its basic properties (marginals as limits, independence through the CDF).
26. IID samples from a population model, the data-generating process, the likelihood, maximum likelihood and the empirical CDF.

**Simulation, Part II (Topic 06)**

27. Transformations of random variables: the three-step method, the monotone case, and Y = X² with X ~ Unif(−1, 1).
28. Computing a quantile function numerically.
29. Density estimation: empirical CDF, histograms in one and several dimensions, kernel density estimation; maximum likelihood over densities needs a penalty.

**Random vectors, Part II**

30. Fully continuous vectors: joint PDF, normalizing a kernel, probabilities as volumes, and moving between the joint CDF and the joint PDF.
31. Two independent exponential variables: marginals, joint PDF and independence.
32. Exponential distribution: waiting times, memorylessness and the printer example.
33. Conditional densities and marginalization for PDFs.
34. Exam-style exercise: normalizing a kernel, CDF, quantile, conditioning on an event, and the transformation Y = √X.
35. Mixed random vector: a Binomial count with a Uniform or Beta success probability; the Beta distribution, the Beta-Binomial marginal, the posterior and conjugacy (a first Bayesian analysis).
36. Stopping time of a stream of uniforms: T given X is Geometric, the marginal of T, and the geometric distribution with its memorylessness.

**16 October**

37. The mixing "trick": latent variables and the marginals of joint models (Beta-Binomial, Geometric with a Uniform parameter).
38. Normal distribution: standardization, probabilities, quantiles and light tails.
39. Heavier tails: Student's t and Laplace distributions; the Gamma distribution and its special cases (Exponential, Erlang, χ²).
40. Scale mixtures of Gaussians: the Student's t with a Gamma latent variable and the Laplace with an exponential one.
41. Finite mixtures: Bernoulli mixtures through the law of total probability and mixtures of Gaussians.

</details>

<details>
<summary><strong>Algorithmic Methods of Data Mining · Topics in lecture order</strong></summary>

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

All local course notes use the same style package at `shared/latex/learningnotes.sty`,
with its logo in `shared/latex/assets/sapienza.png`. Each course loads it through
`\usepackage[english]{../../../shared/latex/learningnotes}`. Edit the shared package
once, then recompile each course PDF to apply the change. Local `learningnotes.sty`
entries are relative symbolic links to that same package, kept for compatibility
with earlier source snapshots.

The LaTeX sources are available, but the custom style package remains excluded from
the public repository. To compile a downloaded copy, supply the shared package and
its logo at these paths, or replace the package and its custom environments with
your own definitions.

🐛 Found an error? [Open an issue](https://github.com/teoang/msc-data-science/issues).
