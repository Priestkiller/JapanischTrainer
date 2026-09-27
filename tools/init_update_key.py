"""One-time local publisher key; never print or overwrite the private key."""
import base64
import json
import os
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

root=Path(__file__).resolve().parents[1]
folder=root/'.release-keys'
folder.mkdir(mode=0o700,exist_ok=True)
path=folder/'update-ed25519.key'
if path.exists():
    key=Ed25519PrivateKey.from_private_bytes(path.read_bytes())
else:
    key=Ed25519PrivateKey.generate()
    with path.open('xb') as stream:stream.write(key.private_bytes_raw())
    os.chmod(path,0o600)
config={'manifest_url':'https://github.com/Priestkiller/JapanischTrainer/releases/latest/download/update.json',
        'public_key':base64.b64encode(key.public_key().public_bytes_raw()).decode(),
        'downloads_url':'https://github.com/Priestkiller/JapanischTrainer/releases'}
(root/'update-source.json').write_text(json.dumps(config,indent=2)+'\n',encoding='utf8')
print('Lokaler Update-Schlüssel gesichert; öffentliche Update-Konfiguration geschrieben.')
