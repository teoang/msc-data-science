# Illustrative figures for the FSL remedy notes on the expected value.
# Run from the project directory: Rscript figure.R
dir.create("images", showWarnings = FALSE)
blue <- "#246387"
orange <- "#B2562C"
ink <- "#343B42"
grid_col <- "#E0E3E5"

# A weightless rod with weights p(x_j): it balances at E(X).
draw_rod <- function(x, p, xlim, main) {
  m <- sum(x * p)
  plot(NA, xlim = xlim, ylim = c(-.12, max(p) * 1.18), axes = FALSE,
       xlab = "", ylab = "", main = main, cex.main = 1)
  segments(xlim[1], 0, xlim[2], 0, col = ink, lwd = 2.2)
  segments(x, 0, x, p, col = blue, lwd = 5, lend = 1)
  text(x, p, labels = format(p), pos = 3, cex = .8, col = blue)
  axis(1, at = x, pos = -.12, col = NA, col.ticks = NA, cex.axis = .8, line = -1)
  polygon(m + c(-.18, .18, 0) * diff(xlim) / 10, c(-.11, -.11, 0),
          col = orange, border = orange)
  text(m, -.11, bquote(E(X) == .(m)), pos = 4, cex = .8, col = orange, offset = .9)
}

pdf("assets/rod-discrete.pdf", width = 8, height = 2.1,
    family = "Helvetica", useDingbats = FALSE)
par(mfrow = c(1, 2), mar = c(1.6, .8, 1.6, .8), cex = .85)
draw_rod(1:5, c(.10, .15, .25, .30, .20), c(.5, 5.5), "Five weights")
draw_rod(c(0, 10), c(.9, .1), c(-.5, 10.5), "The lottery")
dev.off()

# A continuous rod: the density is the mass per unit length.
# Gamma(2, 1): peak (mode) at 1, centre of mass (mean) at 2.
pdf("assets/rod-continuous.pdf", width = 4.6, height = 2.2,
    family = "Helvetica", useDingbats = FALSE)
par(mar = c(2.6, 3.4, .6, .6), mgp = c(1.6, .45, 0), las = 1, cex = .8)
xx <- seq(0, 9, length.out = 601)
yy <- dgamma(xx, shape = 2, rate = 1)
plot(xx, yy, type = "n", xlab = "x", ylab = "", ylim = c(-.05, .42), yaxs = "i")
grid(col = grid_col)
mtext("Density", side = 2, line = 2.3, las = 0, cex = .8)
polygon(c(xx, rev(xx)), c(yy, rep(0, length(xx))),
        col = adjustcolor(blue, .18), border = NA)
lines(xx, yy, col = blue, lwd = 1.8)
segments(1, 0, 1, dgamma(1, 2, 1), col = ink, lty = 3)
text(1, dgamma(1, 2, 1), "peak", pos = 3, cex = .85, col = ink)
polygon(2 + c(-.18, .18, 0), c(-.045, -.045, 0), col = orange, border = orange)
text(2, -.03, "E(X) = 2", pos = 4, cex = .85, col = orange)
dev.off()

# Cauchy against the standard Normal: same bell shape, very different tails.
pdf("assets/cauchy-normal.pdf", width = 8, height = 2.1,
    family = "Helvetica", useDingbats = FALSE)
par(mfrow = c(1, 2), mar = c(2.6, 4.6, 1.6, .6),
    mgp = c(1.65, .45, 0), las = 1, cex = .78)
xx <- seq(-5, 5, length.out = 601)
plot(xx, dnorm(xx), type = "n", xlab = "x", ylab = "", ylim = c(0, .42),
     yaxs = "i", main = "Densities", cex.main = 1)
grid(col = grid_col)
mtext("Density", side = 2, line = 3.2, las = 0, cex = .75)
lines(xx, dcauchy(xx), col = orange, lwd = 1.8)
lines(xx, dnorm(xx), col = blue, lwd = 1.8, lty = 2)
legend("topright", bty = "n", cex = .85, legend = c("Cauchy", "Normal"),
       col = c(orange, blue), lwd = 1.8, lty = c(1, 2))
xx <- seq(0, 10, length.out = 401)
plot(xx, dcauchy(xx), type = "n", log = "y", ylim = c(1e-23, 1),
     xlab = "x", ylab = "", main = "Tails (log scale)", cex.main = 1, yaxt = "n")
