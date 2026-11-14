#!/usr/bin/env python3
"""FDS Pokémon Battles 2026: idea1.

The idea: rebuild what the timeline hides and give the model Player 1's history.

1. Hidden knockouts. Player 2's `fnt` state shows only on a double KO or when
   Player 2 has no Pokémon left, so most P2 knockouts look like ordinary
   switches. Player 1's knockouts are always shown, so P1's switches act as a
   control group: a classifier tells P2 "vanishings" (a Pokémon leaves the
   field and never comes back) from P1 ones, and the excess of P2 events over
   P1 events with the same description estimates how often it was a knockout.
2. Player 2's bench. Teams come from a pool shared by both players: the
   Pokémon P2 has revealed are matched against the P1 teams (and the fully
   revealed P2 teams) of every battle, train and test, to estimate who is
   still unseen on P2's bench. The ablation measures it (configs D and H);
   the final model leaves it out because it adds nothing there.
3. Player 1's history. The win rate of the same P1 team in other battles, as an
   out-of-fold target encoding computed inside every CV fold.

On top of these come the feature families that helped in earlier experiments:
P1 team species, P1 items, and P1-minus-P2 move counts.

The script runs the same way locally and in a Kaggle kernel. It prints and
saves a repeated-CV report, fits the final model on all training battles and
writes `submission.csv`. It never submits anything.

Usage (local):  python idea1.py [--quick] [--no-ablation]
"""

import argparse
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler

COMPETITION = 'fds-pokemon-battles-prediction-2026'
SEED = 2026
N_FOLDS = 5
N_REPEATS = 3
TE_SMOOTHING = 20          # pseudo-battles of prior in the team target encoding
N_JOBS = os.cpu_count() or 4

STATUSES = ('slp', 'par', 'frz', 'tox', 'psn', 'brn')
BOOSTS = ('atk', 'def', 'spa', 'spd', 'spe')
EFFECTS = ('substitute', 'leechseed', 'confusion', 'perish', 'trapped', 'encore',
           'attract', 'nightmare', 'clamp', 'whirlpool', 'wrap', 'firespin', 'bind',
           'curse', 'destinybond', 'protect', 'endure', 'focusenergy')
SIDES = (('p1', 'p2'), ('p2', 'p1'))
STAT_NAMES = ('hp', 'atk', 'def', 'spa', 'spd', 'spe')

# Vocabulary thresholds (counts over train + test, labels never used).
MIN_SPECIES = 30
MIN_ITEM = 20
MIN_MOVE = 100

LGB_PARAMS = dict(n_estimators=700, learning_rate=0.02, num_leaves=12,
                  min_child_samples=50, subsample=0.8, subsample_freq=1,
                  colsample_bytree=0.4, reg_lambda=2.0, verbose=-1)
LOGREG_C = 0.005

START = time.time()


def log(msg):
    print(f'[{time.time() - START:7.1f}s] {msg}', flush=True)


# ---------------------------------------------------------------------------
# Paths and loading
# ---------------------------------------------------------------------------

def script_dir():
    return Path(__file__).resolve().parent if '__file__' in globals() else Path.cwd()


def find_data_dir():
    candidates = []
    if os.environ.get('FDS_DATA'):
        candidates.append(Path(os.environ['FDS_DATA']))
    candidates += [Path('/kaggle/input') / COMPETITION,
                   Path('/kaggle/input/competitions') / COMPETITION,
                   script_dir().parent / 'data', script_dir() / 'data']
    for c in candidates:
        if (c / 'train.jsonl').exists():
            return c
    kaggle_input = Path('/kaggle/input')
    if kaggle_input.exists():
        for p in sorted(kaggle_input.rglob('train.jsonl')):
            return p.parent
    raise FileNotFoundError('train.jsonl not found: set the FDS_DATA environment variable')


def find_out_dir():
    if Path('/kaggle/working').exists():
        return Path('/kaggle/working')
    out = script_dir() / 'outputs' / 'local'
    out.mkdir(parents=True, exist_ok=True)
    return out


def load_jsonl(path):
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def clean(name):
    return re.sub(r'[^0-9a-zA-Z_]', '_', name)


# ---------------------------------------------------------------------------
# Reference tables, built from competition data only
# ---------------------------------------------------------------------------

