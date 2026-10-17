# 01 | Building the LCG generator
# ============================================================================
# PURPOSE
# An LCG (Linear Congruential Generator) builds a sequence of numbers by
# repeatedly applying the same rule to the previous number:
#
#   next state = (a + b * previous state) modulo M
#
# "Modulo M" means taking the remainder after division by M. The states are
# therefore integers from 0 to M - 1. At the end, we divide them by M + 1
# to obtain values between 0 and 1, excluding 1.
#
# The procedure is deterministic: the same parameters and initial number
# produce the same sequence. We want this sequence to imitate independent
# uniform draws; having values between 0 and 1 does not guarantee this.
# In the second file, we will make an initial check of their distribution.
#
# FUNCTION ARGUMENTS
#   u0 : seed, meaning the initial state; must be supplied in the call.
#   n  : total number of returned values, INCLUDING the rescaled seed.
#   a  : number added at each step.
#   b  : number by which the previous state is multiplied.
#   M  : modulus, which determines the possible integer states.
#
# Expressions such as n = 1000 and a = ... specify default values:
# they are used when we do not provide different values in the call.
# This version requires an integer n >= 2, a positive integer M, and an integer
# seed from 0 to M - 1. The parameters a and b are also integers.
# It does not check these requirements.
#
# HOW TO USE IT
# Running this file defines lcg; it does not generate a sequence yet.
# A call such as the following actually executes the function's instructions:
#
#   u <- lcg(u0 = 2, n = 4, a = 1, b = 5, M = 16)
#
# In R, <- assigns a result to a name. Here u will hold the four returned
# values. To follow the calculations by hand, we use these small parameters
# in the comments below; the function's defaults remain those listed above.
# ============================================================================

lcg <- function(u0, n = 1000, a = 69069069, b = 12345, M = 2^32) {
  # 1. PREPARE THE CONTAINER
  # rep(NA, n) repeats NA n times: it creates a vector with n places to fill.
  # NA represents a missing value; x_out is the name assigned to the vector.
  # With n = 4: x_out is [NA, NA, NA, NA].
  x_out <- rep(NA, n)

  # 2. INSERT THE SEED
  # R indices start at 1: x_out[1] is the first element of the vector.
  # With u0 = 2: x_out becomes [2, NA, NA, NA].
  x_out[1] <- u0

  # 3. COMPUTE THE NEXT STATES
  # 2:n is the sequence of indices from 2 to n. With n = 4, i is 2, then 3, then 4.
  # The for loop repeats the block inside the braces for each index.
  for (i in 2:n) {
    # x_out[i - 1] reads the previous state, which has already been computed.
    # We multiply it by b, add a, and take the remainder using %% M.
    # The assignment stores the result in the current position, x_out[i].
    #
    # With a = 1, b = 5, M = 16, and seed 2:
    #   i = 2: (1 + 5 * 2)  %% 16 = 11  -> [2, 11, NA, NA]
    #   i = 3: (1 + 5 * 11) %% 16 = 8   -> [2, 11,  8, NA]
    #   i = 4: (1 + 5 * 8)  %% 16 = 9   -> [2, 11,  8,  9]
    x_out[i] <- (a + (b * x_out[i - 1])) %% M
  }

  # 4. RESCALE AND RETURN THE VECTOR
  # R divides every element of x_out by M + 1; return passes the result back
  # to whoever called the function. With M = 16, we obtain:
  #   [2/17, 11/17, 8/17, 9/17], approximately [0.118, 0.647, 0.471, 0.529].
  # The first value comes from the seed; the loop computed the other n - 1.
  return(x_out / (M + 1))
}
