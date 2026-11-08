# 🎓 MSc Data Science Notes

*Lecture notes and worked exercises · Sapienza University of Rome*

---

## 📚 Course notes

### First year · First semester

| Course | Notes | Status |
| --- | --- | --- |
| Fundamentals of Statistical Learning | [📖 Open PDF](First%20year/First%20semester/Fundamentals%20of%20Statistical%20Learning/Fundamentals_of_Statistical_Learning_Notes.pdf)<br>[📋 Cheatsheet PDF](First%20year/First%20semester/Fundamentals%20of%20Statistical%20Learning/Fundamentals_of_Statistical_Learning_Cheatsheet.pdf) | 🔴 Major rewrite in progress, arguments may be missing. |
| Fundamentals of Data Science | [📖 Open PDF](First%20year/First%20semester/Fundamentals%20of%20Data%20Science/Fundamentals_of_Data_Science_Notes.pdf) | 🟡 In progress |
| Algorithmic Methods of Data Mining | [📖 Open PDF](First%20year/First%20semester/Algorithmic%20Methods%20of%20Data%20Mining/Algorithmic_Methods_of_Data_Mining_Notes.pdf) | 🟢 On par with the lessons |

<details>
<summary><strong>📊 Fundamentals of Statistical Learning · Topics in lecture order</strong></summary>

**23 September**

- [ ] Course presentation.
- [ ] Recap of basic probability: sample spaces and events, probability and its basic properties, inclusion–exclusion and probability bounds.
- [ ] Conditional probability, independence and Bayes' theorem.

**24 September**

- [ ] Introduction to R.
- [ ] Crash course exercises.

**25 September**

- [ ] Random variables as maps from the sample space: five coin flips and the dart example.
- [ ] Discrete and continuous variables: PMF and PDF, support, and why P(X = x) = 0 for a continuous variable.
- [ ] The CDF: definition and properties; the PDF as the derivative of the CDF.
- [ ] Discrete example: PMF, step-function CDF, and recovering the PMF from the jumps.
- [ ] Relations between PMF, PDF and CDF.
- [ ] Continuous example (darts): CDF, PDF, indicator functions and interval probabilities.

**30 September**

- [ ] The quantile function: invertible case, general definition, Pareto example (percentiles and median), discrete example (median, 90th percentile, third quartile), and solving F(x) = p numerically.
- [ ] The sample space moves into the background; "famous" distributions.
- [ ] Modelling a psychic's 25 card guesses: Bernoulli model, IID assumptions, and the number of successes as a Binomial.
- [ ] Bernoulli and Binomial distributions.
- [ ] Log-odds and the link to logistic regression.
- [ ] Poisson distribution and the Poisson approximation to the Binomial.
- [ ] Uniform distribution.

**1 October**

- [ ] The quantile transform.
- [ ] The probability transform.
- [ ] Single-parameter exponential families, with Binomial and Normal examples.
- [ ] Why simulate: typical behaviour, variability and rare events.
- [ ] Population model and sampling scheme; simulation as a generative model.
- [ ] Physical simulators; truly random and pseudorandom numbers.
- [ ] First definitions of random vectors and IID random samples.
- [ ] Pseudorandom number generators.

**2 October**

- [ ] Seeds in R.
- [ ] Distances between densities: L1, L2 and L∞.
- [ ] KL divergence, Wasserstein and Hellinger distances.
- [ ] When a generator works: worst-case and average loss, a first definition of learning, convergence rates.
- [ ] Checking generated samples: uniformity and independence of consecutive pairs.
- [ ] Linear congruential generator: definition, period, distribution and independence of the samples.
- [ ] k-dimensional equidistribution of the LCG.
- [ ] Generating discrete random variables; the inverse-transform (quantile) method with continuous and Bernoulli examples in R.
- [ ] Limits of the inverse-transform method: the Normal and Box–Muller, dimension p > 1.

**7 October**

- [ ] Describing a random vector: individual variables and their dependence; the exam and attendance contingency table.
- [ ] Fully discrete vectors: joint, marginal and conditional PMFs.
- [ ] Independence and distances from independence.
- [ ] Sklar's theorem and copulas; the joint CDF and its basic properties (marginals as limits, independence through the CDF).
- [ ] IID samples from a population model, the data-generating process, the likelihood, maximum likelihood and the empirical CDF.