axis(2, at = 10^c(-20, -10, 0), labels = expression(10^-20, 10^-10, 1))
grid(col = grid_col)
mtext("Density", side = 2, line = 3.2, las = 0, cex = .75)
lines(xx, dcauchy(xx), col = orange, lwd = 1.8)
lines(xx, dnorm(xx), col = blue, lwd = 1.8, lty = 2)
dev.off()

# Lack of robustness: move 0.05 of probability from x = 1 to x = 50.
draw_far <- function(x, p, file, main) {
  m <- sum(x * p)
  pdf(file, width = 3.9, height = 2, family = "Helvetica", useDingbats = FALSE)
  par(mar = c(1.6, .8, 1.6, .8), cex = .85)
  xlim <- c(-1, 53)
  plot(NA, xlim = xlim, ylim = c(-.12, .36), axes = FALSE,
       xlab = "", ylab = "", main = main, cex.main = 1)
  segments(xlim[1], 0, xlim[2], 0, col = ink, lwd = 2.2)
  segments(x, 0, x, p, col = blue, lwd = 3, lend = 1)
  axis(1, at = c(1, 5, 50), pos = -.12, col = NA, col.ticks = NA,
       cex.axis = .8, line = -1)
  polygon(m + c(-.9, .9, 0), c(-.11, -.11, 0), col = orange, border = orange)
  text(m, -.08, bquote(E(X) == .(sprintf("%.2f", m))), pos = 4,
       cex = .8, col = orange, offset = .9)
  dev.off()
}
draw_far(1:5, c(.10, .15, .25, .30, .20), "assets/far-before.pdf", "Before")
draw_far(c(1:5, 50), c(.05, .15, .25, .30, .20, .05), "assets/far-after.pdf",
         "After moving 0.05 to x = 50")

# The lottery rod resting on a support at c: level if balanced, tilted if not.
draw_tilt <- function(c, angle, file, main) {
  pdf(file, width = 3.9, height = 1.55, family = "Helvetica", useDingbats = FALSE)
  par(mar = c(0, .8, 1.6, .8), cex = .85)
  x <- c(0, 10); p <- c(.9, .1)
  plot(NA, xlim = c(-1, 11), ylim = c(-1.6, 3.2), axes = FALSE, asp = 1,
       xlab = "", ylab = "", main = main, cex.main = 1)
  rot <- function(px, py) cbind(c + (px - c) * cos(angle) + py * sin(angle),
                                -(px - c) * sin(angle) + py * cos(angle))
  ends <- rot(c(-.5, 10.5), c(0, 0))
  lines(ends, col = ink, lwd = 2.2)
  base <- rot(x, c(0, 0))
  top <- base + cbind(0, p * 3)
  segments(base[, 1], base[, 2], top[, 1], top[, 2], col = blue, lwd = 5, lend = 1)
  text(top[, 1], top[, 2], format(p), pos = 3, cex = .8, col = blue)
  polygon(c + c(-.35, .35, 0), c(-.6, -.6, 0), col = orange, border = orange)
  text(c, -.6, paste("c =", c), pos = 1, cex = .8, col = orange)
  dev.off()
}
draw_tilt(1, 0, "assets/rod-balanced.pdf", "Support at c = 1")
draw_tilt(.5, .12, "assets/rod-tilted.pdf", "Support at c = 0.5")

# The tangent on (-pi/2, pi/2) and its inverse, the arctangent:
# vertical asymptotes at +-pi/2 become horizontal ones.
pdf("assets/tan-arctan.pdf", width = 8, height = 2.4,
    family = "Helvetica", useDingbats = FALSE)
par(mfrow = c(1, 2), mar = c(2.6, 3.4, 1.6, .8),
    mgp = c(1.6, .45, 0), las = 1, cex = .78)
h <- pi / 2
xx <- seq(-h + .03, h - .03, length.out = 501)
plot(xx, tan(xx), type = "n", xlim = c(-1.9, 1.9), ylim = c(-8, 8),
     xlab = "x", ylab = "", xaxt = "n", main = "tan(x)",
     cex.main = 1)
axis(1, at = c(-h, 0, h), labels = expression(-pi/2, 0, pi/2))
grid(col = grid_col)
abline(v = c(-h, h), col = orange, lty = 2, lwd = 1.4)
lines(xx, tan(xx), col = blue, lwd = 1.8)
xx <- seq(-8, 8, length.out = 501)
plot(xx, atan(xx), type = "n", ylim = c(-1.9, 1.9), xlab = "x", ylab = "",
     yaxt = "n", main = "arctan(x)", cex.main = 1)