class Reference:
    """Species types and base stats, read from the teams and leads in the data."""

    def __init__(self, battles):
        self.species = {}
        for b in battles:
            for p in b['p1_team_details'] + [b['p2_lead_details']]:
                if p['name'] not in self.species:
                    self.species[p['name']] = {
                        'types': tuple(t for t in p['types'] if t != 'notype'),
                        'stats': np.array([p['base_' + s] for s in STAT_NAMES], dtype=float)}
        self.mean_stats = np.mean([v['stats'] for v in self.species.values()], axis=0)

    def types(self, name):
        sp = self.species.get(name)
        return sp['types'] if sp else ()

    def stats(self, name):
        sp = self.species.get(name)
        return sp['stats'] if sp else self.mean_stats


def p2_seen(b):
    return frozenset([b['p2_lead_details']['name']] +
                     [t['p2_pokemon_state']['name'] for t in b['battle_timeline']])


def p1_species(b):
    return frozenset(p['name'] for p in b['p1_team_details'])


# ---------------------------------------------------------------------------
# Field state: Spikes
# ---------------------------------------------------------------------------

def spikes_after(tl, ref):
    """For every record, whether Spikes lie on each side's field after it.

    Spikes land on a side when the opponent uses the move, and leave it when the
    side uses Rapid Spin against a non-Ghost opponent (Ghosts block the spin).
    """
    on = {'p1': False, 'p2': False}
    out = {'p1': [], 'p2': []}
    for t in tl:
        for side, opp in SIDES:
            mo = t[opp + '_move_details']
            if mo is not None and mo['name'] == 'spikes':
                on[side] = True
        for side, opp in SIDES:
            ms = t[side + '_move_details']
            if (ms is not None and ms['name'] == 'rapidspin'
                    and 'ghost' not in ref.types(t[opp + '_pokemon_state']['name'])):
                on[side] = False
        for side in out:
            out[side].append(on[side])
    return out


# ---------------------------------------------------------------------------
# Hidden knockouts of Player 2
# ---------------------------------------------------------------------------

STATUS_CODE = {'nostatus': 0, 'slp': 1, 'par': 2, 'frz': 3, 'tox': 4, 'psn': 5, 'brn': 6}
KO_PARAMS = dict(n_estimators=400, learning_rate=0.03, num_leaves=15, min_child_samples=200,
                 subsample=0.8, subsample_freq=1, colsample_bytree=0.8, verbose=-1)
KO_SPLITS = 3   # the vanishing classifier is averaged over this many battle splits


def vanish_events(tl, side, spikes):
    """Switch-outs after which the Pokémon never shows up again in the 30 records.

    Each event gets a description `x` that reads the same for either player:
    the leaver's HP, status and last HP drop, the base power of both players'
    moves in the leaving record and the next one, the opponent's HP drop
    (Explosion users), and whether the replacement came in unhurt (Spikes
    aside): after a knockout the replacement enters at the end of the turn,
    while after a voluntary switch it usually takes the opponent's attack.
    """
    opp = 'p2' if side == 'p1' else 'p1'
    names = [t[side + '_pokemon_state']['name'] for t in tl]
    last_hp = {}
    events = []
    for i, t in enumerate(tl):
        cur = t[side + '_pokemon_state']
        if i > 0:
            prev = tl[i - 1][side + '_pokemon_state']
            if (prev['name'] != cur['name'] and prev['status'] != 'fnt'
                    and prev['name'] not in names[i:]):
                om = t[opp + '_move_details']
                hit = om is not None and om['base_power'] > 0
                allowance = 0.02 + (0.125 if spikes[side][i - 1] else 0.0)
                unhurt = last_hp.get(cur['name'], 1.0) - cur['hp_pct'] <= allowance
                before = tl[i - 2][side + '_pokemon_state'] if i >= 2 else None
                x = {'i': i, 'hp': prev['hp_pct'], 'status': STATUS_CODE.get(prev['status'], 7),
                     'drop': (before['hp_pct'] - prev['hp_pct']
                              if before is not None and before['name'] == prev['name'] else np.nan),
                     'signature': int(hit and unhurt), 'unhurt': int(unhurt),
                     'spikes': int(spikes[side][i - 1]), 'rep_hp': cur['hp_pct'],
                     'opp_switch': int(tl[i - 1][opp + '_pokemon_state']['name'] != t[opp + '_pokemon_state']['name'])}
                for j, tag in ((i - 1, 'prev'), (i, 'cur')):
                    mv, att = tl[j][opp + '_move_details'], tl[j][opp + '_pokemon_state']
                    own = tl[j][side + '_move_details']
                    x[f'opp_bp_{tag}'] = mv['base_power'] if mv else -1
                    x[f'own_bp_{tag}'] = own['base_power'] if own else -1
                    att_before = tl[j - 1][opp + '_pokemon_state'] if j > 0 else None
                    x[f'opp_drop_{tag}'] = (att_before['hp_pct'] - att['hp_pct']
                                            if att_before is not None and att_before['name'] == att['name'] else np.nan)
                events.append({'name': prev['name'], 'x': x})
        last_hp[cur['name']] = cur['hp_pct']
    return events


