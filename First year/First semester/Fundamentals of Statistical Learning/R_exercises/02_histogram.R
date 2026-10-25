# 02 | Checking the output with a histogram
# ============================================================================
# PURPOSE
# We want to use the LCG values as a starting point for simulations.
# We therefore check whether they are distributed approximately like a uniform
# distribution on (0, 1): intervals of equal length should receive similar
# fractions of the values.
#
# A histogram divides the range into intervals (bins), counts the values in
# each interval, and represents them with bars. Here the bars describe the
# LCG OUTPUT; the dashed line represents the reference UNIFORM PDF.
#
# HOW TO RUN IT
# R's working directory must be this Code folder, because source looks for
# the first file relative to the working directory, not relative to this script.
# In RStudio: Session > Set Working Directory > To Source File Location,
# with this file open. Then run the lines in order.
# From a terminal opened in the Code folder: Rscript 02_histogram.R
# ============================================================================

# 1. LOAD THE FUNCTION
# source reads and executes the first file, making lcg available.
# The first file defines the function; numbers are generated when we call it.
source("01_lcg.R")

# 2. GENERATE THE VALUES TO EXAMINE
# n = 1000 is our choice: we request 1000 values, including the rescaled seed.
# u0 = 26 is the seed; a, b, and M determine the generator's update rule.
# In R, ^ denotes a power: 2^12 = 4096.
# <- stores the vector returned by the function in the variable u.
# To explore it in the console: length(u) shows how many values it contains,
# while head(u) shows the first six.
u <- lcg(u0 = 26, n = 1000, a = 69069069, b = 12345, M = 2^12)

# 3. BUILD THE HISTOGRAM
# hist(u, ...) uses the values we just stored in u as its data.
# breaks sets the bin boundaries. seq(0, 1, 0.1) creates the sequence
# 0, 0.1, 0.2, ..., 1: eleven boundaries define ten bins of width 0.1.
# With hist's default settings, the first bin is [0, 0.1] and the following
# bins are (0.1, 0.2], (0.2, 0.3], etc.: each value is counted exactly once.
#
# WHY probability = TRUE?
# A PDF represents an interval's probability as the AREA under its curve.
# To compare the bars with a PDF, we therefore want each AREA to equal the
# fraction of values in its bin, rather than using the count as the height.
#
#   fraction in the bin = count / total number of values
#   bar area = width * height
#   height = fraction / width
#
# In this sequence, the first bin contains 81 values out of 1000:
#   fraction = 81 / 1000 = 0.081
#   height   = 0.081 / 0.1 = 0.81
#   area     = 0.1 * 0.81 = 0.081
# The bar therefore represents 8.1% of the values. Its HEIGHT is not a
# probability; it is the estimated PDF value over that bin.
# probability = TRUE performs this calculation automatically for every bar.
# The bar areas sum to 1 because every value belongs to a bin.
# main sets the plot title; xlab sets the label of the x-axis.
hist(u, breaks = seq(0, 1, 0.1), probability = TRUE,
     main = "LCG output (n = 1000)", xlab = "Generated value")

# 4. ADD THE THEORETICAL REFERENCE
# The PDF of Unif(0, 1) has height 1 on (0, 1). Over a bin of width 0.1,
# its area is 0.1 * 1 = 0.1, meaning a probability of 10%.
# In 1000 uniform draws, we therefore expect about 100 values per bin.
# With 100 values, the bar would also have height (100 / 1000) / 0.1 = 1.
# abline adds a line to the plot we just drew: h = 1 makes it horizontal
# at height 1; lty = 2 makes it dashed.
abline(h = 1, lty = 2)

# HOW TO READ THE RESULT
# Bars roughly close to the line suggest an approximately uniform distribution.
# We do not require identical counts in the ten bins: even a random uniform
# sample can have more values in one interval and fewer in another.
# This is an initial visual check, not a guarantee of the generator's quality.
# Also, the histogram ignores the order of the values: it does not check independence.