axis(2, at = c(-h, 0, h), labels = expression(-pi/2, 0, pi/2))
grid(col = grid_col)
abline(h = c(-h, h), col = orange, lty = 2, lwd = 1.4)
lines(xx, atan(xx), col = blue, lwd = 1.8)
dev.off()

# Integrand of the expected value, x f(x): Cauchy against the standard Normal.
pdf("assets/cauchy-integrand.pdf", width = 4.6, height = 2.4,
    family = "Helvetica", useDingbats = FALSE)
par(mar = c(2.6, 3.6, .6, .6), mgp = c(1.6, .45, 0), las = 1, cex = .8)
xx <- seq(-10, 10, length.out = 801)
plot(xx, xx * dnorm(xx), type = "n", ylim = c(-.26, .26),
     xlab = "x", ylab = "")
grid(col = grid_col)
abline(h = 0, col = ink, lwd = .8)
mtext("x f(x)", side = 2, line = 2.6, las = 0, cex = .8)
lines(xx, xx * dcauchy(xx), col = orange, lwd = 1.8)
lines(xx, xx * dnorm(xx), col = blue, lwd = 1.8, lty = 2)
legend("topleft", bty = "n", cex = .85, legend = c("Cauchy", "Normal"),
       col = c(orange, blue), lwd = 1.8, lty = c(1, 2))
dev.off()

# A convex function: the chord between two points lies above the graph.
pdf("assets/convex-chord.pdf", width = 4.8, height = 2.9,
    family = "Helvetica", useDingbats = FALSE)
par(mar = c(2.2, 7, .6, .6), mgp = c(1.4, .45, 0), las = 1, cex = .8)
r <- function(x) .25 * (x - 1.5)^2 + .5
x1 <- .1; x2 <- 4.2; t <- .5
xm <- t * x1 + (1 - t) * x2
ym <- t * r(x1) + (1 - t) * r(x2)
xx <- seq(.05, 4.6, length.out = 401)
plot(xx, r(xx), type = "n", xlim = c(0, 4.7), ylim = c(0, 2.9),
     axes = FALSE, xlab = "", ylab = "", xaxs = "i", yaxs = "i")
box(bty = "l", col = ink)
segments(c(x1, xm, x2), 0, c(x1, xm, x2), c(r(x1), ym, r(x2)),
         col = grid_col, lty = 2)
segments(0, c(r(xm), ym), xm, c(r(xm), ym), col = grid_col, lty = 2)
segments(0, c(r(x1), r(x2)), c(x1, x2), c(r(x1), r(x2)), col = grid_col, lty = 2)
lines(xx, r(xx), col = blue, lwd = 1.8)
lines(c(x1, x2), r(c(x1, x2)), col = orange, lwd = 1.6)
points(c(x1, x2, xm, xm), c(r(x1), r(x2), r(xm), ym), pch = 19, cex = .6,
       col = c(ink, ink, blue, orange))
axis(1, at = c(x1, xm, x2), labels = expression(x[1], t*x[1] + (1-t)*x[2], x[2]),
     tick = FALSE, cex.axis = .85)
axis(2, at = c(r(xm), r(x1), ym, r(x2)), tick = FALSE, cex.axis = .8,
     labels = expression(r(t*x[1] + (1-t)*x[2]), r(x[1]),
                         t*r(x[1]) + (1-t)*r(x[2]), r(x[2])))
text(4.45, r(4.45), "r(x)", pos = 2, col = blue, cex = .9)
dev.off()

# The standard Normal: density and CDF.
purple <- "#7A5195"
green <- "#2E8B3E"
pdf("assets/normal-pdf-cdf.pdf", width = 8, height = 2.3,
    family = "Helvetica", useDingbats = FALSE)
par(mfrow = c(1, 2), mar = c(2.6, 3.2, 1.6, .6),
    mgp = c(1.65, .45, 0), las = 1, cex = .78)
xx <- seq(-3.5, 3.5, length.out = 601)
plot(xx, dnorm(xx), type = "n", xlab = "x", ylab = "", ylim = c(0, .46),
     yaxs = "i", main = expression(f[X](x)), cex.main = 1)