def calibrate_hidden_kos(battles, ref):
    """P(knockout) for every P2 vanishing, using P1's vanishings as the control.

    P1's knockouts are always visible, so every P1 vanishing is a real switch.
    Both players switch alike, so where P2 events outnumber P1 events with the
    same description, the excess is hidden P2 knockouts. A classifier telling
    P2 events from P1 events estimates the ratio n2(x) / n1(x) and
    P(KO | x) = 1 - n1(x) / n2(x). Predictions are out-of-fold by battle and
    averaged over KO_SPLITS splits; one scale factor makes the expected total
    equal the overall excess.
    Battle labels are not used. Returns (per_battle, info): one list of
    probabilities per battle, in vanish_events order, and calibration statistics.
    """
    rows, side, owner = [], [], []
    for k, b in enumerate(battles):
        tl = b['battle_timeline']
        sp = spikes_after(tl, ref)
        for s in ('p1', 'p2'):
            for e in vanish_events(tl, s, sp):
                rows.append(e['x'])
                side.append(int(s == 'p2'))
                owner.append(k)
    X, side, owner = pd.DataFrame(rows), np.array(side), np.array(owner)
    q = np.zeros(len(side))
    for r in range(KO_SPLITS):
        # Battles go to folds through a seeded permutation, which is the same on
        # every platform (GroupKFold breaks ties with an unstable sort).
        fold = np.random.RandomState(SEED + r).permutation(len(battles))[owner] % 5
        for k in range(5):
            a, v = fold != k, fold == k
            m = lgb.LGBMClassifier(**KO_PARAMS, random_state=SEED + r, n_jobs=N_JOBS)
            m.fit(X[a], side[a])
            q[v] += m.predict_proba(X[v])[:, 1] / KO_SPLITS
    is_p2 = side == 1
    odds = (1 - q[is_p2]) / q[is_p2]
    target = is_p2.sum() - (~is_p2).sum()
    lo, hi = 0.5, 3.0   # bisection on the scale factor
    for _ in range(50):
        c = (lo + hi) / 2
        lo, hi = (c, hi) if np.clip(1 - c * odds, 0, 1).sum() > target else (lo, c)
    p = np.clip(1 - c * odds, 0, 1)
    per_battle = [[] for _ in battles]
    for k, pk in zip(owner[is_p2], p):
        per_battle[k].append(float(pk))
    return per_battle, {'scale': c, 'p2_events': int(is_p2.sum()), 'p1_events': int((~is_p2).sum()),
                        'mean': float(p.mean()), 'sd': float(p.std())}


# ---------------------------------------------------------------------------
# Player 2's bench from the shared team pool
# ---------------------------------------------------------------------------

