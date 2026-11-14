"""Recreate the vector TikZ illustrations of k-means' geometric limitations."""
from pathlib import Path
import numpy as np

DEST = Path(__file__).resolve().parent
RNG = np.random.default_rng(10112026)
COLORS = ['ClA', 'ClB', 'ClC']


def hull(points):
    points = sorted(set(map(tuple, points)))
    def cross(a, b, c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    lower, upper = [], []
    for seq, out in [(points, lower), (reversed(points), upper)]:
        for p in seq:
            while len(out) > 1 and cross(out[-2], out[-1], p) <= 0:
                out.pop()
            out.append(p)
    return lower[:-1] + upper[:-1]


def lloyd(data, k):
    best = None
    for _ in range(40):
        centres = data[RNG.choice(len(data), k, replace=False)].copy()
        for _ in range(100):
            labels = ((data[:, None] - centres)**2).sum(axis=2).argmin(axis=1)
            if any(not np.any(labels == j) for j in range(k)):
                break
            updated = np.array([data[labels == j].mean(axis=0) for j in range(k)])
            if np.allclose(updated, centres):
                score = ((data - updated[labels])**2).sum()
                if best is None or score < best[0]:
                    best = score, labels.copy()
                break
            centres = updated
    assert best is not None
    return best[1]


def figure(name, data, natural, k, curves=None):
    result = lloyd(data, k)
    lo, hi = data.min(axis=0), data.max(axis=0)
    scale = min(5.4/(hi[0]-lo[0]), 3.4/(hi[1]-lo[1]))
    centre = (lo + hi)/2
    def coord(p):
        p = (np.array(p)-centre)*scale + [2.9, 1.9]
        return f'({p[0]:.4f},{p[1]:.4f})'
    lines = [r'\begin{tikzpicture}[x=1cm,y=1cm]']
    for panel, (labels, title) in enumerate([(natural, 'Geometric groups'), (result, '$k$-means partition')]):
        lines += [f'\\begin{{scope}}[xshift={panel*6.9}cm]',
                  r'\draw[gray!55,->] (0,0)--(6,0) node[right,font=\small] {$x_1$};',
                  r'\draw[gray!55,->] (0,0)--(0,3.9) node[above,font=\small] {$x_2$};',
                  f'\\node[font=\\small] at (2.9,-0.45) {{{title}}};']
        for j in range(k):
            pts = data[labels == j]
            color = COLORS[j]
            if panel == 0 and curves is not None:
                path = ' '.join(coord(p) for p in curves[j])
                lines.append(f'\\draw[{color}!22,line width=12pt,line cap=round,line join=round] plot[smooth] coordinates {{{path}}};')
            else:
                path = '--'.join(coord(p) for p in hull(pts))
                lines.append(f'\\path[fill={color}!18,draw={color}!35,line join=round] {path}--cycle;')
            for p in pts:
                lines.append(f'\\node[circle,fill={color},draw=black,line width=0.15pt,inner sep=0.8pt] at {coord(p)} {{}};')
            lines.append(f'\\node[diamond,fill={color},draw=black,line width=0.6pt,inner sep=2pt] at {coord(pts.mean(axis=0))} {{}};')
        lines.append(r'\end{scope}')
    lines.append(r'\end{tikzpicture}')
    (DEST / f'kmeans-{name}.tex').write_text('\n'.join(lines)+'\n')
    print(name, 'group counts', np.bincount(natural).tolist(),
          'assignments by source group', [np.bincount(result[natural == j], minlength=k).tolist() for j in range(k)])


def blobs(counts, means, scales):
    data = np.vstack([RNG.normal(mean, scale, size=(n, 2)) for n, mean, scale in zip(counts, means, scales)])
    labels = np.repeat(np.arange(len(counts)), counts)
    return data, labels


if __name__ == '__main__':
    x, labels = blobs([150, 22, 22], [(0, 0), (-4, 0), (4, 0)], [1.25, .25, .25])
    figure('sizes', x, labels, 3)
    x, labels = blobs([140, 32, 32], [(0, 0), (5, 1), (5, -1)], [1.35, .18, .18])
    figure('densities', x, labels, 3)
    t = np.linspace(0, np.pi, 85)
    curves = [np.c_[np.cos(t), np.sin(t)], np.c_[1-np.cos(t), .5-np.sin(t)]]
    x = np.vstack(curves) + RNG.normal(0, .035, (170, 2))
    figure('shapes', x, np.repeat([0, 1], 85), 2, curves)