grid(col = grid_col)
lines(xx, dnorm(xx), col = blue, lwd = 1.8)
segments(0, 0, 0, dnorm(0), col = ink, lty = 3)
text(0, dnorm(0), expression(f[X](0) %~~% 0.3989), pos = 3, cex = .85, col = ink)
plot(xx, pnorm(xx), type = "n", xlab = "x", ylab = "", ylim = c(0, 1.05),
     yaxs = "i", main = expression(F[X](x)), cex.main = 1)
grid(col = grid_col)
lines(xx, pnorm(xx), col = blue, lwd = 1.8)
segments(-3.5, .5, 0, .5, col = ink, lty = 3)
segments(0, 0, 0, .5, col = ink, lty = 3)
text(0, .5, expression(F[X](0) == 0.5), pos = 4, cex = .85, col = ink)
dev.off()

# Four Normals: the mean moves the bell, the variance stretches it.
pdf("assets/normal-family.pdf", width = 8, height = 2.5,
    family = "Helvetica", useDingbats = FALSE)
par(mfrow = c(1, 2), mar = c(2.6, 3.2, 1.6, .6),
    mgp = c(1.65, .45, 0), las = 1, cex = .78)
pars <- list(c(0, .2), c(0, 1), c(0, 5), c(-2, .5))
cols <- c(blue, orange, green, purple)
labs <- c(expression(mu == 0 ~ "," ~ sigma^2 == 0.2),
          expression(mu == 0 ~ "," ~ sigma^2 == 1),
          expression(mu == 0 ~ "," ~ sigma^2 == 5),
          expression(mu == -2 ~ "," ~ sigma^2 == 0.5))
xx <- seq(-5, 5, length.out = 801)
plot(xx, xx, type = "n", xlab = "x", ylab = "", ylim = c(0, .95),
     yaxs = "i", main = expression(f[X](x)), cex.main = 1)
grid(col = grid_col)
for (k in 1:4) lines(xx, dnorm(xx, pars[[k]][1], sqrt(pars[[k]][2])),
                     col = cols[k], lwd = 1.8)
legend("topright", legend = labs, col = cols, lwd = 1.8, bty = "n", cex = .8)
plot(xx, xx, type = "n", xlab = "x", ylab = "", ylim = c(0, 1.05),
     yaxs = "i", main = expression(F[X](x)), cex.main = 1)
grid(col = grid_col)
for (k in 1:4) lines(xx, pnorm(xx, pars[[k]][1], sqrt(pars[[k]][2])),
                     col = cols[k], lwd = 1.8)
dev.off()

# Quantiles of the standard Normal: 97.5% below 1.96, 2.5% below -1.96,
# 95% in between.
draw_area <- function(a, b, label, main) {
  xx <- seq(-3.5, 3.5, length.out = 601)
  plot(xx, dnorm(xx), type = "n", xlab = "", ylab = "", ylim = c(0, .45),
       yaxs = "i", axes = FALSE, main = main, cex.main = 1)
  axis(1, at = c(-1.96, 0, 1.96), labels = c("-1.96", "0", "1.96"),
       cex.axis = .85)
  sx <- xx[xx >= a & xx <= b]
  polygon(c(sx, rev(sx)), c(dnorm(sx), rep(0, length(sx))),
          col = adjustcolor(orange, .35), border = NA)
  lines(xx, dnorm(xx), col = blue, lwd = 1.8)
  text(mean(c(max(a, -3.5), min(b, 3.5))), .12, label, cex = .9, col = ink)
}
pdf("assets/normal-quantiles.pdf", width = 8, height = 2,
    family = "Helvetica", useDingbats = FALSE)
par(mfrow = c(1, 3), mar = c(2.2, .6, 1.6, .6), mgp = c(1.4, .45, 0), cex = .78)
draw_area(-Inf, 1.96, "97.5%", expression(P(Z <= 1.96)))
draw_area(-Inf, -1.96, "", expression(P(Z <= -1.96)))
text(-2.6, .06, "2.5%", cex = .9, col = ink)
draw_area(-1.96, 1.96, "95%", expression(P(-1.96 <= Z ~ "" <= 1.96)))
dev.off()

# Light tails: the log-density of the standard Normal is a parabola.
pdf("assets/normal-log-density.pdf", width = 4.6, height = 2.3,
    family = "Helvetica", useDingbats = FALSE)