class TeamPool:
    """Every team seen in the data: P1 teams and fully revealed P2 teams."""

    def __init__(self, battles):
        count = Counter()
        for b in battles:
            count[p1_species(b)] += 1
            seen = p2_seen(b)
            if len(seen) == 6:
                count[seen] += 1
        self.teams = list(count)
        self.weights = np.array([count[t] for t in self.teams], dtype=float)
        self.index = defaultdict(set)
        for k, team in enumerate(self.teams):
            for s in team:
                self.index[s].add(k)

    def bench(self, seen):
        """Expected count of each unseen species on P2's team.

        Uses the teams that contain every revealed Pokémon; if there are none,
        the teams with the largest overlap. Returns (posterior, n_candidates,
        exact_match).
        """
        need = 6 - len(seen)
        if need <= 0:
            return {}, 0, 1
        sets = [self.index.get(s, set()) for s in seen]
        cands = set.intersection(*sets) if sets else set()
        exact = 1
        if not cands:
            exact = 0
            overlap = Counter()
            for s in sets:
                for k in s:
                    overlap[k] += 1
            if not overlap:
                return {}, 0, 0
            best = max(overlap.values())
            cands = {k for k, v in overlap.items() if v == best}
        post, total = Counter(), 0.0
        for k in sorted(cands):
            rest = self.teams[k] - seen
            if not rest:
                continue
            w = self.weights[k]
            scale = need / len(rest)   # loose matches leave more than `need` members
            for s in sorted(rest):   # sorted: set order changes with the hash seed
                post[s] += w * scale
            total += w
        if total == 0:
            return {}, len(cands), exact
        return {s: v / total for s, v in post.items()}, len(cands), exact


# ---------------------------------------------------------------------------
# Per-battle features
# ---------------------------------------------------------------------------

def battle_features(b, ref, pool, ko_probs, vocab):
    """Static features of one battle. Column prefixes define the feature groups."""
    tl = b['battle_timeline']
    sp = spikes_after(tl, ref)
    f = {}

    # Hidden knockouts of P2: probability per vanished Pokémon.
    ko_prob = {'p1': {}, 'p2': {}}
    p2_events = vanish_events(tl, 'p2', sp)
    for e, pk in zip(p2_events, ko_probs):
        ko_prob['p2'][e['name']] = pk
    f['ko_p2_vanished'] = len(p2_events)
    f['ko_p2_hidden_sum'] = sum(ko_prob['p2'].values())

    alive_w = {}
    for side, opp in SIDES:
        last = {}
        for t in tl:
            s = t[side + '_pokemon_state']
            last[s['name']] = s
        fnt = {n for n, s in last.items() if s['status'] == 'fnt'}
        n_unseen = 6 - len(last)   # P1: never sent out; P2: not revealed yet
        w = {n: (0.0 if n in fnt else 1.0 - ko_prob[side].get(n, 0.0)) for n in last}
        alive_w[side] = w

        # core: unaffected by the knockout correction
        f[f'core_{side}_seen'] = len(last)
        f[f'core_{side}_fnt'] = len(fnt)
        act = tl[-1][side + '_pokemon_state']
        f[f'core_{side}_act_hp'] = act['hp_pct']
        f[f'core_{side}_act_fnt'] = int(act['status'] == 'fnt')
        for st in STATUSES:
            f[f'core_{side}_act_{st}'] = int(act['status'] == st)
        for k in BOOSTS:
            f[f'core_{side}_act_boost_{k}'] = act['boosts'][k]
        for e in EFFECTS:
            f[f'core_{side}_act_eff_{e}'] = int(e in act['effects'])
        f[f'core_{side}_spikes'] = int(sp[side][-1])

        # naive: what the timeline shows at face value
        alive_naive = [s for n, s in last.items() if n not in fnt]
        f[f'naive_{side}_alive'] = 6 - len(fnt)
        f[f'naive_{side}_hp'] = sum(s['hp_pct'] for s in alive_naive) + n_unseen
        f[f'naive_{side}_low'] = sum(1 for s in alive_naive if s['hp_pct'] < 0.25)
        f[f'naive_{side}_healthy'] = sum(1 for s in alive_naive if s['hp_pct'] >= 0.75) + n_unseen
        for st in STATUSES:
            f[f'naive_{side}_st_{st}'] = sum(1 for s in alive_naive if s['status'] == st)

        # ko: same quantities with P2's hidden knockouts removed in expectation
        f[f'ko_{side}_alive'] = sum(w.values()) + n_unseen
        f[f'ko_{side}_hp'] = sum(s['hp_pct'] * w[n] for n, s in last.items()) + n_unseen
        f[f'ko_{side}_low'] = sum(w[n] for n, s in last.items() if 0 < s['hp_pct'] < 0.25)
        f[f'ko_{side}_healthy'] = sum(w[n] for n, s in last.items() if s['hp_pct'] >= 0.75) + n_unseen
        for st in STATUSES:
            f[f'ko_{side}_st_{st}'] = sum(w[n] for n, s in last.items() if s['status'] == st)

    for prefix in ('core', 'naive', 'ko'):
        for key in [k for k in f if k.startswith(prefix + '_p1_')]:
            other = key.replace('_p1_', '_p2_', 1)
            if other in f:
                f[key.replace('_p1_', '_d_', 1)] = f[key] - f[other]

    # P1 team composition and items
    for p in b['p1_team_details']:
        if p['name'] in vocab['species']:
            f['p1sp_' + clean(p['name'])] = 1
        if p['item'] in vocab['items']:
            f['it_' + clean(p['item'])] = f.get('it_' + clean(p['item']), 0) + 1
    levels = [p['level'] for p in b['p1_team_details']]
    f['p1sp_min_level'] = min(levels)

    # Moves used: P1 count minus P2 count, per move name
    for t in tl:
        for side, sign in (('p1', 1), ('p2', -1)):
            m = t[side + '_move_details']
            if m is not None and m['name'] in vocab['moves']:
                key = 'mv_' + clean(m['name'])
                f[key] = f.get(key, 0) + sign

    # P2 composition: revealed Pokémon weighted by survival, plus the bench
    seen = p2_seen(b)
    post, n_cand, exact = pool.bench(seen)
    for n, wt in alive_w['p2'].items():
        if n in vocab['species']:
            f['p2sp_' + clean(n)] = wt
    lead = b['p2_lead_details']['name']
    if lead not in alive_w['p2'] and lead in vocab['species']:
        f['p2sp_' + clean(lead)] = 1.0
    for n, pr in post.items():
        if n in vocab['species']:
            f['bench_sp_' + clean(n)] = pr
    need = 6 - len(seen)
    f['bench_need'] = need
    f['bench_cands'] = np.log1p(n_cand)
    f['bench_exact'] = exact
    if post:
        tot = sum(post.values())
        exp_stats = sum(ref.stats(n) * pr for n, pr in sorted(post.items())) / tot
    else:
        exp_stats = ref.mean_stats
    for k, s in enumerate(STAT_NAMES):
        f[f'bench_{s}'] = exp_stats[k] if need > 0 else 0.0
    f['bench_bst'] = float(exp_stats.sum()) if need > 0 else 0.0
    return f