**8 October**

- [ ] Transformations of random variables: the three-step method, the monotone case, and Y = X² with X ~ Unif(−1, 1).
- [ ] Checking the transformation by simulation in R.

**9 October**

- [ ] Computing a quantile function numerically in R with `uniroot`.
- [ ] Density estimation: the empirical CDF in R, histograms in one and several dimensions, kernel density estimation.

**14 October**

- [ ] Refresher on IID samples and the data-generating process: maximum likelihood over CDFs gives the empirical CDF, while maximum likelihood over densities needs a penalty.
- [ ] Fully continuous vectors: joint PDF, normalizing a kernel, probabilities as volumes, and moving between the joint CDF and the joint PDF.
- [ ] Two independent exponential variables: marginals, joint PDF and independence.
- [ ] Exponential distribution: waiting times, memorylessness and the printer example.
- [ ] Conditional densities and marginalization for PDFs.
- [ ] Exam-style exercise: normalizing a kernel, CDF, quantile, conditioning on an event, and the transformation Y = √X.
- [ ] Mixed random vector: a Binomial count with a Uniform or Beta success probability; the Beta distribution.

**15 October**

- [ ] Mixed random vector: joint model, Beta-Binomial marginal, posterior and conjugacy (a first Bayesian analysis).
- [ ] Stopping time of a stream of uniforms: T given X is Geometric, the marginal of T, and the geometric distribution with its memorylessness.

**16 October**

- [ ] The mixing "trick": latent variables and the marginals of joint models (Beta-Binomial, Geometric with a Uniform parameter).
- [x] Normal distribution: standardization, probabilities, quantiles and light tails.
- [ ] Heavier tails: Student's t and Laplace distributions.
- [ ] The Gamma distribution, with the exponential as a special case.
- [ ] Erlang and χ² as further special cases of the Gamma.
- [ ] Scale mixtures of Gaussians: the Student's t with a Gamma latent variable and the Laplace with an exponential one.
- [ ] Finite mixtures: Bernoulli mixtures through the law of total probability and mixtures of Gaussians.

**21 October**

- [ ] Recap of the mixing trick: the Student's t as a scale mixture of Gaussians.
- [ ] Heart-rate data in R: summaries, histogram, empirical CDF and tail probabilities; what a good population model should capture.
- [x] A Gaussian mixture model for the heart-rate data: the likelihood of the sample and maximum likelihood; why known component labels would make fitting easy.
- [ ] Parametric and nonparametric maximum likelihood; when maximum likelihood alone fails (choosing K, learning a PDF) and penalties, constraints or priors help; why finite mixtures are tricky (choice of K, ambiguous soft clustering, unbounded likelihood).
- [ ] Many-to-one transformations of an IID sample: the sum and the empirical average; sampling distributions.
- [ ] Transformations of continuous random vectors: the three-step method for Z = r(X, Y), the Jacobian matrix and the change-of-variables formula.
- [ ] The Student's t as Z / √(W/ν): adding an auxiliary variable and marginalizing it out.
- [ ] The Box–Muller transform: polar coordinates, the quantile transform for the radius, and sampling Normals in R.

**22 October**

- [ ] Classwork 00: checking our LCG formally in R; the power-law and lognormal models for bursty email activity.

**23 October**

- [ ] Why graphical models: the chain rule, conditional probability tables with O(J^D) parameters, conditional independence and the first-order Markov assumption.
- [ ] Graphical models and DAGs: graph terminology, Bayesian networks and topological ordering.
- [ ] The Markov condition and the graph-induced factorization; the set M(G) of distributions that are Markov to G.
- [ ] Examples: Markov chains of first and second order, hidden Markov models and latent variables, linear dynamical systems.
- [ ] Examples: medical diagnosis (the alarm network), Quick Medical Reference and latent Dirichlet allocation.
- [ ] Latent variables for dimensionality reduction: probabilistic PCA.

**28 October**