par(mar = c(2.6, 3.4, .6, .6), mgp = c(1.65, .45, 0), las = 1, cex = .78)
xx <- seq(-5, 5, length.out = 601)
plot(xx, dnorm(xx, log = TRUE), type = "n", xlab = "x", ylab = "")
grid(col = grid_col)
mtext(expression(log ~ f[X](x)), side = 2, line = 2.2, las = 0, cex = .78)
lines(xx, dnorm(xx, log = TRUE), col = blue, lwd = 1.8)
dev.off()

# Standardization: N(170, 10^2) becomes N(0, 1); x = 190 becomes z = 2,
# and the area on its left stays the same.
draw_std <- function(mu, s, x0, main, xlab, lab) {
  xx <- seq(mu - 4 * s, mu + 4 * s, length.out = 601)
  yy <- dnorm(xx, mu, s)
  plot(xx, yy, type = "n", xlab = xlab, ylab = "", yaxs = "i",
       ylim = c(0, max(yy) * 1.25), main = main, cex.main = 1)
  grid(col = grid_col)
  sx <- xx[xx <= x0]
  polygon(c(sx, rev(sx)), c(dnorm(sx, mu, s), rep(0, length(sx))),
          col = adjustcolor(orange, .3), border = NA)
  lines(xx, yy, col = blue, lwd = 1.8)
  segments(x0, 0, x0, dnorm(x0, mu, s), col = orange, lwd = 1.5)
  text(x0, dnorm(x0, mu, s), lab, pos = 4, cex = .85, col = orange)
  segments(mu, 0, mu, dnorm(mu, mu, s), col = ink, lty = 3)
}
pdf("assets/normal-standardization.pdf", width = 8, height = 2.3,
    family = "Helvetica", useDingbats = FALSE)
par(mfrow = c(1, 2), mar = c(2.6, 3.4, 1.6, .6),
    mgp = c(1.65, .45, 0), las = 1, cex = .78)
draw_std(170, 10, 190, expression(X %~% N(170, 10^2)), "x", "x = 190")
draw_std(0, 1, 2, expression(Z == (X - 170) / 10 %~% N(0, 1)), "z", "z = 2")
dev.off()

# Learning: 50 made-up heights and two Normal candidates.
set.seed(7)
heights <- round(rnorm(50, 172, 7))
draw_heights <- function(main, mu = NULL, s = NULL, col = blue) {
  br <- seq(130, 205, by = 5)
  hist(heights, breaks = br, freq = FALSE, main = main, cex.main = 1,
       xlab = "height (cm)", ylab = "", xlim = c(130, 205), ylim = c(0, .085),
       col = adjustcolor(ink, .15), border = "white", yaxs = "i")
  rug(heights, col = ink)
  if (!is.null(mu)) {
    xx <- seq(130, 205, length.out = 400)
    lines(xx, dnorm(xx, mu, s), col = col, lwd = 2)
  }
}
pdf("assets/heights-candidates.pdf", width = 8, height = 2.3,
    family = "Helvetica", useDingbats = FALSE)
par(mfrow = c(1, 3), mar = c(2.6, 2.6, 1.6, .4),
    mgp = c(1.5, .45, 0), las = 1, cex = .72)
draw_heights("Observed heights")
draw_heights(expression(theta == (list(170, 10^2))), 170, 10, blue)
draw_heights(expression(theta == (list(150, 5^2))), 150, 5, orange)
dev.off()
cat("heights summary:", range(heights), mean(heights), "\n")

# A mixture of two Normals: women and men, each weighted 0.5.
pdf("assets/heights-mixture.pdf", width = 5.2, height = 2.5,
    family = "Helvetica", useDingbats = FALSE)
par(mar = c(2.6, 3.2, .6, .6), mgp = c(1.6, .45, 0), las = 1, cex = .78)
xx <- seq(140, 205, length.out = 600)
fw <- .5 * dnorm(xx, 163, 6.5)
fm <- .5 * dnorm(xx, 177, 7)
plot(xx, fw + fm, type = "n", xlab = "height (cm)", ylab = "",
     ylim = c(0, .047), yaxs = "i")