def build_vocab(battles):
    sp, it, mv = Counter(), Counter(), Counter()
    for b in battles:
        for p in b['p1_team_details']:
            sp[p['name']] += 1
            it[p['item']] += 1
        for t in b['battle_timeline']:
            for side in ('p1', 'p2'):
                m = t[side + '_move_details']
                if m is not None:
                    mv[m['name']] += 1
    return {'species': {k for k, v in sp.items() if v >= MIN_SPECIES},
            'items': {k for k, v in it.items() if v >= MIN_ITEM},
            'moves': {k for k, v in mv.items() if v >= MIN_MOVE}}


def build_static(battles, ref, pool, ko_probs, vocab):
    rows = [battle_features(b, ref, pool, kp, vocab) for b, kp in zip(battles, ko_probs)]
    X = pd.DataFrame(rows).fillna(0.0).astype(np.float32)
    return X[sorted(X.columns)]


# ---------------------------------------------------------------------------
# Player 1's history: out-of-fold target encoding of the P1 team
# ---------------------------------------------------------------------------

def history_keys(battles):
    team = np.array(['|'.join(sorted(p['name'] for p in b['p1_team_details'])) for b in battles], dtype=object)
    team_items = np.array(['|'.join(sorted(p['name'] + ':' + p['item'] for p in b['p1_team_details']))
                           for b in battles], dtype=object)
    return {'hist_team': team, 'hist_team_items': team_items}


def target_encode(keys, y, fit_idx, apply_idx, prior, m=TE_SMOOTHING):
    s, n = defaultdict(float), defaultdict(int)
    for k, t in zip(keys[fit_idx], y[fit_idx]):
        s[k] += t
        n[k] += 1
    return np.array([(s[k] + prior * m) / (n[k] + m) for k in keys[apply_idx]])