- [ ] Probabilistic PCA: population model, sampling scheme and fitting by maximum likelihood; mixtures for nonlinear structure.
- [ ] Bayesian modelling as a DAG: IID data are conditionally independent given θ; plate notation.
- [ ] d-separation: chain, common cause and collider (explaining away, Berkson's paradox); the "am I out of fuel?" example.
- [ ] The Bayes-ball algorithm, the general statement of d-separation and the Markov blanket; a worked example.
- [ ] Ancestral (forward) sampling.
- [ ] Exam exercise: the factorization encoded by a DAG, forward sampling in R and the marginal of one node.
- [ ] Forward sampling for mixing-trick models in R: Beta-Binomial and Student's t.

**29 October**

- [ ] Did we simulate well? Comparing a simulated Student's t (ν = 1.5) with its theoretical density, CDF and quantiles; the Q-Q plot.
- [ ] The random sample and the observed data; the CDF of the maximum of an IID sample, with the example of five bus waiting times.
- [ ] From a tail probability to a "surprise": the p-value and what "small" means.
- [ ] The lab example: why a maximum of about 7797 is not necessarily surprising, and the calculation in R.

**30 October**

- [ ] Causal inference: association and causation, confounders, and conditioning by intervention.
- [x] The expected value of a random variable and the law of the lazy statistician.

**4 November**

- [x] Jensen's inequality and the ELBO: a lower bound for the log-likelihood of a model with hidden variables.
- [x] The information gap and the KL divergence; the EM algorithm as coordinate ascent, with its remarks and the M-step as expected complete log-likelihood.

**5 November**

- [x] EM for a Gaussian mixture: the E-step with Bayes' theorem and the responsibilities.
- [x] The M-step: the expected complete log-likelihood of a GMM, centres and spreads as weighted averages, and the weights.
- [ ] Constrained optimisation and Lagrange multipliers for the weights.

**6 November**

- [x] Prediction under perfect information: loss and risk functions; the square loss gives the expected value (MSE), the abs loss the median (MAE).
- [x] Variance, standard deviation and the median absolute deviation; shift and scale; existence and degeneracy of the variance.
- [x] The variance from the moments, higher moments and the existence of lower moments.
- [x] Expected value of a random vector: linear combinations and products of independent variables.
- [x] The covariance matrix and the variance of a linear combination; independent variables have zero covariance.
- [x] Conditioning: conditional expectation and variance, the law of total expectation and the law of total probability.

</details>

<details>
<summary><strong>⛏️ Algorithmic Methods of Data Mining · Topics in lecture order</strong></summary>

**24 September**

- [x] Course organization: homeworks, hackathon and written exam.
- [x] Definition of data mining; descriptive and predictive tasks.
- [x] Structured, unstructured and semi-structured data; data cleaning.

**28 September**

- [x] Types of data: tables, transactions, documents, networks, genomic sequences, climate and behavioural data.
- [x] Attributes (binary, categorical, numeric) and sparsity; rows as points or vectors; document, transaction, ordered and graph data.
- [x] Max-Find: pseudocode, correctness by induction, counting steps (3n + 2 and 4n + 2).

**29 September**

- [x] Asymptotic notation (O, Ω, Θ), dominant terms and growth rates; the base of the logarithm.
- [x] Lower bounds and optimal algorithms: Max-Find is optimal.
- [x] Prefix sums: the quadratic algorithm and the linear one.
- [x] Matrix multiplication: the open gap between n² and n³.
- [x] Recursion: recursive Fibonacci, its exponential running time, and the linear iterative algorithm.

**1 October**

- [x] Binary search: algorithm, examples and the Θ(log n) recurrence.
- [x] Traveling salesman problem and brute force.
- [x] Decision problems, the classes P and NP, and the P = NP question.
- [x] NP-completeness and reductions (Max-Find and sorting).

**5 October**

- [x] NP-completeness recap; SAT and how to prove that a problem is NP-complete.
- [x] Knapsack, Set cover, Subset sum and Max clique.
- [x] NP-hard problems.
- [x] Approximation algorithms and guarantees from a lower bound.

**8 October**

- [x] Approximability (set cover, max clique); heuristics, greedy knapsack, fractional knapsack and meta-heuristics.
- [x] Distance functions; Euclidean, Lp, Manhattan, L∞ and Hamming distances.
- [x] Distances between sets: intersections, binary vectors, Jaccard similarity and distance.

**12 October**

- [x] Distances between strings: first attempts and their problems.
- [x] Subsequences, common subsequences and the longest common subsequence.
- [x] Edit distance, its relation to the LCS, and its recursive formula (start of dynamic programming).

**19 October**

- [ ] Memory: bytes, addresses and consecutive memory locations.
- [ ] Python names refer to objects.

**20 October**

- [x] Text mining: corpus, vocabulary and document count vectors; document length and L1/L2 normalization.
- [x] Cosine similarity: geometric interpretation and step-by-step computation from coordinates.
- [x] Stopwords, document frequency, IDF and TF-IDF weights, with worked examples.
- [x] Query vectors, cosine scores and top-k retrieval; direct-search cost O(Nm + N log N).
- [x] Offline corpus preparation and online query processing.
- [x] Boolean AND search; inverted indexes and sorted posting lists.
- [x] Posting-list intersections with pointers, algorithm and query-cost analysis.

**22 October**

- [x] Terms stored as integer identifiers.
- [x] Boolean queries with OR and AND NOT: the same pointer merge with different rules, a worked query, and the cost O(|L| + |M|).
- [x] Faster ranked search: approximate answers by searching inside one cluster.
- [x] Ranked retrieval with an inverted index: (document, TF) postings, scoring only documents that share a query term, precomputed document norms, and the top-K algorithm with a worked example.

**26 October**

- [x] The sorting problem; Merge: combining two sorted arrays in linear time.
- [x] MergeSort: split, sort the halves and merge, with a worked 13-element example.
- [x] MergeSort running time: expanding the recurrence 2T(n/2) + cn to Θ(n log n).
- [x] Randomized algorithms; expected value with one and two dice.
- [x] Randomized QuickSort: pivot, partition and a worked execution.
- [x] QuickSort cost: balanced partitions, the Θ(n²) worst case with extreme pivots, and the expected O(n log n) bound (stated without proof).

**29 October**

- [x] Back to top-k selection: sorting everything, or keeping k candidates in an array.
- [x] Abstract data types and data structures: an interface and its implementations.
- [x] The list ADT: arrays, singly and doubly linked lists, and their operation costs.
- [x] The priority queue ADT.
- [x] Binary heaps: the array representation, insertion with sift-up and extraction with sift-down; comparing priority queue implementations.
- [x] HeapSort, first into a second array and then in place.
- [x] Selecting the top k with a min-heap in O(n log k) time.

**2 November**

- [x] The dictionary of terms in the inverted index; the dictionary (map) ADT.
- [x] Keys as array positions, and turning names into numbers: collisions and wasted space.
- [x] Hash functions, collisions, and why collisions cannot be avoided.
- [x] How rare collisions should be, and why the hash function must be deterministic.
- [x] Universal hash families: a family for IP addresses and the proof of its 1/p collision probability.
- [x] Hash tables with chaining.

**5 November**

- [x] Clustering: grouping similar points with the L2 distance; hierarchical and partitional (k-) clustering.
- [x] Bottom-up hierarchical clustering: merging the closest clusters, the distance between cluster means, and the dendrogram of a ten-point example.
- [x] Cost of hierarchical clustering: O(n³) by rescanning, O(n² log n) with one heap per cluster.
- [x] k-partitions and the k-means problem: representatives and the cost of the partitioning.
- [x] Hardness of k-means: k^n partitions, the easy cases k = n and k = 1 (the mean is the best representative), and points on a line.
- [x] Why cutting at the largest gaps fails on a line; NP-completeness and the need for approximation algorithms.

</details>

## About

These are my English notes for the MSc in Data Science at Sapienza. They are a work in progress and may contain mistakes, so use them alongside the lectures and textbooks. 🐛 Found an error? [Open an issue](https://github.com/teoang/msc-data-science/issues).

The LaTeX sources are included, but the shared style package is not: to compile them, supply your own.

## License

Released under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/): you may share and adapt the notes with credit, for non-commercial use, under the same license. The Sapienza logo and figures from other sources belong to their owners. Full text in [LICENSE](LICENSE).
