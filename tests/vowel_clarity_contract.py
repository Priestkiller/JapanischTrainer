"""Allow only the documented 11.0.15 wording errata in older course contracts."""
import copy, json
from pathlib import Path

PATCHES = json.loads((Path(__file__).parent / 'fixtures/vowel-clarity-11.0.15.json').read_text('utf8'))

def before_vowel_clarity(key, lesson):
    original = copy.deepcopy(lesson)
    for change in PATCHES.get(key, []):
        parent = original
        for step in change['path'][:-1]:
            parent = parent[step]
        field = change['path'][-1]
        assert parent[field] == change['after'], (key, change['path'], 'unexpected wording change')
        if change['existed']:
            parent[field] = change['before']
        else:
            del parent[field]
    return original

def before_retry_assessment(core):
    changes=json.loads((Path(__file__).parent / 'fixtures/retry-assessment-11.0.15.json').read_text('utf8'))
    for change in changes:
        assert core.count(change['after']) == 1, (change['method'], 'unexpected assessment change')
        core=core.replace(change['after'],change['before'],1)
    return core