def history_features(keys_by_name, y, fit_idx, apply_idx, seed):
    """Encodings for the fitting rows (out-of-fold inside them) and the apply rows.

    Only labels of `fit_idx` are read, so validation and test labels never leak.
    """
    prior = float(y[fit_idx].mean())
    fit_cols, app_cols = {}, {}
    inner = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
    for name, keys in keys_by_name.items():
        col = np.zeros(len(fit_idx))
        for ia, ib in inner.split(np.zeros(len(fit_idx)), y[fit_idx]):
            col[ib] = target_encode(keys, y, fit_idx[ia], fit_idx[ib], prior)
        fit_cols[name] = col
        app_cols[name] = target_encode(keys, y, fit_idx, apply_idx, prior)
    return (pd.DataFrame(fit_cols).astype(np.float32),
            pd.DataFrame(app_cols).astype(np.float32))


def frequency_features(keys_by_name):
    """How often each P1 team appears in train + test (labels not used)."""
    out = {}
    for name, keys in keys_by_name.items():
        c = Counter(keys)
        out[name.replace('hist_', 'freq_')] = np.log1p([c[k] for k in keys])
    return pd.DataFrame(out).astype(np.float32)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

def fit_predict(model, Xa, ya, Xv, seed):
    """Probability that P1 wins for the rows of Xv."""
    if model == 'lgb':
        m = lgb.LGBMClassifier(**LGB_PARAMS, random_state=seed, n_jobs=N_JOBS)
        m.fit(Xa, ya)
        return m.predict_proba(Xv)[:, 1], m
    if model == 'logreg':
        scaler = StandardScaler().fit(Xa.values)
        m = LogisticRegression(C=LOGREG_C, max_iter=5000)
        m.fit(scaler.transform(Xa.values), ya)
        return m.predict_proba(scaler.transform(Xv.values))[:, 1], m
    raise ValueError(model)


# ---------------------------------------------------------------------------
# Repeated cross-validation
# ---------------------------------------------------------------------------

def make_folds(y, n_folds, n_repeats, seed):
    folds = []
    for r in range(n_repeats):
        skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=seed + r)
        for a, v in skf.split(np.zeros(len(y)), y):
            folds.append((r, a, v))
    return folds


def select_columns(columns, groups):
    prefixes = tuple(g + '_' for g in groups)
    return [c for c in columns if c.startswith(prefixes)]


def run_cv(name, X, groups, use_history, model, folds, y, hist_cache, freq):
    cols = select_columns(X.columns, groups)
    accs, oof = [], np.zeros((N_REPEATS_RUN, len(y)))
    for k, (r, a, v) in enumerate(folds):
        Xa = X.iloc[a][cols].reset_index(drop=True)
        Xv = X.iloc[v][cols].reset_index(drop=True)
        if use_history:
            ha, hv = hist_cache[k]
            Xa = pd.concat([Xa, ha, freq.iloc[a].reset_index(drop=True)], axis=1)
            Xv = pd.concat([Xv, hv, freq.iloc[v].reset_index(drop=True)], axis=1)
        p, _ = fit_predict(model, Xa, y[a], Xv, SEED + k)
        oof[r, v] = p
        accs.append(float(((p > 0.5) == y[v]).mean()))
    per_repeat = [float(((oof[r] > 0.5) == y).mean()) for r in range(N_REPEATS_RUN)]
    res = {'name': name, 'groups': groups, 'history': use_history, 'model': model,
           'n_features': len(cols) + (4 if use_history else 0),
           'fold_acc': accs, 'repeat_acc': per_repeat,
           'acc': float(np.mean(per_repeat)), 'acc_std_repeats': float(np.std(per_repeat))}
    log(f'{name:<34s} acc {res["acc"]:.4f} (repeats {", ".join(f"{a:.4f}" for a in per_repeat)}) '
        f'features {res["n_features"]}')
    return res, oof.mean(axis=0)


def paired(res_a, res_b, test_frac=1 / (N_FOLDS - 1)):
    """Mean fold-level difference b - a with the Nadeau-Bengio corrected SE."""
    d = np.array(res_b['fold_acc']) - np.array(res_a['fold_acc'])
    j = len(d)
    se = float(np.sqrt((1 / j + test_frac) * d.var(ddof=1))) if j > 1 else float('nan')
    return float(d.mean()), se


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

# The final model: the corrected state, P1 team species and items, move counts
# and P1's history. P2's bench is measured in the ablation (D, H) but left out.
FINAL_GROUPS = ['core', 'ko', 'p1sp', 'it', 'mv']
FINAL = ('E final', FINAL_GROUPS, True, 'lgb')