grid(col = grid_col)
lines(xx, fw, col = orange, lwd = 1.6, lty = 2)
lines(xx, fm, col = blue, lwd = 1.6, lty = 2)
lines(xx, fw + fm, col = ink, lwd = 2.2)
legend("topright", bty = "n", cex = .85, lwd = c(1.6, 1.6, 2.2),
       lty = c(2, 2, 1), col = c(orange, blue, ink),
       legend = c("p(height | woman) p(woman)", "p(height | man) p(man)",
                  "p(height)"))
dev.off()

# A Gaussian mixture with K = 3: three weighted bells and their sum.
pdf("assets/gmm-three.pdf", width = 5.2, height = 2.5,
    family = "Helvetica", useDingbats = FALSE)
par(mar = c(2.6, 3.2, .6, .6), mgp = c(1.6, .45, 0), las = 1, cex = .78)
xx <- seq(-6, 10, length.out = 800)
w <- c(.3, .45, .25); m <- c(-2, 2.5, 6.5); s <- c(1.1, 1.3, 1)
comp <- sapply(1:3, function(j) w[j] * dnorm(xx, m[j], s[j]))
tot <- rowSums(comp)
plot(xx, tot, type = "n", xlab = "o", ylab = "", ylim = c(0, max(tot) * 1.25),
     yaxs = "i", xaxt = "n")
axis(1, at = m, labels = expression(mu[1], mu[2], mu[3]))
grid(col = grid_col)
cols3 <- c(orange, blue, green)
for (j in 1:3) lines(xx, comp[, j], col = cols3[j], lwd = 1.6, lty = 2)
lines(xx, tot, col = ink, lwd = 2.2)
legend("topright", bty = "n", cex = .8, lwd = c(1.6, 1.6, 1.6, 2.2),
       lty = c(2, 2, 2, 1), col = c(cols3, ink),
       legend = c(expression(pi[1] * N(o * "|" * mu[1], sigma[1]^2)),
                  expression(pi[2] * N(o * "|" * mu[2], sigma[2]^2)),
                  expression(pi[3] * N(o * "|" * mu[3], sigma[3]^2)),
                  expression(f[O](o))))
dev.off()

# Labelled heights: split by group and fit one Normal to each part.
set.seed(2)
grp <- sample(c("woman", "man"), 50, TRUE)
hgt <- round(ifelse(grp == "woman", rnorm(50, 163, 6.5), rnorm(50, 177, 7)))
draw_group <- function(x, main, col) {
  m <- mean(x); s <- sqrt(mean((x - m)^2))
  hist(x, breaks = seq(140, 200, by = 5), freq = FALSE, main = main,
       cex.main = 1, xlab = "height (cm)", ylab = "", xlim = c(140, 200),
       ylim = c(0, .085), col = adjustcolor(col, .25), border = "white",
       yaxs = "i")
  rug(x, col = col)
  xx <- seq(140, 200, length.out = 400)
  lines(xx, dnorm(xx, m, s), col = col, lwd = 2)
}
pdf("assets/heights-split.pdf", width = 8, height = 2.4,
    family = "Helvetica", useDingbats = FALSE)
par(mfrow = c(1, 2), mar = c(2.6, 2.8, 1.6, .6),
    mgp = c(1.5, .45, 0), las = 1, cex = .75)
draw_group(hgt[grp == "woman"], "Women: 25 heights", orange)
draw_group(hgt[grp == "man"], "Men: 25 heights", blue)
dev.off()

# ELBO sketch: the log-likelihood and a lower bound F(q, theta) that never exceeds it.
pdf("assets/elbo-sketch.pdf", width = 5.2, height = 2.5,
    family = "Helvetica", useDingbats = FALSE)
par(mar = c(1.6, 1.2, .6, .6), mgp = c(1.6, .45, 0), las = 1, cex = .78)
tt <- seq(0, 10, length.out = 600)
lp <- 3 + 1.2 * exp(-(tt - 4)^2 / 6) + .8 * exp(-(tt - 7.5)^2 / 1.5)
fq <- 2.2 + 1.3 * exp(-(tt - 5)^2 / 5)
plot(tt, lp, type = "n", xlab = "", ylab = "", xaxt = "n",
     yaxt = "n", ylim = c(1.8, 4.8), yaxs = "i")
title(xlab = expression(theta), line = .5)
grid(col = grid_col)
lines(tt, lp, col = blue, lwd = 2.2)
lines(tt, fq, col = orange, lwd = 2.2, lty = 2)
legend("topleft", bty = "n", cex = .85, lwd = 2.2, lty = c(1, 2),
       col = c(blue, orange),
       legend = c(expression(log ~ p[theta](obs)), expression(F(q, theta))))
