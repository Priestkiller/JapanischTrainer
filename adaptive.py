"""Small daily practice, independent of course completion and XP.

Stable card keys; seconds since epoch in both ports. Help/self-checks never
become measured speaking competence. A persisted daily queue survives restart.
"""
from datetime import date
import math
import time

SKILLS = ('read', 'listen', 'write', 'speak', 'use')
LABELS = dict(read='Lesen', listen='Hören', write='Schreiben', speak='Sprechen', use='Anwenden', intro='Neu kennenlernen')
PHASE_SKILL = dict(meaning='read', listen='listen', write='write', build='write', apply='use', speak='speak')


def clean_adaptive(value):
    value = value if isinstance(value, dict) else {}
    out = {'skills': {}, 'introduced': [], 'daily': {}, 'milestones': {}}
    for key, skills in list(value.get('skills', {}).items())[:2000] if isinstance(value.get('skills'), dict) else []:
        if not isinstance(key, str) or len(key) > 150 or not isinstance(skills, dict):
            continue
        out['skills'][key] = {}
        for skill in SKILLS:
            raw = skills.get(skill)
            if not isinstance(raw, dict):
                continue
            def num(name):
                v = raw.get(name, 0)
                return max(0, min(10**12, v)) if isinstance(v, (int, float)) and math.isfinite(v) else 0
            out['skills'][key][skill] = {k: num(k) for k in ('attempts', 'right', 'streak', 'due', 'last', 'assisted')}
    out['introduced'] = list(dict.fromkeys(x for x in value.get('introduced', []) if isinstance(x, str) and len(x) < 150))[:2000] if isinstance(value.get('introduced'), list) else []
    raw = value.get('daily')
    if isinstance(raw, dict) and isinstance(raw.get('date'), str):
        tasks = [dict(id=x['id'], card=x['card'], skill=x['skill']) for x in raw.get('tasks', [])[:10]
                 if isinstance(x, dict) and all(isinstance(x.get(k), str) for k in ('id', 'card', 'skill'))
                 and x['skill'] in (*SKILLS, 'intro') and len(x['card']) < 150] if isinstance(raw.get('tasks'), list) else []
        done = [x for x in raw.get('done', []) if x in {t['id'] for t in tasks}] if isinstance(raw.get('done'), list) else []
        out['daily'] = dict(date=raw['date'][:10], tasks=tasks, done=list(dict.fromkeys(done)))
    if isinstance(value.get('milestones'), dict):
        out['milestones'] = {k: v for k, v in list(value['milestones'].items())[:100] if isinstance(k, str) and isinstance(v, dict)}
    return out


def record_attempt(data, key, skill, ok, assisted=False, now=None):
    if skill not in SKILLS:
        return
    now = time.time() if now is None else now
    a = data.setdefault('adaptive', clean_adaptive(None))
    m = a['skills'].setdefault(key, {}).setdefault(skill, dict(attempts=0, right=0, streak=0, due=0, last=0, assisted=0))
    m['attempts'] += 1
    m['last'] = now
    if assisted:
        m['assisted'] += 1
    if ok and not assisted:
        m['right'] += 1
        m['streak'] = min(6, m['streak'] + 1)
        m['due'] = now + (1, 2, 4, 7, 14, 30)[int(m['streak']) - 1] * 86400
    else:
        m['streak'] = 0
        m['due'] = now + (86400 if ok else 0)


def daily_plan(data, cards, available, upcoming, today=None, now=None):
    today = today or date.today().isoformat()
    now = time.time() if now is None else now
    a = data.setdefault('adaptive', clean_adaptive(None))
    by_key = {c['key']: c for c in cards}
    old = a.get('daily', {})
    if old.get('date') == today and old.get('tasks') and all(t['card'] in by_key for t in old['tasks']):
        return old
    known = list(dict.fromkeys([c['key'] for c in available if c['lesson_key'] in data.get('completed', []) or data.get('study_cards', {}).get(c['key'], {}).get('attempts', 0)>0 or c['key'] in data.get('review', {})] + [k for k in a['introduced'] if k in by_key]))
    candidates = []
    for key in known:
        for rank, skill in enumerate(SKILLS):
            m = a['skills'].get(key, {}).get(skill, {})
            if m.get('due', 0) > now:
                continue
            failures = m.get('attempts', 0) - m.get('right', 0)
            candidates.append((-min(20, failures), m.get('last', 0), rank, key, skill))
    candidates.sort()
    tasks = []
    chosen = set()
    for _, _, _, key, skill in candidates:
        if key in chosen or len(tasks) >= 5:
            continue
        chosen.add(key)
        tasks.append(dict(id=f'{today}:{key}:{skill}', card=key, skill=skill))
    for card in upcoming[:2]:
        if card['key'] not in a['introduced'] and len(tasks) < 7:
            tasks.append(dict(id=f"{today}:{card['key']}:intro", card=card['key'], skill='intro'))
    a['daily'] = dict(date=today, tasks=tasks, done=[])
    return a['daily']


def finish_daily(data, task, ok, assisted=False, now=None):
    a = data.setdefault('adaptive', clean_adaptive(None))
    plan = a['daily']
    if task not in plan.get('tasks', []) or task['id'] in plan.get('done', []):
        return False
    if task['skill'] == 'intro':
        if ok and task['card'] not in a['introduced']:
            a['introduced'].append(task['card'])
    else:
        record_attempt(data, task['card'], task['skill'], ok, assisted, now)
    if ok:
        plan['done'].append(task['id'])
    return bool(ok)
