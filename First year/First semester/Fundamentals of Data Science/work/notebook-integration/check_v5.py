"""Execute the final V5 path verbatim, in a fresh process, with local I/O paths."""

import importlib.metadata
import json
import os
from pathlib import Path
import sys
import time

root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
out.mkdir(parents=True, exist_ok=True)
os.chdir(out)
notebook = root / 'report/other_approaches (2nd and 3rd)/submission_v5_catboos_dominant.ipynb'
nb = json.loads(notebook.read_text())
namespace = {'__name__': '__main__'}
started = time.monotonic()
versions = {name: importlib.metadata.version(name) for name in (
    'numpy', 'pandas', 'scikit-learn', 'lightgbm', 'xgboost', 'catboost')}
print('Environment:', json.dumps(versions), flush=True)
for index in (2, 3, 4, 6, 8, 18, 22):
    print(f'[{time.monotonic() - started:.1f}s] START original cell {index}', flush=True)
    source = ''.join(nb['cells'][index]['source'])
    exec(compile(source, f'{notebook}:cell-{index}', 'exec'), namespace)
    if index == 2:
        namespace.update({
            'DATA_DIR': str(out),
            'TYPE_CHART_PATH': str(root / 'data/type_chart_gen2.csv'),
            'EXCEL_UNPACKED_PATH': str(out / 'unused.xlsx'),
            'TRAIN_JSONL_PATH': str(root / 'data/train.jsonl'),
            'TEST_JSONL_PATH': str(root / 'data/test.jsonl'),
        })
    print(f'[{time.monotonic() - started:.1f}s] DONE original cell {index}', flush=True)

import pandas as pd

submission = pd.read_csv(out / 'submission_v5_catboost_dominant.csv')
sample = pd.read_csv(root / 'data/sample_submission.csv')
assert list(submission.columns) == ['battle_id', 'player_won']
assert len(submission) == len(sample) == 5000
assert submission.battle_id.is_unique
assert set(submission.battle_id) == set(sample.battle_id)
assert submission.player_won.isin([0, 1]).all()
print(f'PASS: {len(submission)} unique test IDs and binary predictions.', flush=True)