ABLATION = [
    # name, feature groups, P1 history, model
    ('A state, naive', ['core', 'naive'], False, 'lgb'),
    ('B state, hidden KOs', ['core', 'ko'], False, 'lgb'),
    ('C B + P1 history', ['core', 'ko'], True, 'lgb'),
    ('D C + P2 bench', ['core', 'ko', 'bench', 'p2sp'], True, 'lgb'),
    ('R loops-style reference', ['core', 'naive', 'p1sp', 'it', 'mv'], False, 'lgb'),
    ('F final - history', FINAL_GROUPS, False, 'lgb'),
    ('G final - hidden KOs', ['core', 'naive', 'p1sp', 'it', 'mv'], True, 'lgb'),
    ('H final + P2 bench', FINAL_GROUPS + ['bench', 'p2sp'], True, 'lgb'),
    ('I final, logistic', FINAL_GROUPS, True, 'logreg'),
]

# (label, config a, config b): paired difference b - a
COMPARISONS = [
    ('final vs loops-style reference', 'R loops-style reference', FINAL[0]),
    ('P1 history (final minus F)', 'F final - history', FINAL[0]),
    ('hidden KOs (final minus G)', 'G final - hidden KOs', FINAL[0]),
    ('P2 bench (H minus final)', FINAL[0], 'H final + P2 bench'),
    ('LightGBM vs logistic (final minus I)', 'I final, logistic', FINAL[0]),
]