dev.off()

# ELBO before and after a change of theta: F goes up, log p_theta(obs) goes down.
elbo_lp <- function(t) 3 + 1.2 * exp(-(t - 4)^2 / 6) + .8 * exp(-(t - 7.5)^2 / 1.5)
elbo_fq <- function(t) 2.2 + 1.3 * exp(-(t - 5)^2 / 5)
elbo_panel <- function(file, t_now, t_old = NULL, label) {
  pdf(file, width = 3.6, height = 2.6, family = "Helvetica", useDingbats = FALSE)
  par(mar = c(2.6, 1.2, 1.4, .6), mgp = c(1.6, .45, 0), las = 1, cex = .78)
  tt <- seq(0, 10, length.out = 600)
  plot(tt, elbo_lp(tt), type = "n", xlab = "", ylab = "", xaxt = "n",
       yaxt = "n", ylim = c(1.8, 4.8), yaxs = "i", main = label,
       cex.main = 1, font.main = 1)
  axis(1, at = c(t_old, t_now),
       labels = if (is.null(t_old)) expression(theta[old])
                else expression(theta[old], theta[new]))
  grid(col = grid_col)
  lines(tt, elbo_lp(tt), col = blue, lwd = 2.2)
  lines(tt, elbo_fq(tt), col = orange, lwd = 2.2, lty = 2)
  if (!is.null(t_old)) {
    points(c(t_old, t_old), c(elbo_lp(t_old), elbo_fq(t_old)),
           pch = 21, col = "grey55", bg = "white", cex = 1.1)
    segments(t_old, elbo_fq(t_old), t_old, elbo_lp(t_old), col = "grey65",
             lty = 3)
  }
  segments(t_now, elbo_fq(t_now), t_now, elbo_lp(t_now), col = ink, lty = 3)
  points(t_now, elbo_lp(t_now), pch = 19, col = blue, cex = 1.1)
  points(t_now, elbo_fq(t_now), pch = 19, col = orange, cex = 1.1)
  legend("topleft", bty = "n", cex = .8, lwd = 2.2, lty = c(1, 2),
         col = c(blue, orange),
         legend = c(expression(log ~ p[theta](obs)), expression(F(q, theta))))
  dev.off()
}
elbo_panel("assets/elbo-before.pdf", t_now = 7.5, label = "Before")
elbo_panel("assets/elbo-after.pdf", t_now = 6, t_old = 7.5, label = "After")
cat("before lp", elbo_lp(7.5), "F", elbo_fq(7.5), "after lp", elbo_lp(6), "F", elbo_fq(6), "\n")

# ELBO with q equal to the posterior at theta_old: it touches log p_theta(obs) there.
pdf("assets/elbo-touch.pdf", width = 5.2, height = 2.8,
    family = "Helvetica", useDingbats = FALSE)
par(mar = c(1.8, 1.2, .6, .6), mgp = c(1.6, .45, 0), las = 1, cex = .78)
t0 <- 7.5
elbo_touch <- function(t) elbo_lp(t) - .12 * (t - t0)^2
tt <- seq(0, 10, length.out = 600)
plot(tt, elbo_lp(tt), type = "n", xlab = "", ylab = "", xaxt = "n",
     yaxt = "n", ylim = c(1.8, 4.8), yaxs = "i")
axis(1, at = t0, labels = expression(theta[old]))
grid(col = grid_col)
lines(tt, elbo_fq(tt), col = "grey70", lwd = 1.6, lty = 2)
lines(tt, elbo_lp(tt), col = blue, lwd = 2.2)
lines(tt, elbo_touch(tt), col = orange, lwd = 2.2, lty = 2)
segments(t0, 1.8, t0, elbo_lp(t0), col = ink, lty = 3)
points(t0, elbo_lp(t0), pch = 21, col = ink, bg = orange, cex = 1.2)
legend("topleft", bty = "n", cex = .8, lwd = c(2.2, 2.2, 1.6),
       lty = c(1, 2, 2), col = c(blue, orange, "grey70"),
       legend = c(expression(log ~ p[theta](obs)),
                  expression(F(q, theta) ~ "with" ~
                             q == p[theta[old]](hid ~ "|" ~ obs)),
                  expression(F(q, theta) ~ "with the" ~ q ~ "of Example 18")))
