from pathlib import Path
import json
import os

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

course = Path(__file__).resolve().parents[2]
root = course / 'challenge'
work = course / 'work/notebook-integration'
os.environ.update(
    FDS_REPO_URL=str(work / 'validation-repo'), FDS_REPO_REF='HEAD',
    FDS_DATA=str(root / 'data'), FDS_SKIP_INSTALL='1',
    JUPYTER_PATH=str(work / 'jupyter'), IPYTHONDIR=str(work / 'ipython'),
    JUPYTER_RUNTIME_DIR=str(work / 'jupyter-runtime'),
    MPLCONFIGDIR=str(work / 'matplotlib-cache'),
)

def execute(name, selected=None):
    os.environ['FDS_NOTEBOOK_WORK'] = str(work / name)
    os.environ['FDS_OUTPUT_ROOT'] = str(work / name / 'final_submissions')
    if selected:
        os.environ['FDS_SUBMISSIONS'] = selected
    else:
        os.environ.pop('FDS_SUBMISSIONS', None)
    nb = nbformat.read(root / 'final_submissions.ipynb', as_version=4)
    client = NotebookClient(nb, timeout=1800, kernel_name='fds-validation',
                            resources={'metadata': {'path': str(work)}})
    try:
        client.execute()
    finally:
        nbformat.write(nb, work / f'{name}.ipynb')
    return nb

try:
    execute('default-preflight')
    raise AssertionError('The default all-three run must report the missing V2 source')
except CellExecutionError as exc:
    if 'A selected original source is incomplete' not in str(exc):
        raise
    print('PASS: default notebook stops at preflight with the original V2 missing-code error', flush=True)

execute('first-submission-smoke', '01_hidden_ko_history')
manifest = json.loads((work / 'first-submission-smoke/final_submissions/01_hidden_ko_history/run_manifest.json').read_text())
print('PASS: first-submission notebook executed end to end', flush=True)
print(json.dumps(manifest['reference'], indent=2), flush=True)