def main():
    global N_REPEATS_RUN, N_JOBS, SEED
    parser = argparse.ArgumentParser()
    parser.add_argument('--quick', action='store_true', help='one CV repeat instead of three')
    parser.add_argument('--repeats', type=int, default=None, help='number of CV repeats')
    parser.add_argument('--no-ablation', action='store_true', help='only the final model')
    parser.add_argument('--configs', default=None,
                        help='comma-separated ablation letters to run, e.g. "A,B" (the final model always runs)')
    parser.add_argument('--jobs', type=int, default=None, help='LightGBM threads')
    parser.add_argument('--out', default=None, help='output folder (default: outputs/local, or /kaggle/working)')
    parser.add_argument('--seed', type=int, default=None, help='seed for folds and models (default 2026)')
    args, _ = parser.parse_known_args()
    N_REPEATS_RUN = args.repeats or (1 if args.quick else N_REPEATS)
    if args.jobs:
        N_JOBS = args.jobs
    if args.seed is not None:
        SEED = args.seed

    data, out = find_data_dir(), find_out_dir()
    if args.out:
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
    log(f'data {data}  output {out}  cpus {N_JOBS}')
    log(f'python {sys.version.split()[0]}  lightgbm {lgb.__version__}  scikit-learn {sklearn.__version__}  '
        f'pandas {pd.__version__}  numpy {np.__version__}')
    train = load_jsonl(data / 'train.jsonl')
    test = load_jsonl(data / 'test.jsonl')
    battles = train + test
    y = np.array([b['player_won'] for b in train], dtype=int)
    n_train = len(train)
    log(f'{n_train} train battles, {len(test)} test battles, P1 win rate {y.mean():.3f}')

    ref = Reference(battles)
    ko_probs, ko_info = calibrate_hidden_kos(battles, ref)
    pool = TeamPool(battles)
    vocab = build_vocab(battles)
    log(f'species {len(ref.species)}, pool teams {len(pool.teams)}, vocab: '
        f'{len(vocab["species"])} species, {len(vocab["items"])} items, {len(vocab["moves"])} moves')
    log(f'hidden-KO calibration: {ko_info}')

    X_all = build_static(battles, ref, pool, ko_probs, vocab)
    keys = history_keys(battles)
    freq_all = frequency_features(keys)
    X, X_test = X_all.iloc[:n_train].reset_index(drop=True), X_all.iloc[n_train:].reset_index(drop=True)
    freq, freq_test = freq_all.iloc[:n_train].reset_index(drop=True), freq_all.iloc[n_train:].reset_index(drop=True)
    keys_train = {k: v[:n_train] for k, v in keys.items()}
    log(f'static features: {X.shape[1]} columns; expected hidden P2 KOs per battle '
        f'{X["ko_p2_hidden_sum"].mean():.2f}, visible P2 KOs {X["core_p2_fnt"].mean():.2f}, '
        f'visible P1 KOs {X["core_p1_fnt"].mean():.2f}')

    folds = make_folds(y, N_FOLDS, N_REPEATS_RUN, SEED)
    hist_cache = [history_features(keys_train, y, a, v, SEED + 100 + k) for k, (r, a, v) in enumerate(folds)]
    log(f'{len(folds)} folds ({N_FOLDS}-fold x {N_REPEATS_RUN} repeats); history encodings ready')

    ablation = [] if args.no_ablation else ABLATION
    if args.configs:
        wanted = {c.strip() for c in args.configs.split(',')}
        ablation = [c for c in ablation if c[0].split()[0] in wanted]
    configs = ablation + [FINAL]
    results, oofs = {}, {}
    for name, groups, use_hist, model in configs:
        res, oof = run_cv(name, X, groups, use_hist, model, folds, y, hist_cache, freq)
        results[name], oofs[name] = res, oof

    # Paired comparisons on identical folds
    final_name, groups, use_hist, model = FINAL
    base_name = 'A state, naive' if 'A state, naive' in results else final_name
    lines = ['| config | features | CV accuracy | vs ' + base_name.split()[0] + ' (paired, ±SE) |',
             '|---|---:|---:|---:|']
    for name, res in results.items():
        d, se = paired(results[base_name], res)
        lines.append(f'| {name} | {res["n_features"]} | {res["acc"]:.4f} ± {res["acc_std_repeats"]:.4f} | '
                     f'{d:+.4f} ± {se:.4f} |')
        res['diff_vs_base'], res['se_vs_base'] = d, se
    table = '\n'.join(lines)
    print('\n' + table + '\n', flush=True)
    comparisons = {}
    for label, a, b in COMPARISONS:
        if a in results and b in results:
            d, se = paired(results[a], results[b])
            comparisons[label] = {'diff': d, 'se': se}
            log(f'{label}: {d:+.4f} ± {se:.4f} (corrected SE)')

    # Final model, fitted on all training battles
    log(f'final model: {final_name} (CV {results[final_name]["acc"]:.4f})')
    cols = select_columns(X.columns, groups)
    Xa, Xt = X[cols], X_test[cols]
    if use_hist:
        all_idx = np.arange(n_train)
        keys_full = keys   # train + test keys; only train labels are read
        y_full = np.concatenate([y, np.zeros(len(test), dtype=int)])
        ha, ht = history_features(keys_full, y_full, all_idx, np.arange(n_train, n_train + len(test)), SEED + 999)
        Xa = pd.concat([Xa.reset_index(drop=True), ha, freq], axis=1)
        Xt = pd.concat([Xt.reset_index(drop=True), ht, freq_test], axis=1)
    p_test, fitted = fit_predict(model, Xa, y, Xt, SEED)
    sub = pd.DataFrame({'battle_id': [b['battle_id'] for b in test],
                        'player_won': (p_test > 0.5).astype(int)})
    sub.to_csv(out / 'submission.csv', index=False)
    pd.DataFrame({'battle_id': [b['battle_id'] for b in test], 'p_win': p_test}).to_csv(
        out / 'test_probabilities.csv', index=False)
    pd.DataFrame({'battle_id': [b['battle_id'] for b in train], 'player_won': y,
                  'oof_p_win': oofs[final_name]}).to_csv(out / 'oof_predictions.csv', index=False)
    if hasattr(fitted, 'booster_'):
        imp = pd.DataFrame({'feature': fitted.booster_.feature_name(),
                            'gain': fitted.booster_.feature_importance('gain')})
        imp.sort_values('gain', ascending=False).to_csv(out / 'feature_importance.csv', index=False)
    log(f'submission.csv: {len(sub)} rows, predicted P1 win rate {sub.player_won.mean():.3f}')

    report = {'final': final_name, 'n_folds': N_FOLDS, 'n_repeats': N_REPEATS_RUN, 'seed': SEED,
              'hidden_ko_calibration': ko_info, 'comparisons': comparisons,
              'results': results, 'table': table}
    (out / 'cv_report.json').write_text(json.dumps(report, indent=2))
    (out / 'cv_report.md').write_text(table + f'\n\nFinal model: {final_name}\n')
    log('done; nothing was submitted')


N_REPEATS_RUN = N_REPEATS

if __name__ == '__main__':
    main()