dev.off()

# Coordinate ascent on F(q, theta): a step in q, then a step in theta, and so on.
pdf("assets/em-coordinate-ascent.pdf", width = 4.2, height = 3,
    family = "Helvetica", useDingbats = FALSE)
par(mar = c(2.2, 2.2, .6, .6), mgp = c(1, .45, 0), las = 1, cex = .78)
a <- 1; b <- 1; cc <- .8; x0 <- 6; y0 <- 6
Fxy <- function(x, y) -(a * (x - x0)^2 + b * (y - y0)^2 + 2 * cc * (x - x0) * (y - y0))
gx <- seq(0, 10, length.out = 200); gy <- seq(0, 10, length.out = 200)
z <- outer(gx, gy, Fxy)
contour(gx, gy, z, levels = -c(1, 4, 9, 16, 25, 36, 49), drawlabels = FALSE,
        col = "grey70", xaxt = "n", yaxt = "n", xlab = "", ylab = "", xaxs = "i",
        yaxs = "i")
title(xlab = "q (a distribution)", ylab = expression(theta ~ "(a parameter)"),
      line = .6)
px <- 1.2; py <- 9; path_x <- px; path_y <- py
for (k in 1:6) {
  px <- x0 - cc * (py - y0) / a; path_x <- c(path_x, px); path_y <- c(path_y, py)
  py <- y0 - cc * (px - x0) / b; path_x <- c(path_x, px); path_y <- c(path_y, py)
}
lines(path_x, path_y, col = orange, lwd = 1.8)
points(path_x[1], path_y[1], pch = 19, col = ink, cex = .9)
points(x0, y0, pch = 4, col = ink, cex = 1.1, lwd = 1.6)
text(path_x[1], path_y[1], "start", pos = 4, cex = .85, col = ink)
dev.off()

# EM step by step: each E-step builds a lower bound that touches log p at the
# current theta, each M-step moves to the top of that bound.
em_bound <- function(t, at) elbo_lp(t) - .06 * (t - at)^2
em_argmax <- function(at) optimize(function(t) em_bound(t, at), c(0, 10),
                                   maximum = TRUE)$maximum
th <- c(.6); for (k in 1:2) th <- c(th, em_argmax(th[k]))
pdf("assets/em-steps.pdf", width = 7, height = 4.6, family = "Helvetica",
    useDingbats = FALSE)
par(mfrow = c(2, 2), mar = c(2, 1, 1.6, .6), mgp = c(1.6, .4, 0), las = 1,
    cex = .72)
tt <- seq(0, 10, length.out = 600)
em_panel <- function(title, at, show_move, labels) {
  plot(tt, elbo_lp(tt), type = "n", xlab = "", ylab = "", xaxt = "n",
       yaxt = "n", ylim = c(1.8, 4.8), yaxs = "i", main = title,
       cex.main = 1, font.main = 1)
  grid(col = grid_col)
  lines(tt, elbo_lp(tt), col = blue, lwd = 2)
  lines(tt, em_bound(tt, at), col = orange, lwd = 2, lty = 2)
  ticks <- at; labs <- labels[1]
  points(at, elbo_lp(at), pch = 21, col = ink, bg = orange, cex = 1.1)
  if (show_move) {
    nw <- em_argmax(at)
    segments(nw, em_bound(nw, at), nw, elbo_lp(nw), col = ink, lty = 3)
    points(nw, em_bound(nw, at), pch = 19, col = orange, cex = 1)
    points(nw, elbo_lp(nw), pch = 19, col = blue, cex = 1.1)
    arrows(at, 2.05, nw, 2.05, length = .07, col = ink)
    ticks <- c(at, nw); labs <- labels
    if (abs(nw - at) < 1) { ticks <- nw; labs <- labels[2] }
  }
  axis(1, at = ticks, labels = labs)
}
em_panel("E-step, t = 1", th[1], FALSE, expression(theta^(0)))
em_panel("M-step, t = 1", th[1], TRUE, expression(theta^(0), theta^(1)))
em_panel("E-step, t = 2", th[2], FALSE, expression(theta^(1)))
em_panel("M-step, t = 2", th[2], TRUE, expression(theta^(1), theta^(2)))
dev.off()
cat("EM thetas", th, "lp", elbo_lp(th), "\n")
