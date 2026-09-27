"""Standalone frozen helper; never runs from the installation being replaced."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback
from updater import apply_update, run_health_check, wait_for_parent, write_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', required=True)
    parser.add_argument('--archive', required=True)
    parser.add_argument('--manifest', required=True)
    parser.add_argument('--parent', type=int, default=0)
    parser.add_argument('--profile', required=True)
    parser.add_argument('--no-restart', action='store_true')
    args = parser.parse_args()
    result = Path(args.archive).parent/'result.json'
    try:
        if Path(sys.executable).resolve().is_relative_to(Path(args.target).resolve()):
            raise RuntimeError('Der Update-Helfer muss aus dem Download-Ordner gestartet werden.')
        wait_for_parent(args.parent)
        backup = apply_update(args.target, args.archive, args.manifest, run_health_check, args.profile)
        write_json(result, {'success':True, 'backup':str(backup)})
        if not args.no_restart:
            env = os.environ.copy()
            env['JAPANISCHTRAINER_DATA_DIR'] = args.profile
            subprocess.Popen([str(Path(args.target)/'JapanischTrainer.exe')], cwd=args.target, env=env)
        return 0
    except Exception as exc:
        write_json(result, {'success':False, 'error':str(exc), 'traceback':traceback.format_exc()})
        if not args.no_restart:
            import ctypes
            ctypes.windll.user32.MessageBoxW(None, str(exc), 'JapanischTrainer – Update fehlgeschlagen', 0x10)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
